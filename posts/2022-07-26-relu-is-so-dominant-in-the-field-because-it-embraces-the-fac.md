---
title: "Why ReLU dominates"
date: 2022-07-26
lang: en
noindex: true
summary: "ReLU dominates because a neural net only slices the input space hyperplane after hyperplane, and piecewise linearity is the non linearity that fits."
source: linkedin
legacy_url: /thoughts/2022/07/26/relu-is-so-dominant-in-the-field-because-it-embraces-the-fac.html
---

ReLU is so dominant in the field because it embraces the fact that all a neural network does is slice and dice the input space, linear transformation after linear transformation, hyperplane after hyperplane, layer after layer.

Piecewise linearity is maybe the only useful non linearity that can happen in a neural network.

Nothing smooth to see there. If you need some smoothness maybe you should go back to feature engineering it.
