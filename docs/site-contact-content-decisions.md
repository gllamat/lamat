# Contact, subscriptions and site content: migration decisions

Working inventory for [issue #37](https://github.com/gllamat/lamat/issues/37), observed 17 November 2026. Public pages and the repository preview were inspected without submitting forms or accessing protected content. These are observations and choices for the owner, not approved changes or proof that any service works.

| Area | Existing public site | New static preview | Decision and evidence needed |
| --- | --- | --- | --- |
| Contact | `/contact/` displays `contact@lamatuk.com` and a WordPress/Jetpack form requesting name, email, optional website and message. Its recipient, delivery, storage, spam protection and retention were not tested. | The home page links to `contact@lamat-qanil.com` via `mailto:`; it has no form. | Confirm which address is monitored and should be public, and who owns it. Choose a form, mail link or both; if keeping the form, determine its hosting and privacy notice. Verify mail records, controlled delivery and accessibility on staging. Preserve the old contact path or an approved redirect. |
| Subscriptions | The home page presents a WordPress/Jetpack email subscription form. Its subscriber list, consent, delivery, retention and account access were not inspected. | No subscription form is provided. | Choose whether to retain the WordPress service, migrate to an approved provider, or retire subscriptions. Identify the account owner and decide how existing consent, preferences and data are handled before any export or transfer. Document an approved end-to-end test and opt-out path. |
| Demo | `/demo/` returns a password-protected WordPress page. Its content and access list were not inspected. | No equivalent page exists. | The owner should inspect it through existing authorized access, identify its purpose and users, then approve preservation, replacement, restricted hosting or retirement. Test the chosen path without exposing protected material. |
| About and services | `/about/` describes finance data-science consulting, alternative data, cloud and high-frequency analysis. The public page also includes WordPress commenting controls. | The homepage presents research and AI consulting, with a shorter about section and no comments. | Approve the current service descriptions, about and contact copy, logo and brand assets; decide whether comments need preservation or moderation. Check permissions and attribution for any reused copy or imagery. Preserve or redirect `/about/` according to the approved route map. |

## Before launch

1. The owner records decisions, account custodians and applicable content permissions without putting credentials or personal data in the repository.
2. Implement the approved choices and arrange a controlled staging test: test successful delivery and failures for the chosen contact method; verify subscription confirmation, opt-out and owner access if subscriptions remain. Never transfer subscriber data without a separately approved destination and process.
3. Check the final addresses, links, keyboard access, small screens and copy on staging. Confirm legacy paths, redirects and any retained service still work after cutover. Record results and the owner’s approval.

Related: [migration and staging plan](site-migration-plan.md), [hosting options](site-hosting-options.md), and issues [#18](https://github.com/gllamat/lamat/issues/18) and [#19](https://github.com/gllamat/lamat/issues/19). This inventory does not complete #37; owner decisions, implementation and staging tests remain open.
