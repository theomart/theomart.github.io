---
layout: post
title: "Learning rate schedules allow for changing the learning rate"
date: 2022-08-02 15:26:31 +0200
source: linkedin
categories: thoughts
linkedin_urn: urn:li:activity:6938489263105708032
---

Learning rate schedules allow for changing the learning rate while training, instead of having the same learning rate for every batch of every epoch.

If you had a radar that only told you the direction of the object you are trying to find, and that object could be anywhere in the world, you wouldn't have constant steps. First you would start by huge steps in the right direction, let's say 1000km, and when you would pass the object you would turn around and take a smaller step size, for example 500km. You would reduce the step size again and again until finding the object, maybe down to 10 or so meters. You can see it would take way too long to keep a step size of 10m during the whole process, especially if the object is on the other side of the planet. Symetrically, you would never find the object if you adopted a step size of 1000km all the way.

Gradient descent only gives you the direction of the lowest point of your objective function, not the distance to it, so it's for you to choose how big of a step you want to do at every weight update. This choice can make the difference between converging and not converging, help you win precious points on your accuracy and shorten your taining time.

There are multiple techniques to schedule learning rates here are a few worth checking:
- Exponential decay
- Step drop adjustment
- Cosine annealing
