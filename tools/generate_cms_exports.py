import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "content" / "site-content.json"
OUT_DIR = ROOT / "cms-export"


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    pages = data["pages"]

    # Generic JSON export
    with open(OUT_DIR / "icentech_pages.json", "w", encoding="utf-8") as f:
        json.dump(pages, f, ensure_ascii=False, indent=2)

    # WordPress/Webflow-friendly CSV shape
    with open(OUT_DIR / "icentech_pages.csv", "w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["slug", "title_zh", "title_en", "summary_zh", "summary_en", "status", "template"]
        )
        writer.writeheader()
        for p in pages:
            writer.writerow(
                {
                    "slug": "/" if p["slug"] == "" else f'/{p["slug"]}',
                    "title_zh": p["title_zh"],
                    "title_en": p["title_en"],
                    "summary_zh": p["summary_zh"],
                    "summary_en": p["summary_en"],
                    "status": "draft",
                    "template": "default-bilingual-page"
                }
            )

    print("CMS export files generated.")


if __name__ == "__main__":
    main()
