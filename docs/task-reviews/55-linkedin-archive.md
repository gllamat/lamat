# LinkedIn historical archive review

The owner supplied a LinkedIn account export. Its Articles folder contains 33 HTML files: 30 identify a publication date and a LinkedIn article URL, while three do not identify both and are excluded from the public archive. Only public article titles, publication dates and original LinkedIn URLs are used here. The account export and article copies are kept privately; no drafts, contacts, messages or other account information belong in this repository.

The archive adds 28 dated LinkedIn entries. Two articles with substantial apparent overlap with existing Medium entries are represented as related LinkedIn links alongside those entries, preserving both source URLs without duplicating a primary listing. Similarity does not establish complete equivalence of text, dates, images or rights.

The original URLs come from the export; LinkedIn availability, login restrictions and redirects have not been verified for every link. Exported article pages can reference external images, documents and embeds; the article files alone do not preserve those dependencies. Review their provenance, availability and rights, complete the WordPress/Medium comparison, and verify the deployed archive before closing issue #55. Historical examples and product announcements are dated sources, not claims that their products or data are current.

Rebuild with `python3 scripts/build_archive.py`. The archive generator escapes text and link attributes when rendering the JSON entries.
