# Task 39 review: DNS cutover and rollback

Review [the cutover runbook](../site-cutover-rollback.md), especially the provider-specific differences, required owner evidence, pre-cutover gates and rollback sequence. A public recursive DNS observation is explicitly time-limited and cannot replace a full zone export or prove domain ownership. The plan references current provider documentation and does not prescribe destination DNS values.

The task is **not complete**: the owner must confirm access and account details, export and protect the zone, select the host, approve the plan and thresholds, and rehearse restoration and rollback. No production DNS, hosting or content was changed. Article preservation and staging are tracked separately in #36 and #38.
