# Task 36: preservation inventory review

The [worklist](../wordpress-preservation.md) records all 15 Lamat blog paths already present in the archive, the additional route categories to reconcile, and an owner export, private backup, restore and per-route staging workflow. It does not copy article text or media, choose destinations or configure redirects. Compare the table against `apps/web/archive.json` and review the proposed acceptance checks.

The source-of-truth comparison confirms that the 15 listed paths exactly match the 15 `Lamat blog` archive entries, without duplicates. This is a consistency check against an existing snapshot, not a fresh WordPress inventory, link availability check or rights review. A new public-site retrieval was unavailable to the research tool; prior observations are dated in the migration plan.

On 18 November 2026, an authorized administrator exported the WordPress content and media to local private files outside this repository. The content XML parsed successfully and contained 15 post records and 25 attachment records. The media ZIP passed an integrity check, and each attachment URL's filename matched an entry in the ZIP. Filename matching does not prove completeness of every media variant or external embed. The content export also includes form responses and a protected page; do not publish it or commit it here.

Issue #36 remains open: a second owner-controlled backup, restoration test, rights decisions, destination mapping and hosted staging verification are still required. No live routes or content were changed.
