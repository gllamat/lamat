# Analytics, privacy and site operations: decisions and handover

Working inventory for [issue #40](https://github.com/gllamat/lamat/issues/40), 18 November 2026. No analytics or privacy setting was changed. Owner decisions, a hosted staging test and an accepted maintenance handover remain outstanding.

## What is known

| Area | Evidence | Still to establish |
| --- | --- | --- |
| Existing WordPress site | The [migration inventory](site-migration-plan.md) records `stats.wp.com` and `s0.wp.com` scripts observed on home/contact pages on 17 November. WordPress contact and subscription forms were observed but not submitted. | Active products, actual requests and cookies, consent choices, account access, recipients, data flows and retention cannot be inferred from script names. Inspect the authenticated WordPress/Jetpack configuration with the owner and record the date, purpose and custodian of each service. |
| New static source | Inspection of the repository HTML and stylesheet at `bc66a82` found no JavaScript analytics tag, embedded iframe, cookie banner or privacy notice in the home, archive and 404 pages. The archive contains external links and the home page uses an email link. | A host, proxy, browser extension or future code can introduce requests, cookies and logging independently of these files. This is not a deployed network capture or evidence that personal data is not processed. Confirm host settings and observe staging with a clean browser. |
| Contact and subscriptions | Current-site forms exist; the new static preview has a mail link and no subscription form. | Decide whether to preserve or replace either service; identify the account holder, purpose, access and retention before changes or any subscriber-data transfer. Track implementation in [#37](https://github.com/gllamat/lamat/issues/37). |
| Legal and privacy information | Existing-site settings and any applicable notice have not been authenticated or reviewed. The static pages above do not link to a privacy notice. | Have the owner identify applicable jurisdictions, information obligations and consent choices, obtain appropriate advice if needed, and approve notice text and placement. Do not infer compliance or add a generic banner solely from this inventory. |

## Record owner decisions before enabling a service

For each proposed analytics, error-monitoring, hosting log, consent, contact or subscription service, record the decision (including **none** if appropriate), purpose and owner; provider and account; data categories and recipients; retention, access and deletion procedure; relevant consent or opt-out behaviour; notice and policy links; and where configuration and renewal are maintained. Check provider terms, applicable requirements and cost with the owner. Store account recovery details and private exports in an approved private location, not this public repository. Do not migrate subscriber data until its destination and handling are approved.

## Staging acceptance

1. Record the deployed commit, provider, configuration, access controls, tester and date. Use a clean browser profile; capture network requests and storage before and after any presented choice, without submitting real personal data. Include initial load, navigation, rejected/accepted choices if applicable, and a revisit; document origins, purpose and any unexpected third-party requests. Inspect server-side settings separately because browser capture cannot see all logs or processing.
2. Compare the results against the owner-approved service and data inventory. Verify any privacy notice, choice controls and links, and test only an explicitly approved contact/subscription flow with agreed test data. Verify staging data is separated from production and that monitoring does not publish sensitive URLs or form contents.
3. Record evidence and defects privately where necessary, resolve discrepancies, and have the owner review the results before launch. Repeat after material provider or configuration changes. See [hosting options](site-hosting-options.md) and the [migration plan](site-migration-plan.md).

## Maintenance handover to complete

The following roles are **unassigned**, and the intervals below are proposed review prompts rather than an agreed schedule. The owner should assign named primary and backup custodians privately and approve a schedule before publication.

| Responsibility | Proposed check | Owner / backup / evidence |
| --- | --- | --- |
| Domain, DNS and hosting | Review renewals and access before expiry; inspect service notices and billing. | Pending |
| Deployments and rollback | Review branch protections and production changes; retain a known-good version and rehearse recovery. | Pending; coordinate [#39](https://github.com/gllamat/lamat/issues/39) |
| Site health and contact | Check critical routes, TLS, article links, 404s and the approved contact flow after releases and periodically. | Pending |
| Privacy and analytics | Review service inventory, consent/notice and access when providers or purpose change and at an agreed interval. | Pending |
| Content and accessibility | Review archive links, copy, permissions, accessibility issues and reported defects at an agreed interval. | Pending |
| Incident response | Record monitoring destination, escalation contact, response target and recovery decision maker; test the handover. | Pending |

Issue #40 remains open until the owner has made the choices, staging verifies the approved configuration, and the handover has named custodians and been reviewed.
