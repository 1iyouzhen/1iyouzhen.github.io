---
title: LLM 推理笔记：从一个请求开始
date: 2026-11-15T08:00:00+08:00
slug: inference-notes
description: 待补充的推理系统学习笔记。
tags: [LLM, AI Infrastructure, 推理系统]
draft: true
math: true
---
这是一份写作草稿，不会出现在正式站点。发布前请补充自己的代码阅读、实验与引用。

## 想回答的问题

- 请求从 API 到模型执行经过哪些模块？
- Prefill 与 Decode 的数据流有什么区别？
- KV cache 的生命周期如何管理？

## 推导与验证

这里可以补充数学公式，例如 $y = Wx + b$。

## 实验记录

记录模型、硬件、软件版本、输入输出长度、并发、测量方法与原始结果。

## 参考资料

补充实际阅读过的原始资料。

## 代码示例占位

```python
def forward(x, weight, bias):
    return x @ weight + bias
```
