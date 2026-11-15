# 添加文章与自动发布

## 最简单：直接在 GitHub 网页写

1. 打开仓库 https://github.com/1iyouzhen/1iyouzhen.github.io ，进入 `content/posts`。
2. 选择 **Add file → Create new file**。文件名填写 `my-first-post/index.md`，每篇文章换一个英文目录名。
3. 粘贴下方模板，将标题、日期、摘要、标签、正文改成自己的内容。日期请填写当前或过去的时间。
4. 点击 **Commit changes**，选择直接提交到 **main**。
5. 在仓库 **Actions → Publish blog** 查看进度。绿色成功后打开 https://1iyouzhen.github.io/ 。

每次新增、修改或删除文章并提交到 main，GitHub Actions 都会自动构建并发布。无需本地安装 Hugo，也无需手工更新 HTML。修改草稿同样会触发构建，但草稿不会出现在网站上。

## 文章模板

新建文件路径示例：`content/posts/my-first-post/index.md`。

```markdown
---
title: "我的第一篇文章"
date: 2026-11-15T08:00:00+08:00
slug: my-first-post
description: "文章的一句话介绍"
summary: "这是首页和搜索结果中显示的文章摘要。"
tags: [LLM, 学习笔记]
draft: false
math: false
---

这里是文章开头。

## 第一个小节

这里写正文，可以使用 **加粗**、列表、链接和代码块。

## 参考资料

- [参考链接](https://example.com/)
```

- `title`：网页上显示的标题，可使用中文。
- `date`：发表时间。请填真实时间；未来日期默认不发布，也不会在时间到达时定时上线，需要再次提交或手动运行 Actions。
- `slug`：文章网址的英文短名，全站唯一。例如 `my-first-post` 对应 `/posts/my-first-post/`。
- `summary`：首页摘要。
- `tags`：自动生成标签页，无需手工维护。
- `draft: false`：公开发布；写作中改为 `true`，网站会自动隐藏它。
- `math: true`：启用数学公式，按需加载 MathJax。

## 修改或删除文章

在 GitHub 打开文章 `index.md`，点铅笔编辑，再点 **Commit changes**。删除文章目录中的 Markdown 并提交，会自动从站点、归档、标签、搜索和 RSS 中移除该文章。

**每次点击提交到 main，都会触发一次自动更新。** 如果提交到其他分支，请将 Pull Request 合并到 main 后再查看网站。

## 加图片

先创建文章，再进入这篇文章的目录，用 **Add file → Upload files** 上传图片，例如 `figure.png`。文章里写：

```markdown
![图片说明](figure.png)
```

图片与文章放在同一个目录；注意文件名大小写。

## 本地写作（可选）

本地项目：`C:/Users/l1337/youzhen-blog`。本地预览需要 Hugo Extended 0.170.0，Windows 可运行 `./scripts/bootstrap.ps1` 安装。

```powershell
# 先同步网页上的更新
git pull --ff-only
# 预览，包括草稿
.\.tools\hugo.exe server -D
```

完成后，只需提交 Markdown：

```powershell
git add content
git commit -m "docs: add new article"
git push origin main
```

也可运行 `./scripts/publish.ps1`，会先在本地构建、校验并提交源文件；推送后由 GitHub 自动部署。

## 发布进度与失败排查

进入仓库 **Actions → Publish blog** 查看最近一次运行。绿色表示成功；红色表示失败，点进去查看具体步骤。失败时已上线的网站保持上次成功版本。

常见原因：Markdown 开头少了 `---`、标题中的冒号没有加引号、图片文件名错误、两个文章使用相同 slug，或手工修改后产生无效链接。修复并重新提交即可。

构建会自动检查必要页面、内部链接、RSS、搜索索引和草稿隔离。`public/` 是临时生成目录，不提交到仓库。GitHub Pages 的 Source 使用 **GitHub Actions**。不需要提交 `docs/` 或生成 HTML。

## 配置与样式

- `hugo.toml`：站点名称、导航、社交链接、简介。
- `content/about.md`：关于页面。
- `content/projects.md`：项目页面。
- `assets/css/extended/custom.css`：个性化样式。
- `.github/workflows/publish.yml`：自动构建与发布。
- `versions.json`：固定的 Hugo 与主题版本。

主题来自 MIT 许可的 PaperMod，保留原始 LICENSE。文章版权归各自作者所有。


## 已提交，但网页看起来没变化？

1. 先看 Actions → Publish blog 是否绿色成功；现在部署后还会检查线上页面的提交版本。
2. 查看网站页脚的版本号，并与 GitHub 最新提交前七位比较。点页脚“检查更新”可以重新加载最新页面。已经打开的页面也会定期检查新版本。
3. 首次安装更新检测以前缓存的旧页面，需要按一次 Ctrl+Shift+R 强制刷新；之后页面会自动检测后续版本。
4. 仓库 README.md 是 GitHub 仓库介绍，不会直接显示在博客正文中。博客文章请修改 content/posts/ 下的 Markdown，网站名称请修改 hugo.toml 中的 title 和 params.label.text。
5. 文章网址由 slug 决定。例如文件 content/posts/tset.md 中写了 slug: my-first-post，网址就是 /posts/my-first-post/。
6. 首页按发表日期排序，新建文件不一定排在最上面。需要排在前面的文章，请填写正确的完整日期和时区；不要填写未来时间。

GitHub Pages 的缓存响应可能短暂保留旧版本。本站已增加版本检测、手动更新入口以及搜索索引重新获取，部署仍需要等待 Actions 成功。
