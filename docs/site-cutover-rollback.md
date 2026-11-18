# Lamat DNS cutover and rollback runbook

Prepared for [issue #39](https://github.com/gllamat/lamat/issues/39), 17 November 2026. This is a reviewable plan, not permission to deploy, change DNS or retire WordPress. No owner, provider account, exact destination records, cutover window, restore test or approval has been confirmed. Keep issue #39 open until the owner completes the evidence and rehearsal below.

## What is known and what is not

A recursive `dig` query at approximately 23:25 UTC on 17 November 2026 returned three nameservers (`ns1.wordpress.com`, `ns2.wordpress.com`, `ns3.wordpress.com`), apex A records `192.0.78.187` and `192.0.78.213`, MX priority 0 to `smtp-fwd.wordpress.com`, and a `www` CNAME to `lamatuk.com`. This is a time-limited, public observation, **not** a complete authoritative zone export, a mail-delivery test, or proof of registrar, service ownership or DNS control. Empty AAAA and DS answer sections were not independently validated and do not establish their absence. TTLs returned by recursive resolvers are cache values, not a reliable substitute for configured TTLs. Never use this snapshot as the sole rollback source.

The new archive currently links to dated WordPress articles on `lamatuk.com`. A DNS switch without a working preservation solution will break those links. Article and media preservation and approved mappings are tracked in #36; contact and subscriptions in #37; staged checks in #38; and analytics and maintenance in #40. [The migration plan](site-migration-plan.md) defines the broader acceptance criteria.

## Evidence and decisions to obtain before any change

Record the following in an owner-controlled location, linking the location and completed date in a review record. Do not put credentials, tokens, subscriber lists, raw form submissions, or private account exports in this public repository.

| Evidence or decision | Required before cutover |
| --- | --- |
| Authority | Identify registrar and renewal owner, authoritative DNS provider, WordPress host, intended new provider and account, DNS operator, release decision-maker, technical rollback operator and monitoring contact. Confirm access and renewal status without recording credentials here. |
| Baseline and restoration | Export the complete current authoritative zone, including all records and configured TTLs, delegation, CAA, MX, SPF, DKIM, DMARC, verification, certificate-challenge and subdomain records. Record nameservers and registrar DS/DNSSEC state, old hosting settings, certificate, redirect rules, WordPress content/media, plugin/configuration and backups. Store securely; verify restoration into an isolated environment. A public lookup cannot discover the full zone or all DKIM selectors. |
| Destination | Select Vercel or Cloudflare Pages, production project and exact immutable site revision. Document apex and `www` handling, provider-generated domain-verification and routing records, certificates and any relevant proxy/caching settings. Capture the provider's actual instructions for the chosen account; do not guess record values. |
| Content and services | Owner approves the preservation/redirect map, content rights, contact and subscription handling, canonical URLs, robots, sitemaps, feeds and analytics. Verify all known old article destinations on staging without loops or generic archive substitutions. |
| Operational plan | Record approved change window, before/after zone exports, TTLs and waiting period, owner-approved acceptance checks, numerical rollback triggers and a deadline for decision, monitoring period, and escalation/communication contacts. Keep the previous site and domain service operational through rollback and the agreed observation window. |

## Provider-specific planning

* **Vercel:** A project can use existing DNS with the provider-supplied apex A and subdomain CNAME records, or use Vercel nameservers. Changing web records at the current DNS provider does not by itself require moving the rest of the zone. If choosing nameserver migration, copy and verify the complete zone first; do not assume a public DNS scan found every record. Verify domain ownership, redirects and certificate status in the target project. See [Vercel domain setup](https://vercel.com/docs/domains/working-with-domains/add-a-domain).
* **Cloudflare Pages:** Its [custom domain instructions](https://developers.cloudflare.com/pages/configuration/custom-domains/) say a Pages apex domain requires the zone and Cloudflare nameservers; a subdomain can use a CNAME without moving the apex zone. Both require associating the hostname with the Pages project. Nameserver migration changes authority for mail and all other zone records, not just the website. Verify imported records, proxy settings, domain activation, CAA and certificate issuance. Cloudflare warns that changing a Pages DNS entry away and back can leave the domain inactive until reactivated; factor this into the rollback exercise.
* **DNSSEC:** Establish whether the parent has a DS record, whether the old zone is signed and who controls both ends. For a nameserver change, follow the registrar and providers' current supported transition procedure; stale parent DS records can cause validating resolvers to return SERVFAIL. Do not blindly disable or enable DNSSEC. See [Cloudflare DNSSEC guidance](https://developers.cloudflare.com/dns/dnssec/).

## Rehearsal and cutover sequence

1. Run an isolated restoration of the previous site and a DNS/route rehearsal on non-production hostnames or a provider-supported staging environment. Verify restoration, mail-related configuration without sending unapproved test messages, certificate behavior, preservation routes, 404 and rollback steps. Record evidence and deviations. A dry run does not prove production DNS behavior.
2. Before the window, verify all evidence above, production content and redirects, staging review, access controls, backups, and both new and old-host readiness. Confirm decision-maker and rollback operator are available and understand the trigger and deadline. Capture fresh authoritative and recursive DNS answers and full configured values. If any prerequisite is missing, postpone.
3. With a separate owner-approved launch decision, apply only the chosen provider's reviewed domain and DNS changes, preserving mail and unrelated records. For a nameserver transfer, follow the approved delegation and DNSSEC sequence; do not copy the snapshot above as a zone. Record exact changes, timestamps and operators securely.
4. Check authoritative and independent recursive DNS responses during propagation, then HTTPS certificate validity, apex/`www` routing, homepage, archive, assets, approved legacy URLs and redirect chains, 404 status, contact behavior and agreed mail checks. Check canonical URLs, robots/sitemaps, approved analytics and monitoring. Some resolvers may continue serving cached old records; maintain both endpoints and observe for the agreed TTL/propagation period.
5. Compare results against agreed acceptance thresholds and deadline. Record the release decision, evidence, issues and owner. Keep the prior service recoverable until the decision-maker explicitly releases it after monitoring.

## Rollback procedure to rehearse and approve

1. The named decision-maker calls rollback if a pre-agreed trigger is met; log time, symptoms and operator. Stop further changes, preserve diagnostics and notify the agreed operational contacts.
2. Restore the **fresh pre-cutover** web routing and redirect configuration, retaining mail and unrelated DNS changes. If authority changed, restore delegation and DNSSEC using the rehearsed provider/registrar sequence and the complete backup; confirm the old nameservers and old zone remain functional. If only web records changed, restore their exact saved values and TTLs at the authoritative provider. Avoid assuming the 17 November snapshot is current.
3. Verify old WordPress hosting, TLS and redirects are still available and check apex, `www`, key original articles, approved contact flow and mail configuration using authoritative and independent resolvers. Account for cached new and old answers and the provider's domain reactivation behavior; keep monitoring until acceptance is met.
4. Record results and unresolved incidents. A rollback does not imply every resolver immediately returned to the old site. Preserve logs and backups, identify the root cause and require a new reviewed change plan before retrying.

## Status

Public DNS observation and this draft runbook are complete. Account-level inventory, selected provider and ownership, exact records, DS/DNSSEC status, consent/rights, staging and restoration tests, rollback triggers, rehearsal and owner review remain outstanding. No live records, nameservers, hosting, domain assignments, forms or production content were changed.
