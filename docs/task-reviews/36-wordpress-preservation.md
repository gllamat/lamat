# Task 36: preservation inventory review

The [worklist](../wordpress-preservation.md) records all 15 Lamat blog paths already present in the archive, the additional route categories to reconcile, and an owner export, private backup, restore and per-route staging workflow. It does not copy article text or media, choose destinations or configure redirects. Compare the table against `apps/web/archive.json` and review the proposed acceptance checks.

The source-of-truth comparison confirms that the 15 listed paths exactly match the 15 `Lamat blog` archive entries, without duplicates. This is a consistency check against an existing snapshot, not a fresh WordPress inventory, link availability check or rights review. A new public-site retrieval was unavailable to the research tool; prior observations are dated in the migration plan.

On 18 November 2026, an authorized administrator exported the WordPress content and media to local private files outside this repository. The content XML parsed successfully and contained 15 post records and 25 attachment records. The media ZIP passed an integrity check, and each attachment URL's filename matched an entry in the ZIP. Filename matching does not prove completeness of every media variant or external embed. The content export also includes form responses and a protected page; do not publish it or commit it here.

Issue #36 remains open: a second owner-controlled backup, restoration test, rights decisions, destination mapping and hosted staging verification are still required. No live routes or content were changed.


## Interactive chart recovery, 18 November 2026

A comparison of published post HTML against exact paths in the media export identified 52 referenced HTML files absent from that ZIP, affecting eight articles. All 52 were retrieved from the existing site into private storage; a private manifest records their source URLs, related articles, sizes and SHA-256 hashes. A second pass matched all 52 local file hashes. These checks establish local byte integrity, not functional restoration, completeness of all dependencies, rights to republish or the existence of an independent backup. Verify the recovered interactive content and any dependencies in an isolated restoration before migration.
