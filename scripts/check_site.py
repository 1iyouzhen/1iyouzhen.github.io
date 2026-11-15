from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent / 'docs'
BASE = '1iyouzhen.github.io'
REQUIRED = ['index.html', 'about/index.html', 'projects/index.html', 'archives/index.html', 'search/index.html', 'tags/index.html', 'posts/hello-world/index.html', 'posts/learning-map/index.html', 'index.xml', 'index.json', 'sitemap.xml', 'robots.txt', 'favicon.svg', '.nojekyll']
class Page(HTMLParser):
    def __init__(self):
        super().__init__(); self.refs = []; self.ids = set(); self.title = False; self.in_title = False; self.canonical = False
    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if 'id' in a: self.ids.add(a['id'])
        if tag == 'title': self.in_title = True
        if tag == 'link' and a.get('rel') == 'canonical': self.canonical = True
        for k in ('href', 'src'):
            if k in a: self.refs.append(a[k])
    def handle_endtag(self, tag):
        if tag == 'title': self.in_title = False
    def handle_data(self, data):
        if self.in_title and data.strip(): self.title = True

errors = []
for path in REQUIRED:
    if not (ROOT / path).is_file(): errors.append('Missing required file: ' + path)
cache = {}
for path in ROOT.rglob('*.html'):
    p = Page(); p.feed(path.read_text(encoding='utf-8')); cache[path.resolve()] = p
    if not p.title: errors.append('Missing title: ' + str(path))
    if path.name != '404.html' and not p.canonical: errors.append('Missing canonical: ' + str(path))
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
index = json.loads((ROOT / 'index.json').read_text(encoding='utf-8'))
assert any('开始记录' in row['title'] for row in index), 'Welcome post missing from search index'
assert any('学习导航' in row['title'] for row in index), 'Learning map missing from search index'
assert not any('inference-notes' in row.get('permalink', '') for row in index), 'Draft leaked into search'
assert not (ROOT / 'posts/inference-notes').exists(), 'Draft leaked into production'
ET.parse(ROOT / 'index.xml'); ET.parse(ROOT / 'sitemap.xml')
assert len(errors) == 0, '\n'.join(errors)
print(f'PASS: {len(cache)} HTML pages, {len(index)} search entries, required routes, internal links, RSS, sitemap and draft isolation.')
