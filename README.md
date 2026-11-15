# Notes

Youzhen Li’s personal blog about LLMs and AI infrastructure.

- English (default): https://1iyouzhen.github.io/
- 简体中文：https://1iyouzhen.github.io/zh/
- English guide: [WRITING.en.md](WRITING.en.md)
- 中文写作说明：[WRITING.md](WRITING.md)

Click the language button in the header to choose English or 简体中文. Article pages link to the matching translation.

## Article source

Keep paired files together: content/posts/my-article/index.en.md and content/posts/my-article/index.zh.md. Use the same slug and maintain each translation independently. Commit to main to automatically publish both language editions.

Generate both drafts locally with scripts/new_post.py. Interface translations live in i18n/en.toml and i18n/zh.toml; language settings and menus live in hugo.toml.

## Local preview

Run ./scripts/bootstrap.ps1 to install the pinned Hugo version, then npm run dev. Use npm run build and npm run check to validate the generated site. GitHub Actions builds and deploys source changes automatically.

The site uses Hugo and the MIT-licensed PaperMod theme. Articles remain the property of their authors.
