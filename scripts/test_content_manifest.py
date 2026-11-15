"""Regression coverage for exact source-to-live content verification."""
import unittest
from content_manifest import inspect

PAGE = '<html lang="en-US"><head><title>Notes</title><meta name="blog-revision" content="commit-a"><meta name="blog-built-at" content="time-a"></head><body><nav><a href="/about/">About</a></nav><main><p>Original content</p></main></body></html>'

class ContentFingerprintTests(unittest.TestCase):
    def test_changed_visible_content_is_detected(self):
        for before, after in [('Original content', 'Updated content'), ('<title>Notes', '<title>New Notes'), ('/about/', '/projects/'), ('en-US', 'zh-CN')]:
            with self.subTest(change=before):
                self.assertNotEqual(inspect(PAGE).digest, inspect(PAGE.replace(before, after)).digest)

    def test_build_time_and_revision_are_checked_separately(self):
        changed = PAGE.replace('time-a', 'time-b').replace('commit-a', 'commit-b')
        self.assertEqual(inspect(PAGE).digest, inspect(changed).digest)
        self.assertNotEqual(inspect(PAGE).revision, inspect(changed).revision)

    def test_equivalent_whitespace_does_not_create_false_mismatch(self):
        self.assertEqual(inspect(PAGE).digest, inspect(PAGE.replace('Original content', 'Original    content')).digest)

if __name__ == '__main__':
    unittest.main()
