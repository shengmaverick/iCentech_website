# Blog Management With GitHub

This redesign now uses the repository itself as the blog management system, based on GitHub's free workflow.

## Current Blog Structure

- Article manifest: `content/blog-posts.json`
- Article bodies: `content/blog/*.html`
- Blog cover images: `content/blog-media/*`
- Generator: `tools/generate_static_site.py`
- Import helper: `tools/import_blog_content.py`

## Recommended Editorial Flow

1. Create a new issue from `.github/ISSUE_TEMPLATE/blog-idea.md`
2. Label it with a status such as `needs-draft`, `in-review`, or `ready-to-publish`
3. Add or edit a post body in `content/blog/`
4. Add or update the metadata entry in `content/blog-posts.json`
5. Add or replace the cover image in `content/blog-media/`
6. Open a pull request for review
7. Regenerate the static site with `python3 tools/generate_static_site.py`
8. Publish the updated site

## Why This Works

- GitHub Issues: free intake queue for topics and source notes
- Pull Requests: built-in review, approval, and change history
- Labels / Projects: free editorial status tracking
- Local files in the repo: the blog belongs to the new site, not the old platform
- GitHub Actions: optional free build validation for every content update

## Import Workflow

If you want to refresh existing posts from the old site into local files again:

1. Run `python3 tools/import_blog_content.py`
2. Run `python3 tools/generate_static_site.py`

The importer converts each original blog page into:

- a local article body file
- a local cover image
- a manifest entry that the generator can publish into `/en/blog/` and `/zh/blog/`

## Publishing Goal

The key rule for this new setup is simple:

- `News & Blog` should publish articles inside the redesigned site
- blog cards should link to local article pages
- GitHub should manage intake, edits, review, and build history
