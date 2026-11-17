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
