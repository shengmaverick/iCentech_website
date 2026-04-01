# iCentech Website Workspace

This repository currently works best as a content-driven static site that deploys to GitHub Pages.

## Recommended Path

- Use `content/`, `pages/`, and `design-system/` as the editable source of truth.
- Use `tools/generate_static_site.py` to generate the publishable site into `static-site/`.
- Use `.github/workflows/deploy-pages.yml` to publish.
- Treat `nextjs-site/` and `nuxt-site/` as framework skeletons for later, not as the current production entrypoint.

## Structure

- `content/`: site data, blog metadata, blog HTML, and media
- `pages/`: bilingual page copy briefs
- `design-system/`: brand tokens and design notes
- `tools/`: static site generator and content utilities
- `static-site/`: generated GitHub Pages output
- `nextjs-site/`: Next.js prototype skeleton
- `nuxt-site/`: Nuxt prototype skeleton

## Local Build

```bash
python3 tools/generate_static_site.py
```

For a repository-based GitHub Pages preview such as `https://shengmaverick.github.io/iCentech_website/`, build with:

```bash
SITE_ORIGIN=https://shengmaverick.github.io \
SITE_BASE_PATH=/iCentech_website \
python3 tools/generate_static_site.py
```

For the future custom domain launch, build with:

```bash
SITE_ORIGIN=https://www.icentech.com \
SITE_BASE_PATH= \
python3 tools/generate_static_site.py
```

## Publish

Push to `main`. The Pages workflow regenerates `static-site/` and deploys it through GitHub Actions.
