---
title: "A non technical dive into alignment"
date: 2024-07-09
lang: en
noindex: true
summary: "A non technical walk through alignment: knowledge comes from pretraining, behaviour from RLHF, and what it took OpenAI to build InstructGPT."
source: linkedin
legacy_url: /thoughts/2024/07/09/how-do-we-get-llms-to-know-what-a-software-bug-is-without-m.html
---

🤔 How do we get LLMs to know what a software bug is without making them write buggy code? A non technical dive into alignment.


🍻 Knowledge vs Behaviour

TLDR: knowledge is acquired during pretraining on a huge dataset, behaviour is taught by humans.

LLMs get good at various tasks by being trained to repeatedly predict the next word in a sequence from a large and diverse dataset.

Problem is, this dataset contains hurtful articles, buggy code, blog posts about conspiracy theories etc.

This data is useful, but only if used the right way:
- we WANT an AI coding assistant to UNDERSTAND what a bug is and how it can be solved BUT we DON’T WANT a coding assistant to write buggy code.
- we WANT the model to KNOW 2% of the people believe the earth is flat, but we DON’T WANT the model to say that the earth is flat 2% of the time when asked about it.

We want to *bias* the model toward what we believe is the trustworthy / high quality part of its training data. In other words, now the model knows what humans know, we want the model to behave the way humans want it to behave.

The most straightforward way to do this is to use reinforcement learning: you tell the model if what it says is good or bad and it tries to adapt to your preferences.


🏓 How do you do that in practice?

TLDR: ask some humans what they prefer over a few examples and then replace them by a model

The problem is that you have to do that A LOT for the model to “align”, e.g. to build instructGPT from GPT3, OpenAI researchers used 31k unique prompts 256k times which amounts to 8 billion human given feedback.

How did they do it?
1) they hired 40 labelers
2) gathered various prompts submitted by users via the OpenAI API
3) made the model generate multiple answers for each prompt
4) asked the labelers to rank the answers
5) trained a “reward model”, whose goal was to mimic the labelers’ answers
7) when doing the reinforcement learning, asked the “reward model” rather than a human to judge the LLM’s answer

Just as you wouldn't want to erase fundamental skills like breathing or walking when brainwashing someone, you wouldn’t want the model to lose its core capabilities, e.g. reasoning, acquired during pre-training. So, during the reinforcement learning phase, for every new instruction tailored to align with human preferences, the model is also given 8x as many tasks from its pre-training phase (that’s the ratio OpenAI used to make InstructGPT)

This technique, called Reinfrocement Learning with Human Feedback (RLHF), works wonders, but reinforcement learning is complex, and it is slow: it requires the LLM to generate an answer every step of the way, and we all know how long it can take.

Last year, researchers at stanford proposed a much simpler technique called Direct Preference Optimization, an answer to those 2 challenges, but linkedin posts are limited to 3000 characters, so that’s for another time.

Hope that was useful!
