# Notes

Youzhen Li 的个人博客，记录 LLMs 与 AI Infrastructure 的学习笔记、论文阅读和工程实践。

- 博客：https://1iyouzhen.github.io/
- **写文章：[添加文章与自动发布](WRITING.md)**
- 直接在 GitHub 的 `content/posts/` 下新建 `<文章英文名>/index.md`，提交到 main 后自动发布。
- 修改文章、图片、导航或样式，同样提交到 main 即自动更新。

## 本地预览

Windows 可运行 `./scripts/bootstrap.ps1` 安装固定版 Hugo，然后运行 `npm run dev`。
`npm run build` 构建到 `public/`，`npm run check` 校验站点。

## 目录

- content/：文章、图片与独立页面
- assets/css/extended/：个性化样式与代码高亮
- layouts/partials/：首页和按需公式加载
- static/：站点图标
- themes/PaperMod/：固定版本 MIT 许可主题
- .github/workflows/publish.yml：main 提交后自动构建与发布
- scripts/：构建、校验与可选的本地发布脚本

## 双语站点 / Bilingual site

- 简体中文：https://1iyouzhen.github.io/
- English：https://1iyouzhen.github.io/en/
- 中文写作说明：[WRITING.md](WRITING.md)
- English authoring guide: [WRITING.en.md](WRITING.en.md)
- index.md 与 index.en.md 分别保存中英文文章；提交 main 后同时自动发布。
- scripts/new_post.py 可一次生成两个语言的文章草稿。
