---
title: "Tribal knowledge never reaches the coding agent"
date: 2025-03-01
lang: en
summary: "Coding agents only get the context you hand them, while human developers pull from Slack, meetings and hallway talk that never reaches a repo."
source: linkedin
legacy_url: /thoughts/2025/03/01/you-should-encourage-employees-to-wear-meta-glasses-to-captu.html
---

You should encourage employees to wear Meta glasses to capture tribal knowledge for AI coding agents. And here is why ⬇️

Documenting code sounds obvious. But when it isn’t documented, developers have to rely on other means. They ask senior team members who’ve been around the longest, rummage through files, and hunt down scattered documentation in GitHub, Notion, Slack messages—anything they can find. That’s how they gather the context needed to get things done.

When comparing AI coding—and especially autonomous coding—to a human developer, the comparison feels unfair. A human coder can spend as long as they want gathering context. Meanwhile, whether it’s AI-assisted or autonomous coding, AI only gets whatever context we include in the prompt or that it retrieves automatically from the codebase. Tools use hybrid retrieval—exact match, semantic search, and often language server protocols (LSPs) to look up function signatures, objects in use, etc. But beyond that, it doesn’t have the deep understanding that a human can develop over time.

Look at Cursor, for example. They don’t charge you by token usage. They pay by token, while you pay per request to the model. That single request can include as many tokens as Cursor decides are needed. But cost also matters to them—if they include more tokens, you pay the same, but Cursor has to pay more. So they balance relevance against expense and sometimes limit how much context the AI actually sees.

Today, codebases can be huge and fragmented—a known limitation for AI that will improve over time. Some things are implicit, making it difficult for AI to piece together the full picture when logic is spread across multiple files.
One approach people have suggested is giving AI a kind of short-term long-term memory. Some users of Cursor already do this by defining rules that ask the AI to note patterns specific to their team or company in a separate file, then read that file before starting a task—so the AI can revisit what it’s learned so far.

In contrast, human developers pull from a range of sources. For AI it's not that easy. GitHub READMEs in the same repo are straightforward to consult. Notion docs and Slack messages need connectors—and although some companies are tackling that, these integrations still aren’t very mature. Some folks use MCP servers, and I’ve even seen Cursor hooked into Linear via MCP. It gets trickier with Google Meet or Zoom meetings, which need transcripts processed before the AI can use them. Finally, there are face-to-face conversations, many of which happen off the record—at a bar or a team event.

Unless your company makes you wear Meta glasses so nothing ever slips by, that knowledge never reaches the AI.
