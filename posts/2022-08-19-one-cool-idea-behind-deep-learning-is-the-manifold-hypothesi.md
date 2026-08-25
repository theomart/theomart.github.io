---
title: "The manifold hypothesis, explained with a shoelace"
date: 2022-08-19
lang: en
summary: "The manifold hypothesis explained with a tied shoelace: hidden layers untangle the data until a hyperplane can separate the two classes."
source: linkedin
legacy_url: /thoughts/2022/08/19/one-cool-idea-behind-deep-learning-is-the-manifold-hypothesi.html
---

One cool idea behind deep learning is the manifold hypothesis.

The manifold hypothesis says that your everyday data is observed in very high dimensional spaces (i.e. lots of features, lots of pixels), but they actually meaningfully sit on lower dimensional spaces called "manifolds", which are embedded in the high dimensional spaces.

When doing binary classification with NN, every hidden layer builds a new representation of the previous layer, squishing and squashing more and more what was initially your input space, until they can draw a hyperplane (i.e. high dimension version of a straight line) between the two classes.

They need to squish and squash because in the input space the data is generally not linearly separable. You can picture the two classes as being the two ends of your shoelaces tied together, that your NN needs to untie before drawing a straight line going through the middle of your shoe, leaving one end of the shoelace on the left side of the line and the second end on the right side

We use the notion of manifolds because they are locally euclidian, so that, among other things, you locally preserve this notion of straight stuff, allowing you to do such things.

I'm still trying to work this out, so if anyone spots something wrong in this way of thinking about it, please scream on me in the comments/in a message.
