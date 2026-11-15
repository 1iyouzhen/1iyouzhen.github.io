# Writing and Publishing

English is the default edition at https://1iyouzhen.github.io/ . Simplified Chinese is available at https://1iyouzhen.github.io/zh/ . The former /en/ addresses redirect to their English counterparts at the root.

The language button shows the current language. Click it to reveal English and 简体中文, then choose a language. Article pages switch to the matching translation. When no published translation exists, the switch opens the destination language home page.

## Add an article on GitHub

Open content/posts in the repository, select Add file → Create new file, and use a unique article directory:

```text
content/posts/my-article/
  index.en.md    # English, the default edition
  index.zh.md    # Simplified Chinese
  figure.png     # Shared image
```

Keep the same slug in both versions. Translate the title, description, summary, tags, categories, and body. Each language has an independent draft flag. Translations are maintained as source Markdown; editing one version does not automatically translate the other.

Explicit .en.md and .zh.md suffixes are recommended. A file without a language suffix, such as index.md, belongs to the default English edition. Standalone files such as my-article.en.md and my-article.zh.md also work.

## Article template

Save the English version as content/posts/my-article/index.en.md:

```markdown
---
title: My Article
date: 2026-11-15T08:00:00+08:00
slug: my-article
description: A one-line introduction.
summary: The summary shown in article lists.
tags: [LLM, Learning Notes]
draft: false
math: false
---

Start writing here.

## First section

Article content.
```

Set draft: false and commit to main when ready. Actions → Publish blog builds, validates, publishes, and checks both live editions. Set an unfinished translation to draft: true. Use a real publication time in the past or present; future publication is not automatically scheduled.

## Links and images

The English article URL is /posts/my-article/; Chinese uses /zh/posts/my-article/. English internal links use /archives/, /search/, and /tags/. Chinese uses /zh/archives/, /zh/search/, and /zh/tags/.

Put images beside the two files and use relative links such as ![Description](figure.png). The same image is available to both versions.

## Create both drafts locally

```powershell
python scripts/new_post.py my-article --title-zh 中文标题 --title-en EnglishTitle
```

This creates index.zh.md and index.en.md with matching slugs and draft status. Existing directories are never overwritten. Install the pinned Hugo version with ./scripts/bootstrap.ps1 and run npm run dev for local preview.

Publish source edits by committing and pushing to main, or use ./scripts/publish.ps1 to build and validate locally before pushing.

## Site configuration

- hugo.toml: default language, translated menus, descriptions, and home headings.
- i18n/en.toml and i18n/zh.toml: interface controls and messages.
- content/about.en.md and content/about.zh.md: about pages.
- content/projects.en.md and content/projects.zh.md: project pages.
- .github/workflows/publish.yml: automatic publishing.

README.md describes the GitHub repository; it is not a website page. Do not edit generated HTML in public/ or the old docs/ snapshot. Search, archives, tags, and RSS are independent for each language.

## Updates

Check Actions → Publish blog for progress. The footer shows the current revision and provides Check for updates. Open pages also check for newer releases. A page cached before this interface update may need one hard refresh with Ctrl+Shift+R.

Set math: true for mathematical expressions. Syntax highlighting, article contents, and code copying are supported in both editions.
