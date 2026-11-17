# Vercel and Cloudflare Pages deployment preparation

Prepared for issues #18 and #19 on 17 November 2026. Both options serve the same static files in `apps/web`; no framework, install, build, server, database or secret is required. These are setup instructions, not evidence of an account, deployment, access protection, DNS change or launch. The existing site and domain remain in place until the migration plan is approved.

## Before creating either project

- Choose the provider, account, billing owner, production and preview branches, authorized reviewers, and access protection. Check the provider's current plan, commercial-use terms, usage limits and costs. Do not put secrets or subscriber data in this public repository.
- Connecting a Git repository can immediately create a deployment and later pushes can trigger production or public previews. Before authorizing an integration, understand its initial deployment and visibility, configure branch controls and protection where available, and confirm who can access **every** generated URL. A hostname that is hard to guess and `noindex` are not access controls. Use only approved, non-sensitive content if protection cannot be established before first deployment.
- Do not attach `lamatuk.com`, alter DNS, or replace WordPress until the 15 dated articles and other legacy routes are preserved as described in [the migration plan](site-migration-plan.md). The new archive links to those same original URLs. Neither option below supplies the old posts or redirects. Preserve and test existing mail records, forms, subscriptions, media and rollback separately.

## Vercel: static project

1. Import the repository in the chosen Vercel account, after reviewing repository permissions and the first deployment's visibility. Set the **Root Directory** to `apps/web`.
2. Set Framework Preset to **Other**. Leave the build and install commands empty; serve the project root (`.`) as the output directory, with no `public` subdirectory override. Check the effective settings before deploying. These files are already deployable and require no build.
3. Configure Deployment Protection before sharing anything. Vercel's [September 2026 announcement](https://vercel.com/changelog/protect-production-deployments-for-free-on-every-plan) says Vercel Authentication with **All Deployments** can protect production and previews on every plan. Confirm the setting and intended reviewers' access in the actual account; a newer announcement differs from some older documentation. Do not assume an initial production URL is private.
4. Record the deployed commit and verify the generated domain without attaching the live domain. Confirm unauthenticated access is denied wherever protection is intended, then perform the checks below.

References: [Vercel build configuration](https://vercel.com/docs/builds/configure-a-build), [Vercel deployment protection](https://vercel.com/docs/deployment-protection), [Vercel project configuration](https://vercel.com/docs/project-configuration/vercel-json).

## Cloudflare Pages: static project

1. Create a Pages project for the chosen account and select Git integration only after reviewing repository permissions and the first deployment's visibility. Set the **Root directory** to `apps/web`, framework preset to **None**, build command to `exit 0`, and build output directory to `.` (relative to that root). Cloudflare recommends `exit 0` for a no-build static project. Confirm the effective settings before deploying.
2. Select the intended production branch and configure branch deployment controls. Pages Git integration can deploy production and preview branches automatically. A Git-integrated project cannot later be converted to a Direct Upload project; automatic deployments can be disabled. A Direct Upload project is a separate option if that operational model is preferred.
3. Pages preview deployments are public by default. Cloudflare Access can protect preview URLs, but its documented Pages preview policy does **not** protect the production `*.pages.dev` or custom domain. Configure and verify an appropriate Access policy for every relevant hostname before treating it as private, or use only content approved for public exposure. Check actual access from an unauthenticated session.
4. Record the deployed commit and verify the generated domain without attaching the live domain. `404.html` is included at the web root so Pages does not use its default single-page-app fallback for missing paths. Verify the response status and body on the actual deployment; this page does not preserve any old article.

References: [Cloudflare static HTML](https://developers.cloudflare.com/pages/framework-guides/deploy-anything/), [Pages build configuration](https://developers.cloudflare.com/pages/configuration/build-configuration/), [Git integration and branch controls](https://developers.cloudflare.com/pages/configuration/git-integration/), [preview protection](https://developers.cloudflare.com/pages/configuration/preview-deployments/), [serving pages](https://developers.cloudflare.com/pages/configuration/serving-pages/).

## Verify on each chosen host

- Record date, commit, host, access settings, reviewer and evidence. Visit `/`, `/archive.html`, `/style.css` and the logo; confirm successful responses and that archive entries and links render. Test a made-up nested route and a missing legacy article path for a real `404` response with the not-found page, rather than a successful homepage fallback. Do not infer historical article preservation from a 404.
- Verify focus and keyboard navigation, skip link, viewport widths and 200% zoom, contrast, screen reader, and current browsers; record results and defects. Verify every archive destination, contact email, canonical/metadata and all approved redirects. Forms and subscriptions require a separately agreed test plan.
- Confirm indexability and access controls, then complete the backup/restore, content rights, redirects, forms, DNS, HTTPS, cutover, owner and rollback checks in the [migration plan](site-migration-plan.md). Production publication is a separate decision; neither hosting setup nor a merge completes issue #19.
