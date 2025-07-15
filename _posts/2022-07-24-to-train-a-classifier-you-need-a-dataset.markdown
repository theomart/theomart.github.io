---
layout: post
title: "To train a classifier, you need a dataset"
date: 2022-07-24 19:46:39 +0200
source: linkedin
categories: thoughts
linkedin_urn: urn:li:activity:6953753189280083969
---

To train a classifier, you need a dataset. When you don't have a dataset, you build one by asking humans to classify your examples.

Either you have experts whom you trust, in which case each example is only seen once by a single human and their answer is considered as ground truth.

Either you go on Amazon Web Services (AWS) mechanical turk and pay a bunch of non experts whom you trust middly to classify the examples. In this case, to get better results you show the same example to multiple labelers.

At the end, you can pick for each example the most picked answer (you take the mode of your distribution of answer) as the ground truth, and train your model on that.

OR, you can use the distribution of the answer as it is, and calculate the loss with a softer version of your output layer, using a temperature T >> 1 in your softmax. This way you capture the human uncertainty and all the representational information it contains. This is exaclty what we do in knowledge distillation from a model to another, why not doing it from a human to a model.

Also, if you think you really cannot trust your labelers, you can do like Joshua C. Peterson et al. and show them an "attention check" every 20 examples, asking them to classify something obvious. When everyone is done labelling, you can throw the data coming from the ones who failed this attention check.
