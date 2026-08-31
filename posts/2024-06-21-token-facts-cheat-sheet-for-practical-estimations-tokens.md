---
title: "Token facts cheat sheet"
date: 2024-06-21
lang: en
noindex: true
summary: "Order of magnitude figures for tokens: counts per word, page and book, training set sizes, context lengths, and latency per input or output token."
source: linkedin
legacy_url: /thoughts/2024/06/21/token-facts-cheat-sheet-for-practical-estimations-tokens.html
---

🦎 Token facts cheat sheet for practical estimations


Tokens are the chunks of text LLMs read and generate. The number of tokens affects various factors, including speed, memory usage, and operating cost, and is essential for understanding the maximum input length and the size of the training dataset used. Here are some figures to give some notion of scale and easily do back-of-the-envelope calculations.


📊 Token count examples:
- Single word: 1.3 tokens
- Average sentence: 30 tokens
- One page: 600 tokens
- The US Declaration of independence (3 pages): 1.7k tokens
- “Attention is all you need” research paper (15 pages): 10k tokens
- The great gatsby (200 pages): 72k tokens
- The bible: 1M tokens
- English wikipedia: 6B tokens
- Refined web dataset: 5T tokens


🚂 Model Training:
- Nb tokens models are usually trained on: 0.5 - 4 trillion
- Token-to-parameter training ratio: 20 - 300


🎛 LLMs token related settings:
- Nb tokens in an LLM’s vocabulary: 32k - 100k
- Token difference: GPT4 vs. llama (same text): llama +20% tokens
- Max input tokens (context length) for LLMs: 1k-100k


⏳ Inference latency estimates*:
- Additional inference time when adding 1 input token: 0.3ms
- Additional inference time when adding 1 output token: 30ms
-> Adding an output token introduces 100x more latency than adding an input token.
- Time before first token: 30 - 500ms
E.g., Generating a page of text takes ~18 seconds (30ms*600 output tokens + 300ms)

*Approximations, varying with input/output length, batch size, hardware, model size, tokenizer, and optimization techniques. Data based on low batch sizes (1-8), standard token lengths (100-2k), and 7b-70b parameter models.

Sources + cool links in the comments.
