#!/usr/bin/env python3
"""Build a reproducible Cloudflare Workers static-site upload archive."""
from pathlib import Path
import argparse
import zipfile

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / 'apps' / 'web'
LIMIT = 25 * 1024 * 1024


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('output', type=Path, help='Destination ZIP file')
    args = parser.parse_args()
    required = ('index.html', '404.html', '_redirects')
    for name in required:
        if not (SITE / name).is_file():
            parser.error(f'missing required site file: {name}')
    files = sorted(p for p in SITE.rglob('*') if p.is_file() and p.name != 'vercel.json')
    if len(files) > 20_000:
        parser.error('site exceeds the free plan file limit')
    for path in files:
        if path.stat().st_size > LIMIT:
            parser.error(f'file exceeds 25 MiB: {path.relative_to(SITE)}')
    output = args.output.resolve()
    if output.is_relative_to(SITE):
        parser.error('output must be outside apps/web')
    output.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in files:
            info = zipfile.ZipInfo(path.relative_to(SITE).as_posix(), (1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = 0o100644 << 16
            archive.writestr(info, path.read_bytes(), compresslevel=9)
    print(f'Created {output} with {len(files)} files')


if __name__ == '__main__':
    main()
