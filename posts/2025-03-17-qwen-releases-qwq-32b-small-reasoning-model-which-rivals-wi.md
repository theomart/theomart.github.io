---
title: "Qwen releases QwQ-32B"
date: 2025-03-17
lang: en
noindex: true
summary: "Qwen's QwQ-32B at release, a 32B reasoning model measured against DeepSeek-R1, and the two stage reinforcement learning behind it."
source: linkedin
legacy_url: /thoughts/2025/03/17/qwen-releases-qwq-32b-small-reasoning-model-which-rivals-wi.html
---

Qwen releases QwQ-32B, small reasoning model which rivals with DeepSeek-R1 and o1-mini.

TL;DR:
- Qwen is a serious player, just like DeepSeek
- a 32B model that rivals with a 671B mixture of experts (37B params activated)
- weights available on huggingface, no paper yet, you can chat with it on chat.qwen.ai
- they used 2 stages of reinforcement learning, 1st one for math and coding tasks and 2md one for general capabilities
- for math, reward is based on accuracy verifier, for coding it's based on predefined tests cases that are actually executed
- let's wait for other benchmarks, Qwen's look decent but interested to see if it replicates / what it looks like in the open LLM leaderboard
