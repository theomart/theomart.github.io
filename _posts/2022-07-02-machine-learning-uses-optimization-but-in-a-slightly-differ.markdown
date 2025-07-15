---
layout: post
title: "Machine learning uses optimization, but in a slightly differ"
date: 2022-07-02 11:45:56 +0200
source: linkedin
categories: thoughts
linkedin_urn: urn:li:activity:6953368812448563200
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
