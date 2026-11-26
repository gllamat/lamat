import json
import unittest
from pathlib import Path
from urllib.parse import urlsplit

WEB = Path(__file__).resolve().parents[2] / 'apps' / 'web'


class HistoricalRouteTests(unittest.TestCase):
    def test_redirects_are_unique_and_local_destinations_exist(self):
        routes = json.loads((WEB / 'vercel.json').read_text())['redirects']
        sources = [route['source'] for route in routes]
        self.assertEqual(len(sources), len(set(sources)))
        for route in routes:
            destination = route['destination']
            if not urlsplit(destination).scheme:
                self.assertTrue((WEB / destination.lstrip('/')).is_file(), destination)

    def test_both_legacy_article_url_forms_resolve_equally(self):
        routes = json.loads((WEB / 'vercel.json').read_text())['redirects']
        destinations = {route['source']: route['destination'] for route in routes}
        articles = [source for source in destinations if source.startswith('/20') and not source.endswith('/')]
        self.assertEqual(len(articles), 15)
        for source in articles:
            self.assertEqual(destinations[source], destinations.get(source + '/'), source)


if __name__ == '__main__':
    unittest.main()
