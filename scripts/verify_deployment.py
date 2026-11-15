"""Verify that live page content exactly matches the deployed source build."""
from concurrent.futures import ThreadPoolExecutor
from hashlib import sha256
from urllib.parse import urljoin, urlencode, quote
import json
import sys
import time
import urllib.request
from content_manifest import inspect

def verify(base, expected):
    base = base.rstrip('/') + '/'
    def fetch(path):
        url = urljoin(base, quote(path.lstrip('/'), safe='/:%?=&'))
        separator = '&' if '?' in url else '?'
        url += separator + urlencode({'_verify': expected, '_time': time.time_ns()})
        request = urllib.request.Request(url, headers={'User-Agent': 'Youzhen-Blog-Content-Check', 'Cache-Control': 'no-cache'})
        with urllib.request.urlopen(request, timeout=20) as response:
            return response.read()

    for attempt in range(1, 13):
        try:
            release = json.loads(fetch('deployment.json'))
            assert release['revision'] == expected, 'Release version is not current yet'
            assert release.get('defaultLanguage') == 'en', 'Default language must be English'
            assert release.get('languages') == ['zh', 'en'], 'Bilingual release missing'
            manifest = json.loads(fetch('content-manifest.json'))
            assert manifest['revision'] == expected, 'Content manifest is from another release'
            def check_page(item):
                route, output = item
                page = inspect(fetch(route).decode('utf-8'))
                assert page.revision == expected, 'Wrong revision: ' + route
                assert page.digest == output['sha256'], 'Live content does not match source build: ' + route
                assert page.language == output['language'], 'Wrong language: ' + route
            with ThreadPoolExecutor(max_workers=6) as pool:
                list(pool.map(check_page, manifest['pages'].items()))
            for route, digest in manifest['files'].items():
                assert sha256(fetch(route)).hexdigest() == digest, 'Search/RSS is out of sync: ' + route
            print(json.dumps({'status': 'PASS', 'revision': expected, 'exact_content_pages': len(manifest['pages']), 'search_and_rss_files': len(manifest['files']), 'languages': ['en', 'zh']}), flush=True)
            return
        except Exception as error:
            if attempt == 12:
                raise SystemExit('Live content verification failed: ' + str(error)) from error
            print(f'Waiting for Pages content sync ({attempt}/12): {error}', flush=True)
            time.sleep(5)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit('Usage: verify_deployment.py BASE_URL COMMIT_SHA')
    verify(sys.argv[1], sys.argv[2])
