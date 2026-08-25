---
title: "The model is the easy part"
date: 2026-03-28
lang: en
summary: "Scaffolding moves task completion more than model choice does, and what a production agent harness has to hold up under."
---

Everyone picks the best model. That's the wrong problem.

LangChain swapped the infrastructure wrapper around the same underlying LLM on Terminal Bench 2.0. Same model. Different scaffolding. Task completion rate went from 52.8% to 66.5%. That's a 26% relative improvement, no new weights, no prompt magic. The model didn't change. The thing around it did.

That thing has a name: the agent harness. It's the infrastructure between the raw model and the actual task: the tools it has access to, how state persists between sessions, how it recovers from interruption, what context it receives and when. Most teams spend 80% of their effort picking and prompting the model. The harness gets the leftover 20%. The numbers suggest that ratio is backwards.

---

## What actually breaks in production

When an agent fails, the post-mortem almost always points to infrastructure, not capability. The agent loses track of what it already did. It gets handed a 40,000-token prompt when it only needed 800 tokens of targeted context. It has no way to pick up a multi-hour task after a session ends. It receives ambiguous instructions because nobody wrote down the operating rules.

None of these are model failures. A smarter model wouldn't fix them.

The failure I see most: agents that work beautifully in a demo session and fall apart when the session ends. There's no resumption contract. No state file. No handoff document. The agent starts fresh each time, refiguring out what was already done, sometimes redoing it, sometimes missing steps. You built a capable agent and no system to keep it oriented across time. Two different problems, and only one of them has anything to do with the model.

---

## The discipline this requires

Building a production-quality agent harness means separating two types of work that most implementations mix together: deterministic stages and model stages.

Deterministic work is file I/O, manifest building, state tracking, deduplication, batch packing. Scripts handle this. They're reproducible, they can be re-run without side effects, and they produce the same output given the same input. The model never touches this work directly.

Model work is judgment: extraction, synthesis, classification. Agents handle this. They receive compact, pre-processed inputs and produce structured outputs that go into files, not memory.

The mistake is letting the model do deterministic work. When an agent builds its own manifest from scratch on every run, reads raw source files instead of pre-computed summaries, or reconstructs state from conversation history rather than a state file, you've let it do janitorial work at model rates. Slow, expensive, non-reproducible. The split sounds obvious when stated. Almost nobody enforces it.

---

## What durable state looks like

A harness that survives interruption needs state files, not chat history. This is the most overlooked engineering requirement in agent systems, and it's also the simplest to get right once you stop assuming the conversation is the record.

Every multi-session pipeline needs three things. A manifest: JSON or JSONL, enumerates what work exists, built once by a deterministic script, read by every subsequent stage. When a session resumes, it reads the manifest first, not the prior conversation. An execution log: records which tasks ran, what they produced, when they finished, append-only and file-locked for concurrent writes. When you need to know what's already done, you grep the log. And a next-steps file: human-readable, one paragraph, updated at the end of every stage, telling the next session what just ran and what needs to run next. The handoff is in the file system, not in the conversation.

This treats sessions as stateless workers against a durable file system. Each one starts cold and still picks up exactly where the last one ended. The model's context window becomes irrelevant to continuity across sessions.

---

## Token discipline

The other failure mode is context bloat. An agent that receives everything fails differently than one that receives nothing: it pattern-matches instead of reasons, gets distracted by irrelevant material, produces lower-quality outputs at higher cost.

The fix is compact intermediate views. If the raw source is 200 conversations, you build a manifest that summarizes metadata: who, when, length, rough topic. The extraction agent reads the manifest, not the conversations. Only when it needs specific content does it fetch a targeted span.

Agents should receive the minimum context that makes the task completable. Build a summarization pass before the extraction pass. Build an index before the search pass. Never hand a full corpus to an agent and ask it to find things, because it will technically try, and the result will be expensive and inconsistent. Anthropic's guidance on long-running agents specifically calls out output swallowing and targeted context injection as core practices for exactly this reason.

---

## What this looks like as a skill

Claude Code formalizes this as a "skill": a SKILL.md file that teaches the agent a specific playbook for a class of tasks. Building a good skill forces you to apply every principle above.

A SKILL.md that works has a few non-negotiable properties. The description is written for trigger clarity, not feature completeness: it includes "use when" and "don't use when" conditions so the agent knows exactly when to invoke it. The file stays under 200 lines. If you need more, you link to reference files, you don't expand in place. The workflow describes discrete stages, not a wall of instructions.

Then there are scripts. Separate Python files for each deterministic stage: build the manifest, create the batches, pack the payloads, record the execution. Each script does one thing, accepts explicit path arguments, writes output to files, and can be re-run without side effects. The SKILL.md names the scripts and the order. The agent follows the order.

The architecture that comes out of this discipline isn't complex. It's just rigorous about what kind of work belongs where, where state lives, and how sessions hand off to each other.

---

## The uncomfortable part

Most teams build harnesses by accident. They start with a prompt, add a few tools, wire up some context, and call it an agent. It works in the demo. Then it slowly fails in production as edge cases accumulate and nobody has a principled way to fix them.

The teams that get it right treat the harness as the product. The model is a commodity, rented by the token. The infrastructure around it, the skills, the state management, the stage separation, the context discipline, that's what you own. That's what compounds over time as production failures get engineered back into the system.

A 26% improvement in task completion from changing the scaffolding around an unchanged model is not a small number. It's a measurement of how much was being left on the table by the surrounding system. The model capability question is mostly settled. The infrastructure question is not. That's where the work is.
