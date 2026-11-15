"""Create stable hashes of rendered page content for deployment verification."""
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
import argparse
import json

class PageContent(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tokens = []
        self.skip = 0
        self.revision = None
        self.language = None
        self.title_parts = []
        self.in_title = False
        self.redirect = False

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ('script', 'style', 'noscript'):
            self.skip += 1
            return
        if self.skip:
            return
        if tag == 'meta':
            name = attrs.get('name', '')
            if name == 'blog-revision': self.revision = attrs.get('content')
            if attrs.get('http-equiv', '').lower() == 'refresh': self.redirect = True
            if name in ('blog-built-at', 'blog-revision'):
                return
        if tag == 'html': self.language = attrs.get('lang')
        if tag == 'title': self.in_title = True
        # Script/style fingerprints are deliberately excluded; content and
        # navigation changes remain covered even if the build time differs.
        if tag == 'link' and any(kind in attrs.get('rel', '').split() for kind in ('preload', 'stylesheet')):
            return
        self.tokens.append(['open', tag, sorted(attrs.items())])

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)

    def handle_endtag(self, tag):
        if tag in ('script', 'style', 'noscript'):
            self.skip = max(0, self.skip - 1)
            return
        if self.skip:
            return
        if tag == 'title': self.in_title = False
        self.tokens.append(['close', tag])

    def handle_data(self, text):
        if self.skip:
            return
        value = ' '.join(text.split())
        if value:
            self.tokens.append(['text', value])
            if self.in_title: self.title_parts.append(value)

    @property
    def digest(self):
        payload = json.dumps(self.tokens, ensure_ascii=False, separators=(',', ':'))
        return sha256(payload.encode('utf-8')).hexdigest()

def inspect(html):
    page = PageContent()
    page.feed(html)
    return page

def generate(destination):
    root = Path(destination).resolve()
    release = json.loads((root / 'deployment.json').read_text(encoding='utf-8'))
    pages = {}
    for path in sorted(root.rglob('*.html')):
        page = inspect(path.read_text(encoding='utf-8'))
        if page.revision is None:
            continue  # Hugo alias pages contain a redirect rather than article content.
        assert page.revision == release['revision'], 'Mixed release in output: ' + str(path)
        relative = path.relative_to(root).as_posix()
        route = '/' + relative[:-10] if relative.endswith('index.html') else '/' + relative
        pages[route] = {'sha256': page.digest, 'title': ' '.join(page.title_parts), 'language': page.language}
    files = {}
    for prefix in ('', 'zh/'):
        for name in ('index.json', 'index.xml'):
            path = root / prefix / name
            files['/' + prefix + name] = sha256(path.read_bytes()).hexdigest()
    manifest = {'schema': 1, 'revision': release['revision'], 'pages': pages, 'files': files}
    (root / 'content-manifest.json').write_text(json.dumps(manifest, ensure_ascii=False, separators=(',', ':')), encoding='utf-8')
    print(f'Content manifest: {len(pages)} page fingerprints and {len(files)} search/RSS fingerprints.')
    return manifest

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destination', nargs='?', default='public')
    generate(parser.parse_args().destination)
