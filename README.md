# Notes

blog about LLMs and AI infrastructure.

- English (default): https://1iyouzhen.github.io/
- 简体中文：https://1iyouzhen.github.io/zh/
- English guide: [WRITING.en.md](WRITING.en.md)
- 中文写作说明：[WRITING.md](WRITING.md)




## 文章与图片目录 / Article folders

```text
content/posts/my-article/
  index.en.md
  index.zh.md
  images/
    architecture.png
```

每篇文章独立一个文件夹，所有配图放在该文章的 images/ 中；Markdown 使用相对路径 ![说明](images/architecture.png)。两种语言共享图片。scripts/new_post.py 会自动建立这套结构。

Each article has its own images/ folder. Both translations reference the same files with paths such as images/architecture.png. See WRITING.md or WRITING.en.md for GitHub upload steps and cover configuration.
