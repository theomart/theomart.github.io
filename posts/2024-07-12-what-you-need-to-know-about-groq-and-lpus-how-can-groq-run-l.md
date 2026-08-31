---
title: "Groq and LPUs, why they run LLMs faster"
date: 2024-07-12
lang: en
noindex: true
summary: "Why Groq ran Mixtral faster than GPU providers: deterministic LPUs, on chip memory, a compiler first design, and the scaling question that follows."
source: linkedin
legacy_url: /thoughts/2024/07/12/what-you-need-to-know-about-groq-and-lpus-how-can-groq-run-l.html
---

What you need to know about Groq and LPUs: How can Groq run LLMs so much faster than the competition?


🖼 About Groq

- Groq runs Mixtral at 450 token / seconds, to put that in perspective, the second best provider in terms of throughput (Fireworks AI) runs it at 190 t/s (cf attached screenshot)

- They build their own chips, the Language Processing Units (LPUs), they don´t use GPUs

- This opens new use cases for LLMs for time sensitive applications, e.g. loading web pages based on a model’s output

- Groq was founded in 2016 by Jonathan Ross, the guy who started the TPU effort at Google in 2014, as part of the famous 20% project

- Groq is selling their chips but they focus more on serving open source LLMs today

- Groq claim they will be profitable by end of 2024


🥊 LPUs vs GPUs

- GPUs are good at running dumb operations in parallel, LPUs embrace the sequential nature of inference for today's LLM, that’s why LPUs are faster for inference but not for training

- The bottleneck of GPUs is memory bandwidth: all state of the art GPUs use a component called HBM (High memory bandwidth), be it AMD or Nvidia GPUs, which they all get from the same suppliers

- Because of that, GPUs manufacturers are subject to shortages, LPUs in the contrary don't use those, they add "net" new compute capacity to the market

- LPUs were designed backwards from the software, the Groq team spent their first 6 months of existence working on the compiler

- This software first approach allows them to easily adapt to the rapid pace of innovation, while Nvidia GPUs require custom CUDA kernels, making bringing a new model to them more difficult

- The GPU war is all about software: AMD GPUs are actually faster that Nvidia’s, Nvidia’s moat is not hardware, it’s software, supported by 50k+ CUDA kernel developers

- LPUs are deterministic in nature: you know when and where in the memory to find the data the current operation needs, contrary to GPUs that have different levels of memory hierarchy that behave non deterministically, which makes them slower: as you cannot predict where and when you can find the data, you need additional time consuming logic to orchestrate the data flow

- This deterministic nature also makes it easier to make LPUs communicate with one another, and therefore have many act as one

- LPUs are easier to manufacture than GPUs, they are made at 14nm which is a very mature technology, making manufacturing more robust and cheaper, contrary to Nvidia’s last H100 which are made at 4nm, involving much more complex processes

- LPUs have on chip memory, which 1) helps lowering latency, and 2) doesn’t require advanced packaging technology, which in turn makes their manufacturing process very flexible, that's what allowed them to switch fabs from Global Foundries, U.S. , Inc. to Samsung Semiconductor for example


🤔 One question though: Mixtral fits on 600 LPUs, while it fits on 2 H100, cause LPUs only have 220MB of memory vs 80GB for H100, will this scale?
