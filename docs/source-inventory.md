# Public source inventory

This inventory distinguishes historical publications and code from current work. The [website archive](../apps/web/archive.html) lists the indexed material in reverse chronological order; [archive.json](../apps/web/archive.json) is its editable source of metadata.

## Coverage

- **Medium:** 30 article cards, dates and links extracted from the author's saved profile page. The saved page may not include every publication; some full articles were inaccessible. Medium's public feed returned the ten most recent items, and its sitemap was incomplete. A catalog entry is not evidence of a full-text review.
- **Lamat blog:** seven entries visible on the existing blog archive, including some topics also published on Medium. These are separate source links, with their own displayed dates.
- **Notebooks:** five reviewed gists: three under `gllamat` and the two earlier `gjlr2000` QTrader examples. Dates are the latest revisions inspected, not necessarily first-publication dates.
- **Repositories:** the earlier MeanReversion and Intelligence-Amplification repositories, dated by repository creation. Historical APIs and dependencies must be checked before reuse.

## Technical review of the historical notebooks

The 2018 QTrader notebook teaches tabular Q-learning in a simulated market with discrete prices, holdings, actions and costs. The related DeepQ notebook replaces the table with a Keras neural approximation; it uses older library APIs. Neither example has been reproduced here. Modern work should separate simulation, agent, reward and evaluation, and use seeded experiments and out-of-sample comparisons.

The three 2021 gists explore character-level LSTM education, Reddit data collection and named-entity recognition, and VADER sentiment in finance. The authors' examples highlight ambiguity and domain mismatch. A rewrite should respect current source access terms, assess datasets and labels, and evaluate false positives and false negatives.

The original mean-reversion notebooks and rate-clustering work provide background for the new reusable research module. Their old API services are obsolete, as confirmed by the owner; historical keys must not be copied. The new library currently uses synthetic data only.

## Editorial notes

Links point to original publications rather than republishing the text. Coauthored work and publication dates should retain their attribution. The saved Medium profile truncates at least one title; check the original before editorial use. The archive is a documented starting inventory, not a claim that every post or source has been discovered.


## Reconciliation and outstanding sources

Checked 17 November 2026 against the saved Medium profile and the earlier local research inventory. `archive.json` contains 44 distinct links: 30 Medium articles, seven Lamat blog entries, five historical notebooks and two historical repositories. The 42 article and notebook entries in the review correspond to entries in the archive. One uses a different link for the same Medium article identifier: [Giving a Worm’s Brain to a Trading Robot](https://medium.datadriveninvestor.com/giving-a-worms-brain-to-a-trading-robot-d55abccb4e8b) was also listed under the author’s Medium domain. This link reconciliation does not prove every link or article body was independently checked.

- The saved Medium profile is a snapshot, not an account export. Compare it with an author export or another complete publication list if available; additional articles may be missing.
- Some article bodies were inaccessible during the original review; individual full-text access was not recorded systematically. Treat entries as metadata-only unless a separate full-text review is documented.
- Confirm the full title of the truncated 18 April 2023 Mini DAO article and verify credits and rights before republishing. Known coauthors appear in archive previews where visible; check originals for other contributors.
- The seven Lamat blog links reflect the archive observed earlier. The blog archive was inaccessible to the research tool on 17 November 2026; additional pages and full-text access remain unverified.
- Notebook source and narrative were reviewed, but notebooks were not executed. Original publication dates and data availability remain unverified. The two `gjlr2000` links were supplied by the owner.
- Keep publication dates distinct from notebook revision dates. Preserve separate Medium and Lamat versions until content and attribution have been compared.
