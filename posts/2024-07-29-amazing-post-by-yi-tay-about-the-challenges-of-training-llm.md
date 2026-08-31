---
title: "Training LLMs from scratch as a startup"
date: 2024-07-29
lang: en
noindex: true
summary: "Yi Tay on training LLMs from scratch as a startup: hardware roulette, multi cluster juggling, thin codebases, and the cost of every idle minute."
source: linkedin
legacy_url: /thoughts/2024/07/29/amazing-post-by-yi-tay-about-the-challenges-of-training-llm.html
---

🌟 Amazing post by Yi Tay about the challenges of training LLMs as a startup! "Training great LLMs entirely from ground up in the wilderness as a startup"


👍 TLDR

When choosing compute providers, startups should look beyond just hardware specs and price. Consider the whole package: storage, networking, and the expertise of the support team. This can help you avoid some of the headaches that come with training LLMs on a budget.


🍭 Some challenges

Hardware roulette: You never know what you're gonna get! Even with the same GPUs (like H100s), the quality of computing clusters can be all over the place. Some might crash every few hours, while others have terrible I/O and file systems that make checkpointing a nightmare. It's a gamble!

Multi-cluster mayhem: With limited GPU supply, startups often have to cobble together clusters from different sources. This means constantly shuffling data around and dealing with the hassle of replication.

Codebases from outside big tech can be a bit... underwhelming. They often lack support for large-scale training, leaving you to fend for yourself.

Strapped for cash (and compute): Startups don't have the luxury of throwing endless resources at hyperparameter sweeps. You gotta trust your gut and take a "YOLO" approach to model scaling.

Babysitting duty: Keeping an LLM training run alive is a full-time job. You're constantly on the lookout for loss spikes, numerical weirdness, and hardware tantrums. And when something goes wrong, you better fix it fast! Every minute of idle time on those 10k H100s is burning a hole in your pocket to the tune of $500 per minute!


Link in the comments 🧁
