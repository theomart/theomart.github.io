---
title: "Every agent works in the demo"
date: 2026-03-28
lang: en
summary: "The resumption contract: what a fresh session reads first, why conversation history is not state, and the test that separates a demo from production."
---

Every agent works in the demo. One session, fresh context, the task fits neatly in the conversation window. That's not a test of production viability. That's a controlled environment with every hard variable removed.

Production means the session ends. A user walks away, a server restarts, a pipeline runs overnight. The agent that worked in a 20-minute session has no documented state, no handoff notes, no execution log. A new session starts. The agent reads the task description, scans the file system for clues, starts over. Or worse, it finds partial results from the prior session, can't tell which parts are complete, and produces a mix of redone finished work and skipped unfinished work.

This failure mode has nothing to do with model capability. It's a missing piece of infrastructure: the resumption contract.

---

## What the resumption contract is

The resumption contract answers one question: if a fresh agent session starts on this task right now, what does it read first?

Most agent systems have no answer. The state is in the conversation history, which the new session doesn't have. Or it's scattered across partial outputs in the file system with no index. The agent starts fresh, rediscovers what was done, redoes some of it, and produces outputs that conflict with the prior session.

A minimal resumption contract is a `logs/next-steps.txt` file, updated at the end of every stage. It's overwritten each time with the current state: what just completed, what runs next, which output files were produced, any blockers. When a new session starts, reading this file is its first action. One paragraph of context, with pointers to the relevant artifacts. The agent doesn't reconstruct state from scratch.

The full version adds an execution log: a JSONL file where each completed task is a single line, with timestamp, task ID, what it produced, and exit status. Before starting any stage, the agent reads the log and skips tasks already marked complete. Append-only, file-locked for concurrent writes. It's the source of truth for what happened.

---

## Why conversation history is not state

Teams that skip explicit state management treat conversation history as state by default. This works for one session and falls apart on the second.

Conversation history is ephemeral by design. Sessions end, context windows fill. Even when history is explicitly passed forward, it brings along all the exploration and failed attempts and intermediate reasoning from the prior session, not just the final outcome. That's noise in the new session's context.

State files do the opposite: compact, current, explicitly structured. A manifest says what work exists. An execution log says what ran. A next-steps file says what to do now. Each readable in under ten seconds by a fresh agent that has never seen the task.

The practical difference: a five-session pipeline with proper state management produces the same outputs as a single-session run. Without it, you get five partially overlapping outputs with no clean reconciliation path.

---

## The demo hides session 2

The demo always runs in one session. The task is chosen to fit that session. The agent's behavior in session 1 of any multi-session pipeline is actually fine: reads the task, does the work, produces output. The resumption contract only becomes relevant starting in session 2.

This is why teams are consistently surprised when production agents fail. They tested thoroughly. The agent worked every time. But they only tested session 1. Session 2 is a different agent, in a different context, trying to pick up work it has no memory of.

The test that surfaces this: interrupt the agent partway through a run, start a fresh session with zero context about the prior state, and check if it resumes correctly. Almost no teams run this before deploying. The ones that pass it have a resumption contract. The ones that fail were testing a demo, not a production system.

---

## State design before agent logic

The practical consequence is that state design has to happen before writing any agent logic. The state files are the API between sessions. Define them clearly and the agent logic becomes mechanical: each stage reads inputs from specific files, does its work, writes outputs to specific files, updates the execution log, updates the next-steps file, exits.

Skip this step and you end up bolting state management onto an agent designed around conversation history. That works poorly. Fixing it usually means redesigning the pipeline from scratch.

Start with the state contract. What files does each stage produce? What does an execution log entry look like? What goes in the next-steps file after each stage? Answer those questions before writing a single line of agent logic.

The demo runs without any of this. Production pipelines that span more than one session don't. The gap is a design decision that most teams postpone until the first failure makes it urgent.

A skill is usually where the state contract gets written down, and [most SKILL.md files work once](/en/writing/most-skill-md-files-work-once/) because they skip it. The arithmetic that makes long pipelines fail regardless of the contract is in [the 99% problem](/en/writing/the-99-percent-problem/).
