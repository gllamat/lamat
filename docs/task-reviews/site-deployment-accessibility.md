# Site deployment accessibility check

The homepage and archive use smooth scrolling for in-page navigation. Visitors who request reduced motion now receive immediate scrolling instead. The default experience remains unchanged.

A local HTML inspection found no duplicate IDs or missing relative page, asset or fragment targets in either page. This checks repository-local references only; it does not verify external article destinations, contact delivery, deployed routes, contrast, screen-reader behavior or a hosted staging environment. Those checks remain in the [migration plan](../site-migration-plan.md).

Review the stylesheet's `prefers-reduced-motion` rule and verify anchor navigation with the browser's reduced-motion preference enabled and disabled during the hosted staging review.
