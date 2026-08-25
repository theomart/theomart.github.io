---
title: "Google's Gemma, don't use the 7B yet"
date: 2024-08-15
lang: en
summary: "Google's Gemma 2B and 7B at release, the gap between the reported benchmarks and what the community measured, and the parameter count discrepancy."
source: linkedin
legacy_url: /thoughts/2024/08/15/tldrs-on-googles-gemma-spoiler-dont-use-gemma-7b-yet-n.html
---

⚡ TLDRs on Google's Gemma, spoiler: don't use Gemma 7B (yet?)


👞 Non technical TLDR

- Google "open weighted" 2 models: Gemma-2B and Gemma-7B, which are direct competitors of Microsoft's phi2 and Mistral AI's Mistral-7B resp.

- They report that their 7B model is better on most benchmarks than Mistral-7B (the current leader for this "size class")

- The community (and I) see the contrary so far, but it wouldn't be the first time that errors in implementations hinder performances, it has only been 4 days, let's give it some time

- Google created a Gemma tuning competition on Kaggle, awarding $10k / winner: they are pushing adoption

- If Gemma is indeed worse, it could just be seen as a move from Google to be able to sit at the "LLM open [[sourcers]]" table without contributing significant value


🔬 Technical TLDR

- Google released weights for Gemma-2B & Gemma-7B + a technical report + a standalone C++ inference engine implementation

- 2B trained on 2T tokens, 7B trained on 6T tokens. 6T is a lot but rumours say Mistral-7B was trained on 8T

- Both models are now available in llama.cpp and ollama

- Vocabulary 8x larger than Llama2’s (256k vs 32k)

- Google observes better performance with Gemma 7B compared to Mistral 7B, the community (me included) observes the contrary so far

- I tested it using llama.cpp, it would not be the first time that errors in implementation degrades performances, it's maybe too early to judge, let's see

- Google introduced yet a new chat template (check attached screenshot)

- They kinda lie on the number of parameters: Mistral-7B has 7.2B parameters; Gemma-7B has 8.5B

- You can try Gemma on Hugging Face Chat & Perplexity: link in the comments

- Waiting for chatbot areana benchmarks


Links in the comments
