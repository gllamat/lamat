"""Check local HTML links and resources without making network requests."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
import sys


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.references = []
        self.ids = []

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get('id'):
            self.ids.append(attrs['id'])
        if tag == 'a' and attrs.get('name'):
            self.ids.append(attrs['name'])
        for attr in ('href', 'src'):
            if attrs.get(attr):
                self.references.append((tag, attr, attrs[attr]))


def check_site(root):
    """Return diagnostics for static files, local links and HTML fragments.

    Does not check external URLs, scripts/CSS-created URLs, server rewrites,
    HTTP status, redirects, accessibility, or the deployed site.
    """
    root = Path(root).resolve()
    pages = {}
    errors = []
    for path in sorted(root.rglob('*.html')):
        page = Page()
        page.feed(path.read_text(encoding='utf-8'))
        relative = path.relative_to(root).as_posix()
        pages[relative] = page
        for ident, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f'{relative}: duplicate ID or anchor {ident!r}')

    if not pages:
        return [f'{root}: no HTML pages found']

    for source, page in pages.items():
        for tag, attr, reference in page.references:
            split = urlsplit(reference)
            if split.scheme or split.netloc or reference.startswith('//'):
                continue
            target = urlsplit(urljoin('/' + source, reference))
            name = unquote(target.path).lstrip('/') or 'index.html'
            if name.endswith('/'):
                name += 'index.html'
            target_path = (root / name).resolve()
            try:
                target_path.relative_to(root)
            except ValueError:
                errors.append(f'{source}: {attr} {reference!r} escapes site root')
                continue
            if not target_path.is_file():
                errors.append(f'{source}: {attr} {reference!r} points to a missing file')
                continue
            fragment = unquote(target.fragment)
            target_name = target_path.relative_to(root).as_posix()
            if fragment and target_name in pages and fragment not in pages[target_name].ids:
                errors.append(f'{source}: {attr} {reference!r} points to a missing fragment')
            if source == '404.html' and tag != 'a' and not reference.startswith('/'):
                errors.append(f'{source}: {attr} {reference!r} must be root-relative for nested missing URLs')
            if source == '404.html' and tag == 'a' and not (reference.startswith(('/', '#')) or split.scheme or split.netloc):
                errors.append(f'{source}: {attr} {reference!r} must be root-relative for nested missing URLs')
    return errors


def main():
    root = Path(__file__).resolve().parents[1] / 'apps' / 'web'
    errors = check_site(root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        print(f'Site check failed: {len(errors)} error(s)', file=sys.stderr)
        return 1
    print('Static site local link and asset check passed')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
