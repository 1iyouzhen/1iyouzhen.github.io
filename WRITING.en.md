# Writing and Publishing

English is the default edition at https://1iyouzhen.github.io/ . Simplified Chinese is available at https://1iyouzhen.github.io/zh/ . The former /en/ addresses redirect to their English counterparts at the root.

The language button shows the current language. Click it to reveal English and 简体中文, then choose a language. Article pages switch to the matching translation. When no published translation exists, the switch opens the destination language home page.

## Add an article on GitHub

Open content/posts in the repository, select Add file → Create new file, and use a unique article directory:

```text
content/posts/my-article/
  index.en.md    # English, the default edition
  index.zh.md    # Simplified Chinese
  images/        # Images for this article, shared by both languages
    architecture.png
    result.jpg
```

Keep the same slug in both versions. Translate the title, description, summary, tags, categories, and body. Each language has an independent draft flag. Translations are maintained as source Markdown; editing one version does not automatically translate the other.

Keep every article in its own folder with index.en.md, index.zh.md, and an images/ subdirectory. Explicit language suffixes are recommended. A file without a language suffix, such as index.md, belongs to the default English edition.

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

Keep all article images inside that article’s images/ folder. Use a relative path such as ![System architecture](images/architecture.png). Both translations share the image file; translate the description separately.


### Upload article images on GitHub

1. Open content/posts/my-article/images/ and choose Add file → Upload files.
2. Upload this article’s images and commit to main.
3. Reference the image in the article body:

```markdown
![System architecture](images/architecture.png)
```

Use the same path in both language files. Choose simple filenames and match their exact capitalization. Do not use local disk paths or upload authoring images into public/.

### Article cover

Add this to the article’s YAML front matter between the two --- delimiters:

```yaml
cover:
  image: images/architecture.png
  alt: System architecture
```

Keep the image path identical in both languages and translate alt. Commit the changes to publish the body images and cover automatically. Different articles can use identical image filenames without collisions because their folders are separate.

## Create both drafts locally

```powershell
python scripts/new_post.py my-article --title-zh 中文标题 --title-en EnglishTitle
```

This creates an article folder containing index.zh.md, index.en.md, and images/, with matching slugs and draft status. images/.gitkeep keeps an otherwise empty image directory visible on GitHub. Existing directories are never overwritten. Install the pinned Hugo version with ./scripts/bootstrap.ps1 and run npm run dev for local preview.

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


## Source-to-website content verification

The site name is Notes, matching your earlier repository title change. The actual site title is configured in hugo.toml and the two language home metadata files, content/_index.en.md and content/_index.zh.md. README is a repository description rather than a rendered blog page.

The obsolete docs snapshot has been removed from the tracked repository. Edit Markdown under content/, not generated HTML.

Automatic deployment now verifies exact rendered content, including titles, text, navigation, links, both search indexes, and both RSS feeds. A matching commit label alone is no longer sufficient for a successful content check. English and Chinese Markdown translations remain independent editable source documents.
