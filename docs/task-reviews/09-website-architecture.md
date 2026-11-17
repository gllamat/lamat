# Task 9: website information architecture — review record

**Status:** Ready for review. **Board task:** [Website information architecture](https://github.com/gllamat/lamat/issues/9).

## Preview and review

Open [the homepage](../../apps/web/index.html) and [historical archive](../../apps/web/archive.html) in a browser, or run `python3 -m http.server 8765 --directory apps/web` from the repository root and visit `http://127.0.0.1:8765/`. The website is a local preview.

The homepage introduces finance research and AI consulting, explains the approach, links the historical archive, and includes About and Contact sections. The same navigation appears on the archive page: Home, Work & Services, Approach, Historical Archive, About and Contact. The supplied transparent logo is used in the header and footer; the contact links use the owner-supplied address. The archive continues to distinguish dates of publication from notebook/repository creation and preserves its 52 sources.

## Checks

- Opened the home page and followed the Historical Archive navigation in a browser; inspected the desktop home layout and the accessibility tree.
- At a 375-pixel viewport, checked home and archive document widths (375 pixels with no horizontal overflow) and confirmed all 52 archive entries are present.
- Regenerated the archive from `apps/web/archive.json`, checked local navigation targets and ran the Python research tests.
- Added a skip link and visible keyboard focus styles. This is not a full accessibility audit or a substitute for screen-reader and keyboard review on multiple devices.

## Boundaries for human review

The finance research and AI consulting text expresses the agreed focus; specific current projects, client names and detailed services still require owner confirmation. About copy is intentionally limited to the project brief. The logo colours are sampled from the supplied image; original specifications and higher-resolution artwork remain outstanding. Medium access, some archive attribution, migration, redirects, hosting and comprehensive accessibility checks remain separate follow-up work. No deployment or domain changes are part of this task.
