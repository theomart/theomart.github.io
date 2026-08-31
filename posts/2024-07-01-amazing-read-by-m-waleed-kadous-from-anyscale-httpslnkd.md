---
title: "Numbers every LLM developer should know"
date: 2024-07-01
lang: en
noindex: true
summary: "Numbers every LLM developer should know, from Waleed Kadous at Anyscale: cost ratios, tokens per word, and GPU memory per token."
source: linkedin
legacy_url: /thoughts/2024/07/01/amazing-read-by-m-waleed-kadous-from-anyscale-httpslnkd.html
---

Amazing read by M Waleed Kadous from Anyscale:
https://lnkd.in/e77fUTiv

"At Google, there was a document put together by Jeff Dean, the legendary engineer, called Numbers every Engineer should know. It’s really useful to have a similar set of numbers for LLM developers to know that are useful for back-of-the envelope calculations."


Some of my favorites: """
6:1 -- Cost Ratio of OpenAI fine tuned vs base model queries
1:1 -- Cost Ratio of Self-Hosted base vs fine-tuned model queries

1.3:1 -- Average tokens per word

2x number of parameters: Typical GPU memory requirements of an LLM for serving

~1 MB: GPU Memory required for 1 token of output with a 13B parameter model
""""

Cheat sheet by Huaiwei Sun.
