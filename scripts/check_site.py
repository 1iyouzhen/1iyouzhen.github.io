from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import csv
import io
import json
import os
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

SOURCE = Path(__file__).resolve().parent.parent
ROOT = (SOURCE / (sys.argv[1] if len(sys.argv) > 1 else 'public')).resolve()
BASE = '1iyouzhen.github.io'
REQUIRED = ['index.html', 'about/index.html', 'projects/index.html', 'archives/index.html', 'search/index.html', 'tags/index.html', 'index.xml', 'index.json', 'sitemap.xml', 'robots.txt', 'favicon.svg', '.nojekyll', 'deployment.json']

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.refs = []; self.ids = set(); self.title = False; self.in_title = False; self.canonical = False
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.add(attrs['id'])
        if tag == 'title': self.in_title = True
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = True
        for key in ('href', 'src'):
            if key in attrs: self.refs.append(attrs[key])
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title and data.strip(): self.title = True

errors = []
for path in REQUIRED:
    if not (ROOT / path).is_file(): errors.append('Missing required file: ' + path)
cache = {}
for path in ROOT.rglob('*.html'):
    page = Page(); page.feed(path.read_text(encoding='utf-8')); cache[path.resolve()] = page
    if not page.title: errors.append('Missing title: ' + str(path))
    if path.name != '404.html' and not page.canonical: errors.append('Missing canonical: ' + str(path))
for path, page in cache.items():
    for ref in page.refs:
        url = urlsplit(ref)
        if url.scheme and url.scheme not in ('http', 'https'): continue
        if url.netloc and url.netloc != BASE: continue
        part = unquote(url.path)
        target = (ROOT / part.lstrip('/')) if part.startswith('/') else (path.parent / part)
        if not part: target = path
        if target.is_dir(): target = target / 'index.html'
        target = target.resolve()
        if not target.exists(): errors.append(f'Broken local link in {path.relative_to(ROOT)}: {ref}')
        elif url.fragment and target.suffix == '.html':
            dest = cache.get(target)
            if dest and unquote(url.fragment) not in dest.ids: errors.append(f'Broken anchor in {path.relative_to(ROOT)}: {ref}')

indexes = {prefix: json.loads((ROOT / prefix / 'index.json').read_text(encoding='utf-8')) for prefix in ('', 'en')}
index = [entry for entries in indexes.values() for entry in entries]
for prefix in ('', 'en'):
    for route in ('index.html', 'about/index.html', 'projects/index.html', 'archives/index.html', 'search/index.html', 'tags/index.html', 'index.xml', '404.html'):
        if not (ROOT / prefix / route).is_file(): errors.append('Missing bilingual route: ' + prefix + '/' + route)
    for entry in indexes[prefix]:
        path = urlsplit(entry['permalink']).path
        if path.startswith('/en/') != (prefix == 'en'): errors.append('Language leaked into search index: ' + entry['permalink'])
    ET.parse(ROOT / prefix / 'index.xml')
local_hugo = SOURCE / '.tools/hugo.exe'
hugo = os.environ.get('HUGO_EXE') or shutil.which('hugo') or (str(local_hugo) if local_hugo.is_file() else None)
assert hugo, 'Hugo executable is required for publication validation'
def manifest(kind):
    result = subprocess.run([hugo, 'list', kind], cwd=SOURCE, check=True, capture_output=True, encoding='utf-8-sig')
    return list(csv.DictReader(io.StringIO(result.stdout)))
all_pages = [row for row in manifest('all') if row['kind'] == 'page']
published = [row for row in manifest('published') if row['kind'] == 'page']
urls = [row['permalink'] for row in all_pages]
assert len(urls) == len(set(urls)), 'Duplicate article URLs: assign each article a unique slug'
published_urls = {row['permalink'] for row in published}
search_urls = {row['permalink'] for row in index}
for row in published:
    if row['section'] != 'posts': continue
    relative = unquote(urlsplit(row['permalink']).path).lstrip('/')
    if not (ROOT / relative / 'index.html').is_file(): errors.append('Published article missing: ' + row['path'])
    if row['permalink'] not in search_urls: errors.append('Published article missing from search: ' + row['path'])
for row in all_pages:
    if row['permalink'] in published_urls: continue
    relative = unquote(urlsplit(row['permalink']).path).lstrip('/')
    if (ROOT / relative / 'index.html').exists(): errors.append('Unpublished article leaked into site: ' + row['path'])
    if row['permalink'] in search_urls: errors.append('Unpublished article leaked into search: ' + row['path'])
release = json.loads((ROOT / 'deployment.json').read_text(encoding='utf-8'))
expected = os.environ.get('HUGO_DEPLOY_COMMIT')
if expected: assert release.get('revision') == expected, 'Wrong build revision'
assert release.get('languages') == ['zh', 'en'], 'Bilingual deployment manifest missing'
ET.parse(ROOT / 'index.xml'); ET.parse(ROOT / 'sitemap.xml')
assert len(errors) == 0, chr(10).join(errors)
print(f'PASS: {len(cache)} HTML pages, {len(index)} search entries, both languages, required routes, internal links, RSS, sitemap and draft isolation.')
