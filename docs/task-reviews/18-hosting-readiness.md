# Review: Vercel and Cloudflare Pages preparation

This adds a provider-neutral 404 page and a setup and verification guide for both Vercel and Cloudflare Pages. Review the project-root and output-directory settings, access and automatic-deployment warnings, and the preservation requirements for the current WordPress articles before applying the guide. The 404 page prevents Cloudflare Pages' documented default SPA fallback; its actual response status must be checked on a hosted deployment.

No accounts, projects, deployments, permissions, DNS, redirects or live site were changed. No staging environment exists as a result of this change. The existing migration plan's review and staging tasks, and publication in #19, remain open. Provider behavior and account features must be confirmed at deployment time.
