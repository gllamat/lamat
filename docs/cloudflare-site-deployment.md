# Publishing the Lamat website

The site source is `apps/web`. The live `lamatq.co.uk` site is served by the
Cloudflare Workers & Pages application **lamat-preview**. Its name is historical:
its production deployment serves the live website. `preview.lamatq.co.uk` uses
the same production deployment, so it is not a separate staging environment.
The final intended canonical domain is `lamat-qanil.com` (tracked in #82).

## Prepare and review

1. Start from the latest approved site source. Make the change under `apps/web`.
2. Keep `_redirects` in sync with any historical URL changes. Cloudflare Workers
   static assets use this file; `vercel.json` is not used by Cloudflare.
3. Test the site locally and review the changed files. Check historical pages,
   plots, PDFs, and redirects affected by the change. Do not include private
   exports or credentials in the site directory.
4. From the repository root, create the upload package outside the site folder:

   ```sh
   python3 scripts/package_cloudflare_site.py /tmp/lamat-site-upload.zip
   ```

   The ZIP contains the site files at its root, includes `_redirects`, and
   excludes `vercel.json`. It checks Cloudflare's static asset file-count and
   per-file size limits. Inspect the ZIP before upload.

## Deploy and verify

1. Open Cloudflare dashboard → **Compute → Workers & Pages → lamat-preview →
   New deployment**. Upload the ZIP as static assets using the dashboard's
   existing deployment flow. Confirm the selected application is `lamat-preview`.
   **Deploying changes the live site**, including both custom domains.
2. Check the deployment is ready, then verify `https://lamatq.co.uk/`, the
   archive, changed pages and charts, a legacy redirect, an unknown path, HTTPS,
   and `www.lamatq.co.uk`. Check browser and mobile layouts as appropriate.
3. Record the deployment/version and verification in the relevant GitHub card.
   The dashboard currently uses manual uploads: a GitHub push alone does not
   publish a change.

## Rollback

Keep the last working Cloudflare deployment until the new one is verified.
Use Cloudflare's Deployments screen to roll back to the previous working version;
then retest the site. Do not delete Vercel or change DNS as part of ordinary
content updates. Domain and email changes are separate work; preserve Google
Workspace DNS records.
