---
title: "Takeways from the Mixtral paper with no chitchat"
date: 2024-07-23
lang: en
noindex: true
summary: "Takeaways from the Mixtral paper: sparse mixture of experts per transformer block, 47B total for 13B active, MegaBlocks, and a 32k context that holds."
source: linkedin
legacy_url: /thoughts/2024/07/23/takeways-from-the-mixtral-paper-with-no-chitchat.html
---

🐬 Takeways from the Mixtral paper with no chitchat.


👨‍🚀 Non technical TLDR

- Mistral AI created a very good LLM called Mixtral, that is "open source" and usable commercially

- Better than Llama2 while being 7x faster (and better than GPT3.5)

- It can take long input (~1/3 of the Frankenstein book), and remembers everything in the input contrary to models that can handle similar input length

- It excels on benchmarks with a technique ("mixture of experts") that wasn't used so often, but might become a new trend

- It's not like some parts of the model specialize on some topics



😎 Technical TLDR

- Mixture of experts: In EVERY transformer block, replaces the FF block (NOT the attention and norm layers) by 8 FF blocks + a router choosing which 2 experts to route the hidden states to at EVERY FORWARD (ie EVERY TOKEN)

- Because of this, it has 47B TOTAL parameters but only 13B ACTIVE. Increasing the nb of params by increasing the nb of experts goes just as fast as long as you only select 2, it's called conditional computation. ALL params are on VRAM, so for memory footprint, only the TOTAL count matters

- Making *SPARSE* MoE go BRRR: For large batches (ie especially when training) you want to parallelize your experts computation, but if the same experts get all the tokens, you cannot parallelize. Also, the memory allocated to each expert, by default, is fixed, so if you feed them more than they can eat, they will just drop the excess input, hurting performances. For those 2 reasons (at least), you need to ensure all experts get more or less the same load. They use MegaBlocks (standford 2022), a library with custom GPU kernels that allows for efficient sparse computation and dynamic memory block allocation for each expert, so that imbalance doesn't matter anymore = MoE go brrrr (40% speedup over MoE without MegaBlocks)

- Fast 32k context length: To make inference faster, you cache keys and values instead of recomputing them at every pass, for that you need to allocate memory to the cache. If done statically, you reserve the maximum length, though sequences often don't reach that length. vLLM allocates memory on the fly, it's called paged attention

- RELEVANT 32k context length: Models tend to ignore text that is in the middle of long prompts, they tested their model for that by using the passkey retrieval test: you put a keyword in the middle of your prompt and ask the model to retreive it. Mixtral passed the test with cuma laude (100%)

- They confirmed individual experts don't look at high level concepts like topics or langage. As ST-MoE (which they didn't cite) already observed, experts only specialize in some groups of tokens and relatively low level syntactic concepts

- They oversampled non english text to make it better at multilingual tasks

- Expectedly there is almost no info on the pretraining



Thank you Albert Qiaochu Jiang, Alexandre Sablayrolles, Arthur Mensch and team (you are way too many for me to tag you all lol)
