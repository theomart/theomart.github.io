---
layout: post
title: "OCR just got better"
date: 2024-07-15 11:59:01 +0200
source: linkedin
categories: thoughts
linkedin_urn: urn:li:activity:7153367591258910720
---

🤠 OCR just got better.

Surya: a python package that detects the position of each line of text in an image / pdf.

TLDR:
- It gives you the POSITION of each line of text in the document, NOT WHAT the text is
- Works on complex layouts, bad captures (blurry/rotated)
- Runs on GPU, takes 2sec / image for the CPU version
- Doesn't work on photos
- Free to use commercially for companies <$5M revenue / year
- Based on NVIDIA's SegFormer
- Named after the Hindu sun god, who has universal vision


👨‍💻Example use case
newspaper to markdown, based on the size and position of the bounding boxes you infer the structure of the newspaper, run each block independently through OCR and convert it to a markdown. (or train an LLM on the The New York Times and get sued cc OpenAI)

Thanks Vik Paruchuri !!!


Link in the comments
