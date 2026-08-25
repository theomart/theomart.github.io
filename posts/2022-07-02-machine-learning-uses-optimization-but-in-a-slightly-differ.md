---
title: "Machine learning is not classical optimization"
date: 2022-07-02
lang: en
summary: "Why machine learning is not classical optimization: the target is generalization error, which changes how the objective and the data feed are handled."
source: linkedin
legacy_url: /thoughts/2022/07/02/machine-learning-uses-optimization-but-in-a-slightly-differ.html
---

Machine learning uses optimization, but in a slightly different approach than traditional optimization does.

Traditional optimization tries to optimize the objective function as much as possible.

Machine learning tries to minimize generalization error as much as possible.

For that, in ML we do things we wouldn't do in traditional optimization, such as:
- Checking the out of sample accuracy on a held out set from time to time during optimization.
- Modifying the way we feed data to optimize the objective function, e.g. random sampling with stochastic gradient descent rather than bare gradient descent.
- Modify the objective function itself to proxy the minimization of the generalization error.

Photo of Augustin-Louis Cauchy, who, among (many) other things, invented gradient descent in 1847. This frenchie contributed so much to physics and maths that Freudenthal said about him: "More concepts and theorems have been named for Cauchy than for any other mathematician".



hashtag
#machinelearning
hashtag
#optimization
