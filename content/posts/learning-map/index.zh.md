---
title: 学习导航：从语言模型到推理系统
date: 2026-11-15T07:50:00+08:00
slug: learning-map
description: 整理语言模型、推理系统与 Agent 方向的公开学习入口。
summary: 把公开学习资源整理成几个入口：语言模型基础、推理服务、Agent 与检索增强生成。它是一份可继续补充的导航，具体结论仍需要回到原始资料与代码中验证。
tags: [LLM, AI Infrastructure, 学习资源]
categories: [学习导航]
draft: false
---
这一页整理几个公开学习入口，方便后续笔记互相连接。它是一份资源导航，不代表已经完成所有课程、实现或复现。

## 语言模型基础

- **[Stanford CS336](https://cs336.stanford.edu/)**：课程与作业入口。相关学习仓库为 [assignment1-basics](https://github.com/1iyouzhen/assignment1-basics)。
- **[Happy-LLM](https://github.com/datawhalechina/happy-llm)**：Datawhale 的大语言模型原理与实践教程。

阅读时可以先建立问题清单：输入如何表示，训练目标是什么，一个训练步骤包含哪些运算，以及结果应该如何检查。

## 推理系统与基础设施

- **[SGLang](https://github.com/sgl-project/sglang)**：推理服务项目与文档入口。
- **[mini-sglang](https://github.com/sgl-project/mini-sglang)**：面向理解 LLM serving 系统的紧凑实现。

这部分可以沿一次请求的执行路径阅读：请求进入后如何排队，如何准备输入，哪些状态需要保留，生成的 token 如何返回。具体机制与版本行为以项目当前文档和源代码为准。

## Agent 与检索增强生成

- **[Hello-Agents](https://github.com/datawhalechina/hello-agents)**：智能体原理与实践教程。
- **[All-in-RAG](https://github.com/datawhalechina/all-in-rag)**：RAG 技术学习资料。

阅读和实验时，可以把模型输出、检索证据、工具调用和最终评估分开记录，避免只保存最终回答而丢失中间过程。

## 把资源变成笔记

每次只选择一个可以回答的小问题，附上对应的原始资料与代码版本，再记录验证过程。若有性能实验，还需要写明模型、硬件、软件版本、输入长度、并发与测量口径，避免把不同条件下的结果直接比较。

后续文章会通过标签与这份导航连接；所有资源的内容和维护状态，以链接中的原项目为准。
