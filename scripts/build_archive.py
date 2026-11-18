"""Build the static historical archive from reviewed public-source metadata."""
import datetime
import html
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
data = json.loads((root / 'apps/web/archive.json').read_text())
assert data == sorted(data, key=lambda a: (a['date'], a['title']), reverse=True)
esc = html.escape
parts = ['''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="Historical research and writing from Lamat."><title>Historical archive — Lamat</title><link rel="stylesheet" href="style.css"></head>
<body><a class="skip-link" href="#main">Skip to content</a><header class="site-header wrap"><a class="brand" href="index.html" aria-label="Lamat home"><img src="assets/lamat-logo-transparent.png" alt="" width="42" height="42"><span>LAMAT<small>DATA SCIENCE APPLIED TO FINANCE</small></span></a><nav aria-label="Main navigation"><a href="index.html">Home</a><a href="index.html#work">Work &amp; Services</a><a href="index.html#approach">Approach</a><a href="archive.html" aria-current="page">Historical Archive</a><a href="index.html#about">About</a><a class="nav-contact" href="index.html#contact">Contact</a></nav></header>
<main id="main" class="wrap archive-main"><div class="archive-hero"><p class="eyebrow">RESEARCH &amp; WRITING &nbsp; / &nbsp; HISTORICAL ARCHIVE</p><h1>Ideas over <em>time.</em></h1><p>Articles, talks and code from earlier work, listed by date. These are historical sources, not claims about current products or results.</p><p class="archive-note">Dates are original publication dates where available; notebooks and repositories are dated by creation; publication and revision dates may differ. Some topics appear more than once where they were published on different platforms.</p></div><div class="archive-list">''']
year = None
for a in data:
    date = datetime.date.fromisoformat(a['date'])
    if date.year != year:
        if year is not None:
            parts.append('</div></section>')
        year = date.year
        parts.append(f'<section id="archive-{year}" class="archive-year"><h2>{year}</h2><div>')
    related = ''.join(
        f'<a href="{esc(link["url"], quote=True)}">{esc(link["label"])}</a>'
        for link in a.get('related_links', [])
    )
    related = f'<div class="archive-related">{related}</div>' if related else ''
    parts.append(f'''<article class="archive-item"><div><time datetime="{date.isoformat()}">{date.strftime('%d %b %Y')}</time><span>{esc(a['date_note'])} · {esc(a['kind'])}</span></div><a href="{esc(a['url'], quote=True)}">{esc(a['title'])}<span aria-hidden="true">↗</span></a>{related}</article>''')
if year is not None:
    parts.append('</div></section>')
parts.append('''</div></main><footer><div class="wrap footer-inner"><div><a class="brand" href="index.html"><img src="assets/lamat-logo-transparent.png" alt="" width="35" height="35"><span>LAMAT</span></a><p>Data science applied to finance.</p></div><div><span>BEGINNINGS &amp; GROWTH</span><a href="mailto:contact@lamat-qanil.com">Get in touch ↗</a></div></div></footer></body></html>''')
(root/'apps/web/archive.html').write_text('\n'.join(parts)+'\n')
print(f'Built archive with {len(data)} entries')
