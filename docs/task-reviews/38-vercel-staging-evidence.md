# Vercel staging evidence

On 18 November 2026, the owner redeployed commit `bc66a82153d00140eaa87352512ca0d88f14057d` to a Vercel preview after changing the project root to `apps/web` and the framework preset to Other. The Vercel deployment screen reported Ready. This is staging evidence for [issue #38](https://github.com/gllamat/lamat/issues/38), not a launch approval.

## Checks recorded

- In an authenticated browser, the homepage loaded, its historical archive navigation opened the archive, and the contact link displayed `contact@lamat-qanil.com`. A made-up path displayed the site's not-found page. Its HTTP status was not verified.
- Independent unauthenticated requests to the homepage, archive, stylesheet, logo and a made-up path returned a redirect to Vercel sign-in. The homepage response included `noindex` and `no-store` headers. This confirms observed protection for these requests, not every possible URL or configuration.
- The archive links its Lamat articles to the existing `lamatuk.com` site. This check did not verify each external destination or preservation after cutover.

## Still required

Record the actual authenticated 404 status and asset responses; test all approved routes and contact delivery, responsive layouts, zoom, keyboard and screen-reader use, contrast, reduced motion, browsers and owner review. Confirm preview access and indexing after configuration changes. Article preservation, redirects, forms, subscription replacement and the rollback plan remain separate open work. Do not treat this partial check as completion of #38 or approval to switch DNS.


## Additional checks on 18 November 2026

- In the authenticated homepage, Tab focused the skip link; Enter navigated to `#main`, and the next Tab focused “Explore our work”. All seven homepage same-page link targets existed, and both logo images loaded. The archive targets for 2025, 2021 and 2018 existed.
- At 320 CSS pixels wide, the homepage and archive document widths matched the viewport without horizontal document overflow; both were visually inspected at 375 pixels. These are limited viewport checks, not a full responsive or accessibility audit.
