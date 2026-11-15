# 添加文章与自动发布

网站默认使用英文。打开 https://1iyouzhen.github.io/ 即进入 English；简体中文版位于 https://1iyouzhen.github.io/zh/ 。

导航栏的语言按钮显示当前语言。点击后展开 English / 简体中文，选择后进入对应语言的同一篇文章。若该文章尚无已发布译文，切换到目标语言首页。

## 在 GitHub 添加文章

1. 打开仓库的 content/posts 目录，选择 Add file → Create new file。
2. 使用下面的双语文件结构；每篇文章使用唯一的英文目录名。
3. 填写配置和正文，准备发布时设置 draft: false，提交到 main。
4. 等待 Actions → Publish blog 绿色成功，网站即自动更新。

```text
content/posts/my-article/
  index.en.md    # English，默认站点
  index.zh.md    # 简体中文
  figure.png     # 两种语言共享的图片
```

显式使用 .en.md 和 .zh.md 可避免混淆。没有语言后缀的 index.md 默认归入英文站点。单文件形式也支持，例如 my-article.en.md 与 my-article.zh.md。

两份文章使用相同 slug，分别翻译 title、description、summary、tags、categories 和正文。两种语言独立维护，修改一份不会自动翻译另一份。未完成的译文设 draft: true，只会发布准备好的版本。

## 中文文章模板

保存为 content/posts/my-article/index.zh.md：

```markdown
---
title: 我的文章
date: 2026-11-15T08:00:00+08:00
slug: my-article
description: 一句话介绍
summary: 显示在文章列表的摘要
tags: [LLM, 学习笔记]
draft: false
math: false
---

这里开始写正文。

## 第一个小节

文章内容。
```

英文版保存为同目录的 index.en.md，保留相同 slug，翻译标题与正文。日期填写实际发表时间，不要填未来时间；未来日期需要等待后续构建才会发布，并不会到时自动运行。

## 链接和图片

- 英文文章：/posts/my-article/；中文文章：/zh/posts/my-article/。
- 英文站内链接用 /archives/、/search/、/tags/；中文站内链接用 /zh/archives/、/zh/search/、/zh/tags/。
- 图片放在文章目录里，通过相对路径引用，例如 ![说明](figure.png)。
- 原英文 /en/ 地址保留跳转到新的英文根路径。

## 本地生成双语草稿

```powershell
python scripts/new_post.py my-article --title-zh 中文标题 --title-en EnglishTitle
```

会创建 index.zh.md 和 index.en.md，默认都是草稿，不会覆盖已有目录。

Windows 可运行 ./scripts/bootstrap.ps1 安装固定版 Hugo，然后 npm run dev 预览。也可以运行 ./scripts/publish.ps1，在本地构建、检查后提交源文件；推送 main 后仍由 GitHub Actions 自动发布。

## 修改和删除

在 GitHub 编辑对应语言的 Markdown 并提交即可。删除某语言文件后会从该语言的页面、搜索、标签和 RSS 中移除。两种语言的搜索、归档、标签和 RSS 分别生成。

README.md 是仓库介绍，不会直接变成网站内容。不要手动编辑 public/ 或旧 docs/ 里的生成文件。

## 站点配置

- hugo.toml：默认语言、两种语言的菜单、首页和描述。
- i18n/en.toml 与 i18n/zh.toml：界面提示和按钮翻译。
- content/about.en.md 与 content/about.zh.md：关于页。
- content/projects.en.md 与 content/projects.zh.md：项目页。
- assets/css/extended/custom.css：个性化样式。
- .github/workflows/publish.yml：自动发布。
- WRITING.en.md：英文写作说明。

公式文章设 math: true，即按需加载 MathJax。代码块可声明语言，目录与复制按钮两种语言均可使用。

## 更新检查

Actions → Publish blog 绿色成功后，可在页脚查看提交版本或点击检查更新。已打开页面会定期检测新版本。若浏览器仍停留在本次界面改版前的缓存，按 Ctrl+Shift+R 强制刷新一次。
