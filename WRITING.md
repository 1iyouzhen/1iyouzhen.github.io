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
  images/        # 这篇文章的图片，中英文共用
    architecture.png
    result.jpg
```

每篇文章统一使用一个独立文件夹；文件夹内放 index.en.md、index.zh.md，配图全部放入该文件夹的 images/。显式语言后缀可避免混淆，没有语言后缀的 index.md 默认归入英文站点。

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
- 图片放在这篇文章的 images/ 子目录，通过相对路径引用，例如 ![说明](images/architecture.png)。英文版引用同一图片，只需翻译说明文字。
- 原英文 /en/ 地址保留跳转到新的英文根路径。


### 在 GitHub 为文章上传图片

1. 进入 content/posts/文章英文名/images/，点击 Add file → Upload files。
2. 上传这篇文章的图片并提交到 main，例如 architecture.png。
3. 打开上一层的 index.zh.md，在需要显示图片的地方添加：

```markdown
![系统架构示意图](images/architecture.png)
```

英文文件 index.en.md 引用同一张图：

```markdown
![System architecture](images/architecture.png)
```

图片名建议使用英文、数字和连字符，引用时大小写必须与文件名一致。不要把 images/ 上传到 public/，也不要在 Markdown 中写本机磁盘路径。

### 文章封面

在文章顶部的两个 --- 之间加入：

```yaml
cover:
  image: images/architecture.png
  alt: 系统架构示意图
```

英文版使用相同 image 路径并翻译 alt 即可。保存并提交后，正文图片与封面都随网站自动发布。相同文件名可以出现在不同文章的 images/ 中，彼此不会覆盖。

## 本地生成双语草稿

```powershell
python scripts/new_post.py my-article --title-zh 中文标题 --title-en EnglishTitle
```

会创建文章独立文件夹，其中包含 index.zh.md、index.en.md 和 images/。两种语言默认都是草稿，不会覆盖已有目录。images/.gitkeep 用于让 GitHub 保留空图片目录，上传图片时不用删除它。

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


## 源码和网站内容同步核验

网站名称已统一为你先前设置的 Notes。名称的实际配置位于 hugo.toml 的 title 和 params.label.text，以及两种语言的 content/_index.en.md / content/_index.zh.md。修改 README 标题只修改 GitHub 仓库介绍，不会自动修改网站名称。

旧 docs 目录是第一次发布时留下的静态快照，不再参与构建，现已从 GitHub 源码中移除。真正可编辑的内容只有 content/ 下的 Markdown；无需编辑生成的 HTML。

自动发布现在会比对全部页面的实际标题、正文、导航和链接，以及两种语言的搜索索引与 RSS。只有线上内容与本次源码构建一致，Actions 才会显示发布核验通过。该核验不再仅检查提交版本号。

英文页面修改 .en.md，简体中文页面修改 .zh.md；两份译文仍分别维护。更改网站公共配置会一起作用于两种语言。
