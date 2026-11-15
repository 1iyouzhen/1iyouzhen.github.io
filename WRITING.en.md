# Writing and Publishing

The blog has two editions: Simplified Chinese at `https://1iyouzhen.github.io/` and English at `https://1iyouzhen.github.io/en/`. Use the language switch beside the site title to open the matching translation. If a translation is not published, the switch opens the destination language’s home page. Search, RSS, archives, and tags are independent for each language.

## Add an article on GitHub

1. Open `content/posts` in the repository and select **Add file → Create new file**.
2. Name the Chinese file `my-article/index.md`, or the English file `my-article/index.en.md`.
3. Paste the template below and write the article after the closing `---`.
4. Set `draft: false` when ready and commit to `main`.
5. Wait for **Actions → Publish blog** to finish. It builds, validates, publishes, and checks the live pages for both languages.

```markdown
---
title: "My Article"
date: 2026-11-15T08:00:00+08:00
slug: my-article
description: "A one-line introduction."
summary: "The summary shown in article lists."
tags: [LLM, Learning Notes]
draft: false
math: false
---

Start writing here.

## First section

Article content.
```

Use a real publication time in the past or present. Future-dated articles are excluded until a later build; publication is not scheduled automatically.

## Maintain both source versions

```text
content/posts/my-article/
  index.md       # Simplified Chinese
  index.en.md    # English
  figure.png     # Shared image
```

Both versions use the same slug. Translate the title, description, summary, tags, categories, and body. Each has its own draft flag. Keep unfinished translations as `draft: true`.

Translations are editable Markdown source files. Changing one language does not automatically translate the other; update both files to keep them in sync. No translation API or key is required.

For standalone files, `tset.md` and `tset.en.md` are also a translation pair. File names must match after removing `.en`.

Use `/en/` for English internal links, such as `[Archive](/en/archives/)`. Put images beside both files and reference them with `![Description](figure.png)`.

## Create both drafts locally

```powershell
python scripts/new_post.py kv-cache-notes --title-zh "KV Cache 学习笔记" --title-en "KV Cache Notes"
```

This creates both files with matching slugs and draft status. Existing directories are never overwritten.

For local preview, install the pinned Hugo version with `./scripts/bootstrap.ps1`, then run `npm run dev`. Publish by committing source changes and pushing to main. You may also use `./scripts/publish.ps1` to build and validate before pushing.

## Translate the site interface

- `hugo.toml`: language menus, names, descriptions, and home headings.
- `i18n/zh.toml` and `i18n/en.toml`: controls and messages.
- `content/about.md` and `content/about.en.md`: about pages.
- `content/projects.md` and `content/projects.en.md`: project pages.
- `.github/workflows/publish.yml`: automatic publishing.

`README.md` describes the GitHub repository; it is not a blog page. Generated files in `public/` do not need to be committed.

## Updates and troubleshooting

Check **Actions → Publish blog** for progress. The footer shows the source revision and includes **Check for updates**. Open pages also check for newer releases. An old cached page may need one hard refresh with Ctrl+Shift+R.

Article addresses follow the slug, not necessarily the source filename. `/posts/my-article/` has the English counterpart `/en/posts/my-article/`.

Set `math: true` to enable MathJax for an article. Code highlighting, article contents, and copy controls are available in both editions.
