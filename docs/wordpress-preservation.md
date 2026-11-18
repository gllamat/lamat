# WordPress preservation worklist

Working inventory for [issue #36](https://github.com/gllamat/lamat/issues/36), 17 November 2026. The entries below are the 15 `Lamat blog` links in `apps/web/archive.json`, not a complete WordPress export. They identify existing public addresses, not approved redirects or proof that content has been backed up. A fresh owner export and route inventory may contain additional material. Preserve the existing site until restoration and staging checks pass.

## Article route inventory

Every path below needs its original content, media, dates and attribution checked against an authorized export. The destination, rights, restoration and staging checks for **every row are pending**. An appropriate destination could be the same path on a migrated site or an approved stable original on a different host; it has not yet been chosen. Redirecting any of these paths to the archive listing loses the original and can create loops because the listing links back to these URLs.

| Date in archive | Current path on lamatuk.com | Archive title |
| --- | --- | --- |
| 2022-01-21 | `/2022/01/21/swaptions/` | Swaptions |
| 2021-12-14 | `/2021/12/14/mexican-swaps/` | Mexican Swaps |
| 2021-12-13 | `/2021/12/13/agnostic-crypto-allocation/` | Agnostic Crypto Allocation |
| 2021-09-22 | `/2021/09/22/inflation-swaps/` | Inflation Swaps |
| 2021-07-07 | `/2021/07/07/companies-house-and-heaven/` | Companies House and Heaven |
| 2021-03-02 | `/2021/03/02/etf-component-liquidity/` | ETF component liquidity |
| 2021-02-12 | `/2021/02/12/reddit-analysis/` | Reddit Analysis |
| 2021-01-29 | `/2021/01/29/sentiment-analysis-in-finance/` | Sentiment Analysis in Finance |
| 2021-01-26 | `/2021/01/26/option-networking/` | Option networking |
| 2020-12-02 | `/2020/12/02/financial-data-mining-public-2/` | FX SDR-SEC |
| 2020-11-29 | `/2020/11/29/market-flies/` | Fixed Income SDR |
| 2020-05-16 | `/2020/05/16/data-science-vs-european-regulations/` | Data Science vs European Regulations |
| 2020-04-07 | `/2020/04/07/example-post/` | Why Financial Time Series LSTM Prediction fails |
| 2020-04-07 | `/2020/04/07/example-post-2/` | Calling AI’s bluff |
| 2020-04-07 | `/2020/04/07/example-post-3/` | AI in Finance: Cutting Through the Hype (With Case Studies) |

Also reconcile `/`, `/about/`, `/contact/`, `/blog-2/`, `/demo/`, `/blog/`, sitemap and robots files, feeds, attachments, uploaded assets, alternate hostnames and inbound links. The [migration plan](site-migration-plan.md) records the prior public snapshot and the pending form, subscription and DNS decisions. A sitemap alone cannot establish a complete set of routes or assets.

## Owner export and restoration

1. Confirm the WordPress account, hosting plan, administrators, ownership and backup scope. An owner or authorized administrator obtains a fresh content export and a separate copy of the media library using the applicable WordPress.com tools. The XML export is not by itself an offline copy of all media. Availability and method differ with plan and plugins; consult [content export](https://wordpress.com/support/export/) and [media export](https://wordpress.com/support/export-your-media-library/). Where available, also obtain a complete [site backup](https://wordpress.com/support/restore/download-backup/) and record its scope; theme and plugin settings may need separate documentation.
2. Store exports and backups privately with the owner, record date, source, location, scope, integrity checks and responsible custodian. They may include drafts, comments, contact messages, personal data and credentials. Do not commit them to this public repository or publish them as-is.
3. Restore a copy in an isolated, access-controlled environment, with outgoing email and indexing disabled as appropriate. Confirm that the restored pages, originals, attachments, embeds, dates and attribution match the source; record gaps and recovery steps. This has not yet been done. An export that opens is not evidence that the site can be restored.
4. Review rights for text, media, embedded content and contributors before any republication. Decide whether each original remains on WordPress at a stable host or is migrated. Record the destination and responsible reviewer for each row; preserve paths where possible. Do not add production redirects until destinations and ownership are agreed.

## Staging acceptance for each route

For each article and additional approved route, record the source URL, approved destination, intended status, test date and result. Check the actual destination content and attribution, media and embeds, canonical URL, trailing slash and query behavior, HTTPS, redirect hops and loops, plus links from the new archive. Confirm that missing resources return an appropriate error rather than a successful homepage. Compare the final map against the fresh export, sitemap, media and known inbound links. Keep the review evidence and actual backup locations private where they contain sensitive material.

The user-facing site must not be switched to a static deployment until content, redirects and rollback are approved and verified on hosted staging. See [hosting options](site-hosting-options.md) when available and [issue #39](https://github.com/gllamat/lamat/issues/39) for cutover and rollback.
