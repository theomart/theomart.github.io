---
title: "Most SKILL.md files work once"
date: 2026-03-28
lang: en
summary: "What makes an agent skill hold up past the first session: a trigger-clear description, a short file, scripts for deterministic work, a resumption contract."
---

Most SKILL.md files work once, in one session, with a fresh agent that has no other context loaded. Then they quietly degrade. The agent misses the trigger. The workflow goes stale. A session gets interrupted and the skill has no recovery path. Nobody fixes it because it's hard to tell whether the skill failed or the agent did.

Building skills that hold up requires the same discipline as building any production system: separation of concerns, durable state, and explicit failure modes. Most skills skip all three.

---

## The description is the most important line

The `description` field in a skill's frontmatter is what Claude uses to decide whether to invoke the skill. Write it poorly and the skill never fires when it should. Write it too broadly and it fires when it shouldn't, crowding out other tools.

A description that works has two parts: what the skill does, and when to use it. Not "transcribes audio" but "transcribe local audio files or remote audio URLs with Groq speech-to-text, use when a user wants fast speech-to-text and has audio files ready." The trigger condition is as important as the capability description.

The test: take your description and ask whether it would survive being read alongside 30 other skill descriptions. Does it uniquely identify the right moment to invoke this skill? Or does it describe a capability that three other skills also claim to have?

---

## Keep SKILL.md under 200 lines

This is an architectural constraint, not an aesthetic preference.

A SKILL.md file that grows past 200 lines has almost certainly mixed workflow instructions with reference material. The workflow (the sequence of steps the agent follows) belongs in SKILL.md. The reference material (schemas, examples, edge case documentation, API quirks) belongs in a `references/` subfolder, linked from SKILL.md.

When an agent invokes a skill, it loads SKILL.md into context. If that file is 800 lines of schema documentation and edge cases, the agent is paying context cost for information it may never need in this particular run. If that information is in a linked reference file, the agent fetches it only when relevant. SKILL.md describes the stages and names the scripts. Reference files document what the scripts expect, what they produce, and what can go wrong. The agent reads SKILL.md first and reference files only when it needs them.

---

## Scripts for deterministic work

Every skill that does more than one logical step should have scripts: separate Python files for each deterministic stage.

Deterministic work is anything where the output is fully determined by the input: building a manifest, packing batches, recording execution status, computing checksums, validating file formats. Scripts handle this. They're reproducible, they can be re-run without side effects, and they produce the same output given the same input regardless of which model invokes them.

Each script should do one thing, accept explicit path arguments rather than hardcoded paths, write output to files rather than returning it to the agent's context, and be re-runnable without corrupting prior state.

The agent invokes scripts in the sequence SKILL.md specifies. It doesn't make judgment calls about file I/O. It doesn't build manifests itself by reading source files. It calls the manifest script, reads the output file, and continues.

Without scripts, the agent rebuilds context from scratch on every run. That's slow and non-reproducible. Small variations in how the agent reads the source files produce different manifests, which produce different results downstream. Scripts eliminate that variance.

---

## The resumption contract

A skill without a resumption contract is a skill that can only run in one session.

The resumption contract is the answer to: if this skill's run is interrupted and a fresh agent session starts on the same task, what does it read first to understand where things stand?

The minimum: a `logs/next-steps.txt` file, updated at the end of every stage. One paragraph. What just completed, what needs to run next, where the relevant output files are. When a session resumes, it reads this file before doing anything else.

The full version adds an execution log: a JSONL file recording which tasks ran, what they produced, when they finished. Append-only. File-locked for concurrent writes. Before starting any stage, the agent checks the log to see what's already done and skips it.

Without this, interrupted runs restart from scratch. They redo work, sometimes producing duplicate outputs. They miss context from prior stages. They fail in ways that look like model failures but are actually infrastructure failures: the agent didn't have the information it needed to continue.

---

## Four things that make a skill hold up

Description written for trigger clarity with "use when" conditions. SKILL.md under 200 lines, with reference files for depth. Scripts for each deterministic stage, each doing one thing. A resumption contract so interrupted runs can recover.

The architecture that comes out of this isn't complex. It's specific about what each component does and where information lives. An agent that follows a well-built skill isn't doing creative work during the deterministic stages, it's executing a documented sequence against a durable file system. The judgment gets applied to the parts that actually require judgment, not to manifest building and batch packing.

Build the skill like it will outlive the session. It probably will.

The resumption contract is the part that separates a demo from a pipeline, and it has [its own piece](/en/writing/every-agent-works-in-the-demo/). Reference files exist for the same reason: what you load up front is [what the agent drowns in](/en/writing/your-agent-isnt-confused-its-drowning/).
