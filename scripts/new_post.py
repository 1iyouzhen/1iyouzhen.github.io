"""Create paired Chinese and English Hugo article drafts."""
import argparse
from datetime import datetime, timedelta, timezone
import json
from pathlib import Path
import re


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('slug', help='Unique URL slug, for example kv-cache-notes')
    parser.add_argument('--title-zh', required=True)
    parser.add_argument('--title-en', required=True)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
        parser.error('Use lowercase letters, digits, and single hyphens for the slug.')
    root = Path(__file__).resolve().parent.parent
    bundle = root / 'content' / 'posts' / args.slug
    if bundle.exists():
        parser.error('Article directory already exists; no existing files were changed.')
    stamp = datetime.now(timezone(timedelta(hours=8))).isoformat(timespec='seconds')

    def document(title, english):
        lines = ['---', 'title: ' + json.dumps(title, ensure_ascii=False),
                 'date: ' + stamp, 'slug: ' + args.slug, 'description: ""',
                 'summary: ""', 'tags: []', 'categories: []',
                 'draft: true', 'math: false', '---', '']
        headings = ['Problem', 'Core idea', 'Details and verification', 'References'] if english else ['问题', '核心思路', '细节与验证', '参考资料']
        for heading in headings:
            lines.extend(['## ' + heading, '', ''])
        return chr(10).join(lines)

    bundle.mkdir(parents=True)
    (bundle / 'index.zh.md').write_text(document(args.title_zh, False), encoding='utf-8')
    (bundle / 'index.en.md').write_text(document(args.title_en, True), encoding='utf-8')
    print('Created: ' + str(bundle / 'index.zh.md'))
    print('Created: ' + str(bundle / 'index.en.md'))
    print('Both versions are drafts. Set draft: false when each version is ready.')


if __name__ == '__main__':
    main()
