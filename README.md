# Youzhen's Notes

Youzhen Li 的个人博客，记录 LLMs 与 AI Infrastructure 的学习笔记、论文阅读与工程实践。

- 在线阅读：https://1iyouzhen.github.io/
- 技术栈：Hugo Extended 0.170.0 + PaperMod（固定源码版本见 versions.json）
- 托管：GitHub Pages，main 分支 /docs
- 写作说明：[WRITING.md](WRITING.md)

## 本地预览

安装 Hugo Extended，Windows 可运行 `./scripts/bootstrap.ps1`，随后运行 `npm run dev`。

## 发布文章

在 content/posts/ 中添加 Markdown，再运行 `./scripts/publish.ps1`。脚本会构建站点、检查内部链接与草稿隔离，随后提交和推送更新。需要已登录并有权限的 Git 环境。

## 目录

- content/：文章与独立页面
- assets/css/extended/：个性化样式与代码高亮
- layouts/partials/：首页和按需公式加载
- static/：图标与站点静态文件
- themes/PaperMod/：固定版本的 MIT 许可主题，保留原始 LICENSE
- docs/：生成的 GitHub Pages 站点，不直接编辑
- scripts/：构建、校验与发布脚本

## 说明

阅读体验参考 Lilian Weng 的 Lil’Log；本站内容独立编写，未复制其文章、图片或个人资料。上线时包含两篇站点介绍与学习导航；推理系统文章提纲默认 draft: true，不会发布。项目页明确区分个人项目与上游 fork。

文章版权归作者所有。第三方代码依各自许可证使用。
