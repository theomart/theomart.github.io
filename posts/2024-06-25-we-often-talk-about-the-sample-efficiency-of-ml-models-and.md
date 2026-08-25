---
title: "The sample efficiency comparison is unfair"
date: 2024-06-25
lang: en
summary: "Sample efficiency comparisons between humans and models are unfair, and in context learning changes what counts as an example."
source: linkedin
legacy_url: /thoughts/2024/06/25/we-often-talk-about-the-sample-efficiency-of-ml-models-and.html
---

🤌 We often talk about the sample efficiency of ML models and compare it to that of humans.

That is, how many data points (or samples) a model needs to be trained on to learn X versus how many a human needs.

Generally, the conclusion is that humans are much more sample efficient than ML models, as they appear to require much less data to learn the same thing.

We often hear the example of the number of hours it takes to learn how to drive, with most people comparing the 20-30 hours a human needs to the millions of hours of video that models need to make self-driving cars.

However, it's interesting to think about sample efficiency for in-context learning, where we don't look at the number of examples a model has been trained on, but rather how much information it saw in the prompt before being asked to execute a task.

Can an LLM learn how to speak a new language only with in-context learning? Maybe. Would the same information delivered to a human be enough for them to learn how to speak this language right away? Surely not.

👀 The comparison of the sample efficiency of humans versus ML models has never really been fair. In the learning-to-drive example, why do we choose the 30 hours of driving lessons the human took?

Why not take into account the thousands of times they interacted with a car, like seeing one in action from inside and outside, or driving a bike?

Also, did the models powering self-driving cars know what an object was before being trained? Did they know what a road was? A human surely knew that before being "trained".

Human evolution looks like a long training, with a TON of data.
