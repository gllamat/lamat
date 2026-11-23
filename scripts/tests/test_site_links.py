import tempfile
import unittest
from pathlib import Path

from check_site_links import check_site


class SiteLinkTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / 'assets').mkdir()
        (self.root / 'assets' / 'logo.png').write_bytes(b'fixture')
        (self.root / 'index.html').write_text('<main id="top"></main>', encoding='utf-8')

    def put(self, name, body):
        (self.root / name).write_text(body, encoding='utf-8')

    def test_empty_site_fails(self):
        (self.root / 'index.html').unlink()
        self.assertTrue(any('no HTML pages' in e for e in check_site(self.root)))

    def test_valid_external_and_local_references(self):
        self.put('a.html', '<a href="index.html#top">x</a><img src="/assets/logo.png"><a href="https://example.test/">x</a><a href="mailto:a@example.test">x</a>')
        self.assertEqual(check_site(self.root), [])

    def test_missing_file_fragment_and_duplicate_ids(self):
        self.put('a.html', '<a href="absent.html">x</a><a href="/index.html#bad">x</a><i id="a"></i><i id="a"></i>')
        errors = check_site(self.root)
        self.assertEqual(len(errors), 3)
        self.assertTrue(any('missing file' in e for e in errors))
        self.assertTrue(any('missing fragment' in e for e in errors))
        self.assertTrue(any('duplicate' in e for e in errors))

    def test_not_found_uses_root_relative_assets_and_home(self):
        self.put('404.html', '<img src="assets/logo.png"><a href="index.html">home</a>')
        errors = check_site(self.root)
        self.assertEqual(sum('root-relative' in e for e in errors), 2)
        self.put('404.html', '<img src="/assets/logo.png"><a href="/index.html">home</a><a href="#main">skip</a><main id="main"></main>')
        self.assertEqual(check_site(self.root), [])

    def test_percent_encoded_fragment(self):
        self.put('index.html', '<p id="hello world"></p>')
        self.put('a.html', '<a href="/index.html#hello%20world">x</a>')
        self.assertEqual(check_site(self.root), [])


if __name__ == '__main__':
    unittest.main()
