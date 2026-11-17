# Lamat website migration and staging plan

Working plan, 17 November 2026. Prepared for [issue #18](https://github.com/gllamat/lamat/issues/18). This is an inventory and proposed migration plan, not authorization or evidence of a deployment, DNS change, or completed staging review.

## Current public site: observed inventory

Read-only checks on 17 November 2026 found:

- The home page, `/about/`, `/contact/`, `/blog-2/`, and `/demo/`, plus 15 dated post URLs, appear in the site's [published sitemap](https://lamatuk.com/sitemap-1.xml). The [WordPress pages API](https://lamatuk.com/wp-json/wp/v2/pages?per_page=100) returned those five pages; the posts inventory is recorded in [the archive audit](task-reviews/08-historical-archive-audit.md). This is a public snapshot, not a complete server, media, draft, attachment or inbound-link inventory.
- `/blog/` redirected to the home page during the check. `robots.txt` advertises `sitemap.xml` and `news-sitemap.xml`; `/wp-sitemap.xml` redirected to the sitemap index. Sitemap XML identified Jetpack. The site served pages with a WordPress/Jetpack contact form and a WordPress email subscription form. Neither form was submitted; functionality, recipients, subscriber access and retention remain unverified.
- Home and contact pages loaded scripts from `stats.wp.com` and `s0.wp.com`. Their presence alone does not establish what data is collected, which analytics are active, consent settings, or account ownership.
- Public DNS answers listed WordPress.com nameservers, with `www.lamatuk.com` resolving as an alias to the apex. This is a point-in-time DNS observation, not proof of domain registrar, billing, hosting contract, control, TTLs, email records or access. Confirm the authoritative DNS zone and domain ownership before any cutover.

## Preserve URLs and original content

The new static preview has `index.html` and `archive.html`; it has no server-side redirects or migrated article bodies. The 15 Lamat archive entries link to their existing `lamatuk.com` post URLs. **If the same domain is switched to the new preview without preserving those pages, the archive's Lamat links will break.** Redirecting those URLs to the archive itself would also lose the originals and may create circular links. Retaining the current site, migrating authorized originals at their existing paths, or hosting an owner-approved archive at a stable address are alternatives to evaluate before cutover.

| Existing path | Proposed treatment, subject to owner review |
| --- | --- |
| `/` | New homepage only after staging and content approval. |
| `/about/`, `/contact/` | Preserve paths as accessible equivalents or tested redirects to corresponding sections; decide how the existing form and older contact address are handled. |
| `/blog-2/` | Preserve or redirect to the historical archive only if original post destinations remain available. |
| 15 dated post URLs | Preserve each original and attribution at its existing URL, or link to an owner-approved stable original with a tested one-to-one redirect where appropriate. Do not substitute a generic archive landing page for the post. |
| `/demo/` | Inspect content, ownership and usage with the owner before deciding whether to preserve, redirect or retire. |
| `/robots.txt`, sitemaps, assets and feeds | Inventory actual consumers and destinations; regenerate and validate for the selected host. Do not silently drop needed media, feed, discovery, or subscription endpoints. |

The source-of-truth list for the 15 post URLs is `apps/web/archive.json` entries with `kind` equal to `Lamat blog`; the sitemap may change. Before migration, obtain a fresh WordPress export, media library, URL/redirect and plugin configuration, server logs or analytics where available, and backups. Include query strings, trailing slash behavior, alternate domains, legacy links, canonical URLs, and high-value inbound URLs in a separately reviewed redirect map. Verify licences and contributor permissions before copying any text or imagery. Preserve source dates, credits and editorial history.

## Owner and access decisions

1. Confirm the domain registrar, DNS and hosting administrators, account access, renewal dates, and who can approve or roll back a change. Record credentials in a secret manager, never in this repository.
2. Choose hosting and staging access, and whether the historical WordPress site remains available at its original domain, another stable address, or as migrated pages. Decide how 15 dated posts, `/demo/`, media and redirects will be preserved.
3. Decide the fate of the existing contact form and WordPress email subscriptions, including owner access to submissions/subscriber data, consent and retention. The preview uses a `mailto:` link; it does not reproduce either service.
4. Confirm any analytics, consent, privacy and accessibility requirements; choose tools only after review. Check the current site and preview for personal or third-party content that needs permission.
5. Approve current-work descriptions and the final about/contact copy. Obtain higher-resolution logo assets and exact brand specifications if available.

## Staging and release checklist

- [ ] Back up the site, export content/media and redirect configuration, and verify restoration with the hosting owner.
- [ ] Create a private or appropriately access-controlled staging environment on the selected host, with no changes to public DNS or the live site. Protect staging from unintended search indexing where supported, and test that protection.
- [ ] Test desktop, tablet and narrow mobile widths, 200% text zoom, keyboard navigation, visible focus, skip link, headings, text contrast, and a screen reader; record actual browsers and results. Fix failures before launch.
- [ ] Verify every internal link and asset, contact destination, original article link, archive order and date labels. Test the agreed redirect map, no loops, trailing slashes, query handling and 404 page. Test forms or subscription alternatives end to end only with an approved test plan.
- [ ] Validate metadata, canonical URLs, sitemap, robots, analytics and privacy choices; make sure staging URLs and test content do not leak into production metadata.
- [ ] Document DNS records and TTLs, HTTPS certificate provisioning, cutover owner, rollback triggers and steps, monitoring, and a recovery exercise. Preserve mail-related records when changing DNS providers.
- [ ] Owner reviews the staging site, source rights, redirect map and rollback plan before a separate launch decision. Check critical links and contact flow after cutover and monitor errors.

## Verification status

Only the public inventory and the preceding local preview checks are complete. No staging environment, migration, redirect configuration, owner review, comprehensive accessibility audit or launch has been performed. The task remains In Progress until the owner decisions, reviewed plan and staging checks required by the issue are complete.
