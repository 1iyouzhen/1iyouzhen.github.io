---
title: "LLM Inference Notes: Starting with One Request"
date: 2026-11-15T08:00:00+08:00
slug: inference-notes
description: A draft of inference system learning notes.
tags: [LLM, AI Infrastructure, Inference Systems]
draft: true
math: true
---
This is a writing draft and is excluded from the production site. Add your own code reading, experiments, and references before publishing.

## Questions to answer

- Which modules does a request pass through from the API to model execution?
- How do the data flows of prefill and decode differ?
- How is the KV cache lifecycle managed?

## Derivation and verification

Add mathematical expressions here, such as $y = Wx + b$.

## Experiment log

Record the model, hardware, software versions, input and output lengths, concurrency, measurement method, and original results.

## References

Add the original sources you have actually read.

## Code placeholder

```python
def forward(x, weight, bias):
    return x @ weight + bias
```
