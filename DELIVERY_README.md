# iCentech Website Delivery Pack

## Included Deliverables

### 1) Content Master
- `content/site-content.json`: single source of bilingual page content.
- `content/blog-posts.json`: local blog manifest used by the new site.
- `content/blog/`: local article body files.
- `content/blog-media/`: local blog cover images.

### 2) Static Multi-Page Website
- `static-site/*.html`: generated static pages for all site routes.
- Generator: `tools/generate_static_site.py`
- Shared stylesheet: `static-site/assets/site.css`
- Branded logo + page illustrations: `static-site/assets/`

### 2.1) Design System
- `design-system/README.md`: design-system overview.
- `design-system/COLOR_SYSTEM.md`: final approved brand color system.
- `design-system/tokens.css`: reusable CSS color tokens.

### 3) Next.js Skeleton
- Folder: `nextjs-site/`
- Uses shared `site-content.json`
- Routes: `/` and `/<slug>`

### 4) Nuxt Skeleton
- Folder: `nuxt-site/`
- Uses shared `site-content.json`
- Routes: `/` and `/<slug>`

### 5) CMS Import Exports
- `cms-export/icentech_pages.json`
- `cms-export/icentech_pages.csv`
- Generator: `tools/generate_cms_exports.py`

### 6) Previously Prepared Documents
- `icentech_bilingual_site_content.md`
- `icentech_pages_bilingual.yaml`
- `icentech_home_modern_copy.md`
- `icentech_page_templates_bilingual.md`
- `pages/*.md` page-level handoff docs

### 7) Blog Workflow Support
- `.github/ISSUE_TEMPLATE/blog-idea.md`: free GitHub issue intake for article planning.
- `blog-admin/README.md`: repo-based blog management workflow.
- `.github/workflows/build-static-site.yml`: GitHub Actions build workflow for site generation.
- `tools/import_blog_content.py`: importer for bringing original posts into the local blog system.

## How to Regenerate

1. `python3 tools/generate_static_site.py`
2. `python3 tools/generate_cms_exports.py`

## Run App Skeletons

### Next.js
1. `cd nextjs-site`
2. `npm install`
3. `npm run dev`

### Nuxt
1. `cd nuxt-site`
2. `npm install`
3. `npm run dev`
