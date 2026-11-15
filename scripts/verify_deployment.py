"""Confirm that Pages serves the expected release and its searchable articles."""
from concurrent.futures import ThreadPoolExecutor
from html.parser import HTMLParser
from urllib.parse import urljoin, urlsplit, urlencode
import json
import sys
import time
import urllib.request

class Metadata(HTMLParser):
    def __init__(self):
        super().__init__(); self.revision = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta' and attrs.get('name') == 'blog-revision':
            self.revision = attrs.get('content')

def verify(base, expected):
    base = base.rstrip('/') + '/'
    def fetch(path):
        url = urljoin(base, path)
        separator = '&' if '?' in url else '?'
        url += separator + urlencode({'_verify': expected, '_time': time.time_ns()})
        request = urllib.request.Request(url, headers={'User-Agent': 'Youzhen-Blog-Deployment-Check', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read().decode('utf-8')
    for attempt in range(1, 13):
        try:
            manifest = json.loads(fetch('deployment.json'))
            assert manifest['revision'] == expected, 'Version manifest has not reached the expected commit'
            assert manifest.get('languages') == ['zh', 'en'], 'Bilingual release manifest missing'
            assert manifest.get('defaultLanguage') == 'en', 'English default language missing'
            pages = json.loads(fetch('index.json')) + json.loads(fetch('zh/index.json'))
            routes = ['', 'archives/', 'search/', 'tags/', 'zh/', 'zh/archives/', 'zh/search/', 'zh/tags/']
            routes.extend(urlsplit(row['permalink']).path.lstrip('/') for row in pages)
            routes = list(dict.fromkeys(routes))
            def check_page(route):
                meta = Metadata(); meta.feed(fetch(route))
                assert meta.revision == expected, 'Page is not on the expected commit: ' + route
            with ThreadPoolExecutor(max_workers=4) as pool:
                list(pool.map(check_page, routes))
            print(json.dumps({'status': 'PASS', 'revision': expected, 'verified_routes': routes, 'search_entries': len(pages)}), flush=True)
            return
        except Exception as error:
            if attempt == 12:
                raise SystemExit('Live deployment verification failed: ' + str(error)) from error
            print(f'Waiting for Pages propagation ({attempt}/12): {error}', flush=True)
            time.sleep(5)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: verify_deployment.py BASE_URL COMMIT_SHA')
    verify(sys.argv[1], sys.argv[2])
