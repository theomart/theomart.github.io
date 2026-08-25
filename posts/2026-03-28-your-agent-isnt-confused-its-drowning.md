---
title: "Your agent isn't confused. It's drowning."
date: 2026-03-28
lang: en
summary: "Context bloat as the main undiagnosed failure mode: tool overload, raw corpora handed to agents, and subagents used as context firewalls."
---

Context bloat is the main undiagnosed failure mode in agent systems. The agent gets handed everything it might possibly need, fails to find the relevant parts, pattern-matches on the wrong signal, and produces output that looks plausible but is wrong. The model gets blamed. The problem is the context.

More tools loaded upfront degrades tool selection. More source material passed directly buries the signal in noise. More instructions in one prompt means the agent attends to the most statistically likely interpretation, not the right one. These are consequences of giving the model too much to process at once, a problem that scales with context length rather than in proportion to it.

---

## The upfront tools problem

Tool selection degrades as the number of available tools increases. When a model chooses from 5 tools, it reasons about which one fits. When it chooses from 200, it pattern-matches on tool names and descriptions. The quality difference is large and mostly invisible until you run a direct comparison.

Claude Code solves this at the architecture level with ToolSearch: a single entry-point tool whose only job is loading other tool definitions on demand. The agent starts with one tool, queries ToolSearch with a description of what it needs, and gets back 3-5 relevant definitions. The agent chose them based on the current task, not because they were all preloaded.

The naive approach is loading all tools upfront so the agent always has everything available. Most teams still do this. It produces worse results.

---

## The context bloat problem

The same principle applies to source material. An agent tasked with extracting structured data from 200 conversations should not receive 200 conversations. It should receive a manifest: metadata about those conversations, who they involve, when they happened, rough length, topic category. The agent reads the manifest, identifies which conversations are relevant, and fetches only those, targeted to the relevant spans.

This is extra work, done once, by a deterministic script that runs fast and is reproducible. The alternative is the agent reading all 200 conversations on every run, paying full context cost, producing inconsistent extractions because the relevant signal is buried in noise, with no way to tell which conversations actually contributed to the output.

Build a summarization pass before the extraction pass. Build an index before the search pass. The intermediate artifact is the point: it compresses the information space so the extraction agent receives a bounded, relevant input rather than the raw corpus.

---

## Subagents as context firewalls

The other tool for token discipline is subagent isolation. A long-running agent accumulates context across its work: tool outputs, intermediate results, prior conversation turns. By the time it's done with task 15 of 20, it's carrying context from tasks 1 through 14 that's irrelevant to task 15. The signal-to-noise ratio in its context window has degraded.

Subagents fix this by giving each bounded task a fresh context. The parent agent passes a compact payload: the specific inputs for this task, the schema for the output, nothing else. The subagent completes the task, writes the output to a file, and exits. Its context disappears. The parent reads the output file, not the subagent's context.

This treats subagents as context firewalls. Each one starts clean, does one thing, and writes its result to durable storage. The accumulated context of the parent never contaminates the focused work of the child. The child's accumulated context never bloats the parent.

The pattern works because the file system is the shared memory, not the context window. Any agent in any session can read the output files. No agent has to carry the context of prior work unless it explicitly needs it.

---

## What token discipline actually costs

The objection to progressive disclosure and subagent isolation is that they add complexity. Building a manifest script, defining a subagent payload schema, wiring up file handoffs between stages: this is more work than passing everything to one agent and asking it to figure it out.

The tradeoff is real, but the math is not close. An agent drowning in irrelevant context doesn't produce subtly worse results. It produces plausible-looking output that's wrong in specific, non-obvious ways, the hardest class of failure to catch in review.

Token discipline also compounds positively. A manifest built once gets reused across every stage. An index built once makes every subsequent search cheaper. The upfront cost is paid once. The benefit accrues on every agent invocation against that data.

The alternative compounds negatively. An agent that reads raw source on every run pays full context cost on every run. Its extraction quality degrades as context grows. Per-run cost increases with data volume. There's no floor on how bad it gets.

---

## The design question this forces

Token discipline forces a question most agent designs skip: what does this agent actually need to know right now?

Answering that for each stage produces a different architecture than "give the agent everything." You end up with a pipeline with explicit information contracts between stages, where each stage produces a specific artifact in a specific format, and the next stage reads that artifact and nothing else. Bounded, reproducible, debuggable.

That's a different system than a single context-stuffed agent. And it completes tasks reliably at scale in ways the stuffed version doesn't.
