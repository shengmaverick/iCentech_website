import json
import re
import ssl
import urllib.parse
import urllib.request
from html import unescape
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BLOG_INDEX_FILE = ROOT / "content" / "blog-posts.json"
BLOG_BODY_DIR = ROOT / "content" / "blog"
BLOG_MEDIA_DIR = ROOT / "content" / "blog-media"

USER_AGENT = "Mozilla/5.0 (compatible; iCentechSiteImporter/1.0)"
SSL_CONTEXT = ssl._create_unverified_context()


def fetch_text(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20, context=SSL_CONTEXT) as response:
        return response.read().decode("utf-8", errors="ignore")


def fetch_binary(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20, context=SSL_CONTEXT) as response:
        return response.read()


def collapse_space(value):
    return re.sub(r"\s+", " ", value or "").strip()


def detect_language(value):
    return "zh" if re.search(r"[\u4e00-\u9fff]", value or "") else "en"


def strip_tags(value):
    return collapse_space(re.sub(r"<[^>]+>", " ", value))


def build_source_posts(payload):
    posts = payload.get("posts", [])
    if posts and "original_url" in posts[0]:
        return posts

    source_url = payload.get("source_url")
    if not source_url:
        return []

    document = fetch_text(source_url)
    pattern = re.compile(
        r'<div class="s-blog-entry-inner ">'
        r'.*?<a target="_self" href="(https://www\.icentech\.com/blog/[^"]+)" aria-label="([^"]+)"'
        r'.*?background-image:url\((.*?)\)'
        r'.*?<span class="s-blog-date">(.*?)</span>'
        r'.*?<div class="s-blog-details-blurb[^"]*"[^>]*>(.*?)</div>',
        re.S,
    )
    items = []
    for url, title, image, date, excerpt in pattern.findall(document):
        slug = url.rstrip("/").split("/")[-1]
        clean_image = unescape(image).replace("&amp;", "&")
        if clean_image.startswith("//"):
            clean_image = "https:" + clean_image
        items.append(
            {
                "slug": slug,
                "title": unescape(title),
                "date": unescape(date),
                "excerpt": collapse_space(unescape(excerpt)),
                "image": clean_image,
                "original_url": url,
            }
        )
    return items


def extract_blog_meta_blob(document):
    match = re.search(r"blogPostData=(\{.*?\});\$S\.siteData=", document, re.S)
    if not match:
        return {}
    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}


def extract_subtitle(document):
    match = re.search(
        r's-blog-subtitle"[^>]*>.*?<p><em>(.*?)</em></p>',
        document,
        re.S,
    )
    if not match:
        return ""
    return collapse_space(strip_tags(match.group(1)))


def extract_body_blocks(document):
    pattern = re.compile(
        r'<div class="s-component-content s-font-body"[^>]*>(.*?)</div></div></div>',
        re.S,
    )
    return pattern.findall(document)


def clean_fragment(fragment):
    value = fragment.strip()
    if not value or value == "<div></div>":
        return ""

    value = re.sub(r"</?span[^>]*>", "", value)
    value = re.sub(r"</?div[^>]*>", "", value)
    value = re.sub(r"<p[^>]*>\s*</p>", "", value)
    value = re.sub(r"<p>\s*<span[^>]*>\s*</span>\s*</p>", "", value)
    value = re.sub(r"<(p|li|ul|ol|h2|h3|strong|em)([^>]*)>", r"<\1>", value)
    value = re.sub(r'<a[^>]*href="([^"]+)"[^>]*>', r'<a href="\1">', value)
    value = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*alt=\"([^\"]*)\"[^>]*>", r'<img src="\1" alt="\2">', value)
    value = re.sub(r"<img[^>]*src=\"([^\"]+)\"[^>]*>", r'<img src="\1" alt="">', value)
    value = value.replace("<h2><p>", "<h2>").replace("</p></h2>", "</h2>")
    value = value.replace("<h3><p>", "<h3>").replace("</p></h3>", "</h3>")
    value = re.sub(r"\n{3,}", "\n\n", value)
    value = value.strip()

    if not strip_tags(value):
        return ""
    return value


def normalize_body(document):
    blocks = []
    for fragment in extract_body_blocks(document):
        cleaned = clean_fragment(fragment)
        if cleaned:
            blocks.append(cleaned)
    return "\n\n".join(blocks).strip()


def download_image(url, slug):
    parsed = urllib.parse.urlparse(url)
    extension = Path(parsed.path).suffix.lower()
    if extension not in {".jpg", ".jpeg", ".png", ".webp", ".gif"}:
        extension = ".jpg"

    BLOG_MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{slug}{extension}"
    target = BLOG_MEDIA_DIR / filename
    target.write_bytes(fetch_binary(url))
    return f"blog/{filename}"


def import_posts():
    payload = json.loads(BLOG_INDEX_FILE.read_text(encoding="utf-8"))
    posts = build_source_posts(payload)
    BLOG_BODY_DIR.mkdir(parents=True, exist_ok=True)
    BLOG_MEDIA_DIR.mkdir(parents=True, exist_ok=True)

    imported = []
    for post in posts:
        print(f"Importing {post['slug']}...", flush=True)
        try:
            document = fetch_text(post["original_url"])
            meta = extract_blog_meta_blob(document)
            body_html = normalize_body(document)
            subtitle = extract_subtitle(document)
            tags = meta.get("blogPostMeta", {}).get("tags", [])
            language = detect_language(post["title"])
            image_asset = ""
            if post.get("image"):
                try:
                    image_asset = download_image(post["image"], post["slug"])
                except Exception:
                    image_asset = post["image"]
            body_path = BLOG_BODY_DIR / f"{post['slug']}.html"
            body_path.write_text(body_html + "\n", encoding="utf-8")

            imported.append(
                {
                    "slug": post["slug"],
                    "title": post["title"],
                    "date": post["date"],
                    "excerpt": post.get("excerpt") or strip_tags(body_html)[:156],
                    "subtitle": subtitle,
                    "image": image_asset,
                    "source_url": post["original_url"],
                    "tags": tags,
                    "language": language,
                    "body_file": f"content/blog/{post['slug']}.html",
                }
            )
        except Exception as error:
            print(f"Skipped {post['slug']}: {error}", flush=True)

    BLOG_INDEX_FILE.write_text(
        json.dumps(
            {
                "source_url": payload.get("source_url"),
                "management": {
                    "model": "repo-managed-local-blog",
                    "body_dir": "content/blog",
                    "media_dir": "content/blog-media",
                },
                "posts": imported,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Imported {len(imported)} posts into local blog files.")


if __name__ == "__main__":
    import_posts()
