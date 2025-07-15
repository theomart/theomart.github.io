---
layout: post
title: "How do you continue training on an already pre trained LLM"
date: 2024-08-09 18:45:14 +0200
source: linkedin
categories: thoughts
linkedin_urn: urn:li:activity:7175808292860874753
---

🥋 How do you continue training on an already pre trained LLM: TLDRs of the "Simple and Scalable Strategies to Continually Pre-train LLMs" paper


🥖 Non-technical TLDR

- When you have a pre-trained LLM and want to update it on new data, you usually have to re-train it from scratch on all the data combined (old + new), which is very expensive (GPT4 training cost >$100M)

- This paper shows you can continue the pre train phase ("continually pre-train") on the new data instead, and get similar performance with way less compute, with simple tricks

- When training a LLM (and most ML models for that matter), you are trying to solve an equation, but you only know in which *direction* to change the value of your model's parameters to get closer to the solution (+ or -), so then you have to choose *how much* you increase/decrease them. This step size you have to pick is the "learning rate" (LR)

- Before, researchers were keeping the LR constant for the whole training, but they figured that at the beginning of the training, doing big steps ("warming" up the LR) helped getting faster to the solution, but when getting close to it it was better to slow down ("decaying" the LR) and making much slower step


With that said, the tricks they found were to:
- Re-warm and re-decay the LR when training on the new data to help the model adapt
- "Replay" a small % of data from the previous dataset to prevent the model from forgetting what it learned before, in other words mixing the new data with a bit of the old.

- They show this works for a weak distribution shift (English Wikipedia → English web crawl) and a strong shift (English → German) and for 405M and 10B parameter models.

- So you can efficiently update your LLM, on new high-quality datasets as they come out, without training from scratch each time



🔬 Technical TLDR

- Cosine decay learning rate schedules, commonly used for LLMs, decay LR to a small value by the end of pre-training

- To adapt the LLM to a new dataset, they find re-warming LR to the original max value and re-decaying it over the course of training on the new data is crucial

- However, this causes some forgetting of the previous dataset, BUT replaying 5% of data from the previous dataset is sufficient to mitigate this forgetting in most cases (25% replay is needed for the stronger English→German shift)

- Combining LR re-warming, re-decaying and replay allows continual pre-training to match the performance of re-training from scratch on the combined datasets

- This holds for a 405M model and 10B model and for both weak and strong distribution shifts between datasets

- They also propose "infinite learning rate schedules" that maintain a constant high learning rate across datasets to avoid optimization difficulties from re-warming, though more work is needed to validate them

Thanks Adam Ibrahim, Benjamin Thérien, Kshitij Gupta, Dr. Mats L. Richter, Quentin Anthony, Timothée Lesort, Eugene Belilovsky, Irina Rish!
