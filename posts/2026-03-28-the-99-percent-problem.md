---
title: "The 99% problem"
date: 2026-03-28
lang: en
summary: "Compound error rates in long agent pipelines, the success table at 99, 95 and 90 percent per step, and why shorter segments beat better models."
---

99% reliable per step sounds good. Run it 20 times and you're at 82%.

That's the core structural problem with long autonomous agent pipelines, and it explains most of the failures teams blame on model capability. The math doesn't care which model you use. Compound error rates are a function of chain length, not intelligence.

The arithmetic: a 20-step pipeline at 99% per-step reliability succeeds 81.8% of the time end-to-end. Drop to 95% per step, which is actually quite good for real-world agent tasks, and 20 steps gets you to 36%. One in three pipelines completes correctly. The rest silently fail somewhere in the middle.

---

## Why teams don't see this coming

The demo pipeline has 5 steps and works reliably. The production pipeline has 20 steps because production tasks are more complex. That failure rate is a predictable consequence of the chain length decision, not a surprise, and most teams make that decision without running the math.

The specific failure mode is also hard to debug. A 20-step pipeline that fails 18% of the time doesn't fail consistently. It fails at step 7 one run, step 14 the next, step 3 on the third try. The errors look random but they're probabilistic: failure is distributed across the chain, not concentrated in one broken step.

Fix step 7, run it again, it fails at step 11. Fix step 11, it fails at step 4. The pipeline itself is the problem.

---

## The math at different chain lengths

| Steps | 99% per step | 95% per step | 90% per step |
|-------|-------------|-------------|-------------|
| 5     | 95.1%       | 77.4%       | 59.0%       |
| 10    | 90.4%       | 59.9%       | 34.9%       |
| 20    | 81.8%       | 35.8%       | 12.2%       |
| 30    | 74.0%       | 21.5%       | 4.2%        |

At 90% per-step reliability, a 30-step pipeline completes correctly 4% of the time. Chain length, not model quality.

Teams optimizing per-step accuracy while keeping chain length fixed are fighting the wrong battle. Push per-step reliability from 90% to 95% with significant engineering effort and a 20-step pipeline moves from 12% to 36% success. Or cut the chain to 5 steps and hit 59% without touching per-step accuracy at all.

---

## The architectural fix

More retries and better models don't solve compound error rates. Narrower tasks do.

A 20-step pipeline should be four 5-step pipelines with explicit handoffs between them. The handoff is a state file, not a prompt chain. Each segment runs to completion, writes its output, and stops. The next segment reads that output and starts fresh. If segment 2 fails, you rerun segment 2, not segments 1 through 20.

Production CI/CD systems figured this out a long time ago: stages with explicit artifacts between them, failure isolation at the stage level, reproducible inputs and outputs for each stage. The same principles apply to agent pipelines for the same reason. Compound failure in long sequential chains is a structural problem that architecture addresses better than reliability engineering does.

Debuggability improves too. When a 5-step segment fails, you have 5 steps to examine. When a 20-step pipeline fails, you have 20 steps of context to sift through, the failure often happened several steps before it became visible, and the model has already done significant work based on corrupted intermediate state.

---

## What the math means for agent design

Longer autonomous chains trade reliability for reduced handoff overhead. That tradeoff can make sense for low-stakes tasks. For tasks where failures are expensive to detect and correct, it usually doesn't.

Design agent pipelines with hard ceilings on step count per segment. 5 is good. 10 is the upper limit. Anything beyond 10 steps belongs in multiple segments with explicit artifacts between them.

Complex work structured as multiple bounded agents in sequence, each with a clear input and a clear output, has a completely different failure profile than one long agent doing everything in a single context window. The work is the same amount of work either way.

The 82% end-to-end success rate for a 20-step pipeline at 99% per-step is not a temporary limitation of current models. It's arithmetic. Models will get more reliable per step over time. The compound math won't.
