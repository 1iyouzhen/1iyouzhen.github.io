---
title: "Learning Map: From Language Models to Inference Systems"
date: 2026-11-15T07:50:00+08:00
slug: learning-map
description: Public learning resources for language models, inference systems, and agents.
summary: A set of starting points for language model foundations, inference serving, agents, and retrieval-augmented generation. This is a growing resource guide; specific conclusions still need to be checked against original sources and code.
tags: [LLM, AI Infrastructure, Learning Resources]
categories: [Learning Map]
draft: false
---
This page collects public learning resources so that future notes can connect to them. It is a resource guide, and does not imply that I have completed every course, implementation, or reproduction.

## Language model foundations

- **[Stanford CS336](https://cs336.stanford.edu/)**: course materials and assignments. The related learning repository is [assignment1-basics](https://github.com/1iyouzhen/assignment1-basics).
- **[Happy-LLM](https://github.com/datawhalechina/happy-llm)**: Datawhale’s guide to language model principles and practice.

A useful starting point is a list of questions: How are inputs represented? What is the training objective? Which operations make up a training step? How should the result be checked?

## Inference systems and infrastructure

- **[SGLang](https://github.com/sgl-project/sglang)**: an entry point to the inference serving project and its documentation.
- **[mini-sglang](https://github.com/sgl-project/mini-sglang)**: a compact implementation for understanding LLM serving systems.

Follow the execution path of a request: how it is queued, how inputs are prepared, which state must be kept, and how generated tokens return to the caller. For specific mechanisms and version-dependent behavior, use the project’s current documentation and source code.

## Agents and retrieval-augmented generation

- **[Hello-Agents](https://github.com/datawhalechina/hello-agents)**: a guide to agent principles and practice.
- **[All-in-RAG](https://github.com/datawhalechina/all-in-rag)**: learning resources for retrieval-augmented generation.

When reading or experimenting, record model outputs, retrieved evidence, tool calls, and evaluation separately. Keeping only the final answer loses the intermediate process.

## Turning resources into notes

Choose one small, answerable question at a time. Keep the original sources and code version, then record the verification process. Performance experiments should also specify the model, hardware, software versions, input lengths, concurrency, and measurement method, so that results from different conditions are not compared as if they were equivalent.

Future articles will connect to this guide through tags. Each original project remains the source of truth for its content and maintenance status.
