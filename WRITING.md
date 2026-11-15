# 写作与维护

## 发布新文章

在 `content/posts/<文章英文短名>/index.md` 新建 Markdown 文件：

```yaml
---
title: 文章标题
date: 2026-11-15T12:00:00+08:00
slug: my-new-post
description: 一句话介绍
summary: 首页显示的摘要
tags: [LLM, 学习笔记]
draft: false
math: false
---
```

正文写在第二个 `---` 后面。图片放在同一目录，使用 `![说明](figure.png)` 引用。不要把整篇正文嵌进配置文件。

修改 Markdown 后，运行 `./scripts/publish.ps1`，脚本会构建、校验、提交并推送源码与静态站点。GitHub Pages 会自动发布 `docs/` 中的产物。若在 GitHub 网页编辑文章，需在本地拉取改动后运行发布脚本。

## 本地预览

安装 Hugo Extended 0.170.0（也可运行 Windows 脚本 `./scripts/bootstrap.ps1`）。主题已随仓库保存，无需克隆子模块。

```powershell
.\.tools\hugo.exe server -D
```

打开终端给出的本地地址。`-D` 只用于本地查看草稿；生产构建不会发布 `draft: true` 的内容。

```powershell
.\.tools\hugo.exe new content posts/my-new-post/index.md
```

## 公式、代码和目录

文章设置 `math: true` 即按需加载固定版本 MathJax 3.2.2。行内公式用 `$...$`，独立公式用 `$$...$$`；公式显示需要读者能访问 jsDelivr。普通页面不依赖外部字体或 JavaScript CDN。代码块在三个反引号后写语言，例如 `python`。二、三级标题自动生成文章目录。

## 配置入口

- `hugo.toml`：站点名称、导航、社交链接、简介。
- `content/about.md`：关于页面。
- `content/projects.md`：项目页面。
- `assets/css/extended/custom.css`：个性化样式。
- `versions.json`：固定的 Hugo 版本和 PaperMod 源码版本。

## 构建与部署

运行 `./scripts/build.ps1` 或 `npm run build` 构建；运行 `npm run check` 检查页面、链接与草稿隔离。

`docs/` 是实际发布产物，由 Hugo 生成。GitHub Pages 从 `main` 分支的 `/docs` 目录发布。首次发布的静态文件随源码提交，后续通过 `scripts/publish.ps1` 更新。不要手动编辑 `docs/`。

主题来自 MIT 许可的 PaperMod，保留在 `themes/PaperMod/LICENSE`。文章内容版权归各自作者所有，引用资料以其原始许可为准。

发布脚本会先检查工作区状态；请先提交或暂存无关的改动，保持 main 分支且不混入其他文件。站点中英文介绍可按需要自行修改。
