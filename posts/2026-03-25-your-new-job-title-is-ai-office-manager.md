---
title: "Your new job title is AI office manager"
date: 2026-03-25
lang: en
summary: "Most of the day around a coding agent is plumbing. What compounds is the CLAUDE.md files, the skills, and the connectors that make a workspace usable."
---

The copy-paste between AI and your tools didn't disappear. It moved.

I run up to 9 Claude Code sessions in parallel on separate worktrees. I'm not new to this. But most of my day isn't prompting or coding. It's making the environment work. Pasting Slack messages into Claude because the connector isn't approved. Downloading Notion pages to drop into context because there's no integration. Copying CI logs by hand because the step output floods the context window. Renewing expired API tokens because nobody set up rotation. Clicking "approve" 40 times a day. The agent thinks. I plumb.

When something breaks, I don't fix it once. I fix it for next time. CircleCI output too verbose? I write a skill that pre-filters it before the agent loads everything. Agent doesn't handle a failing test well? I add instructions so it knows what to do before it hits the wall. I tried telling it "when a skill fails, rewrite the skill yourself." It tried. Got verbose. Wrote bloated instructions. Went in circles. So I refine the skills manually. I'm the self-improving loop. Though this is getting better. Agents are starting to understand their own tooling. The gap is closing.

The most valuable part of my work right now is none of the above. It's writing the CLAUDE.md files that define conventions. Refining skills, configuring tools. Pushing for connectors to get approved. Indexing internal docs so agents can actually find them. Making things accessible to AI that were only accessible to humans. Sometimes that's just exporting a Notion page because the integration doesn't exist yet.

The teams that make this work built the office first. Stripe gives each agent an isolated VM, no internet, no prod access. No approval needed. 1,000+ PRs per week. The model wasn't the hard part. The workspace was.

That's the job now. Building the workspace where agents can work without you in the room. Until the Slack connector gets approved, you're still copy-pasting status updates.

---

None of this is about the model. The [scaffolding around it](/en/writing/the-model-is-the-easy-part/) is what you own, and the skills you write for it [go stale on their own](/en/writing/most-skill-md-files-work-once/) unless someone keeps them.

## Sources

- TechCrunch, "Vibe coding turned senior devs into AI babysitters" (Sep 2025): https://techcrunch.com/2025/09/14/vibe-coding-has-turned-senior-devs-into-ai-babysitters-but-they-say-its-worth-it/
- Ethan Mollick, "Management as AI Superpower": https://www.oneusefulthing.org/p/management-as-ai-superpower
- Addy Osmani, "The 80% Problem in Agentic Coding": https://addyo.substack.com/p/the-80-problem-in-agentic-coding
- Silas Reinagel, "Your Job Is to Build the Workspace" (Jan 2026): https://www.silasreinagel.com/ai/agents/ai-engineering/productivity/automation/2026/01/16/your-job-is-to-build-the-workspace/
- Claude Code issue #4766 (agent keeps stopping): https://github.com/anthropics/claude-code/issues/4766
- Stripe Minions (1,000+ PRs/week): https://stripe.dev/blog/minions-stripes-one-shot-end-to-end-coding-agents
- DoltHub, "How I Use Multiple Agents in Parallel": https://www.dolthub.com/blog/2025-08-28-how-i-use-multiple-agents-in-parallel/
- HBR, "To Thrive in the AI Era, Companies Need Agent Managers" (Feb 2026): https://hbr.org/2026/02/to-thrive-in-the-ai-era-companies-need-agent-managers
