---
title: "The MCP paradox"
date: 2026-03-25
lang: en
summary: "A year of MCP: the integration problem it solved, the context bloat it created, the CLI comeback, and why the real constraint on agents is attention."
---

## Part I: A Brief History of Tool Chaos

Before November 2024, connecting AI models to external tools was a nightmare.

Every AI application needed custom integrations with every tool it wanted to use. OpenAI had one schema format for function calling. Anthropic had another. Google's Gemini spoke its own dialect. If you wanted your app to work with multiple providers, you maintained parallel implementations. If you wanted to connect ten AI products to a hundred tools, you were looking at a thousand separate integrations.

Engineers called it the M×N problem. It was slow, expensive, and created the kind of technical debt that makes senior engineers quit.

**July 2024.** David Soria Parra, working on internal developer tooling at Anthropic, grew frustrated. He'd come to love Claude Desktop, but something fundamental was broken. The AI could write code, analyze documents, and hold sophisticated conversations, but it couldn't do anything. It lived in a glass box, unable to touch the outside world.

Parra and his colleague Justin Spahr-Summers started building a prototype.

**November 25, 2024.** Anthropic open-sourced the Model Context Protocol. The idea was almost embarrassingly simple: create one standard way for AI models to talk to external tools. Instead of M×N integrations, you'd need M+N. The industry went crazy.

**March 2025.** OpenAI announced full MCP support. The protocol had crossed the competitive moat.

**May 2025.** Microsoft and GitHub joined the MCP steering committee. Enterprise adoption accelerated.

**Summer 2025.** The first signs of trouble emerged. Power users connecting five or six MCP servers noticed Claude getting sluggish. Not just slow—dumb. It would pick wrong tools, miss obvious context, behave like it had forgotten how to do its job.

**August 2025.** Mario Zechner published benchmarks showing CLI tools outperforming MCP by 33% on token efficiency. Armin Ronacher, creator of Flask, demonstrated that the `gh` command beat the GitHub MCP server on identical tasks.

**September 2025.** Cloudflare published research showing LLMs performed better writing code to call APIs than using tool-calling syntax directly.

**October 2025.** The RAG-MCP paper dropped, demonstrating 3x accuracy improvements through retrieval-based tool selection.

**November 2025.** Anthropic shipped MCP Tool Search in Claude Code, cutting token overhead by 85%. A research paper revealed 42% of servers in the Smithery Registry had cryptographic vulnerabilities.

**December 2025.** Anthropic donated MCP to the Linux Foundation's new Agentic AI Foundation. The protocol had won—but not without scars.

In twelve months, MCP went from solving a problem to creating one to spawning an ecosystem of solutions. That's the story.

---

## Part II: The Bloat Crisis

MCP clients load all tool definitions upfront. Every server you connect adds hundreds or thousands of tokens before you've typed a single word.

The numbers were brutal. Anthropic's own testing found that a modest five-server setup consumed 55,000 tokens just in tool descriptions. The GitHub MCP server alone ate 55,000 tokens—nearly a quarter of Claude Sonnet's entire context window.

Scott Spence ran the numbers on his personal setup. With all his MCP tools enabled, he was hitting 143K of 200K tokens immediately. MCP tools consumed 82,000 tokens—41% of his total capacity—leaving just 12,000 tokens of actual breathing room. He'd upgraded to a mansion-sized context window and MCP had filled it with furniture before he moved in.

The irony was sharp. MCP solved the integration problem by creating a standardization problem, then the standardization problem created a bloat problem. Users who connected the most tools got the worst experience. The power users were being punished for being power users.

Editor vendors noticed early and implemented hard caps. Cursor: 40 tools maximum. GitHub Copilot: 128. Windsurf: 100. If you exceeded these limits, tools simply became inaccessible. These weren't elegant solutions. They were tourniquets.

---

## Part III: The CLI Renaissance

Meanwhile, a quieter truth was emerging from the benchmarks. Sometimes the old ways were better.

Armin Ronacher ran a direct comparison: the GitHub CLI versus the GitHub MCP server. Same operations. Same model. The CLI consumed far less context and got to the result faster. It wasn't close. His experiment with `gh` got the actual diff with 71 lines of changes—something that both the REST API and the official GitHub MCP failed to deliver.

Mario Zechner's formal benchmarks in August 2025 confirmed it. For developer debugging workflows, CLI provided 33% better token efficiency than MCP. The margin was 77 vs 60 points. The CLI-first approach passed specific tools into context only when needed, rather than loading entire server definitions upfront.

The practical takeaway became folk wisdom among power users: if a CLI tool exists for something, use the CLI. The GitHub MCP defines 93 tools and consumes 55,000 tokens. The `gh` command does the same work with near-zero overhead and it's already baked into most models' training data. Some MCPs genuinely don't add much value over established CLI tools. They just pollute context without benefit.

The distinction that emerged was this: CLI tools are for your personal workflow. You build scripts, put them in a Justfile, tell your agent to use that file. It's the most token-efficient approach because it gives the model only what it needs. MCP servers are for sharing. When you want a colleague or a non-technical client to use your tools, walking them through an MCP server is simpler than sending folders of scripts. MCP makes tools portable and plug-and-play.

The two aren't competing. They're complementary. The problem was that everyone treated MCP as a replacement when it was really an addition.

---

## Part IV: The Hype Reckoning

MCP arrived with the kind of breathless enthusiasm usually reserved for cryptocurrency launches. "The USB-C of AI!" "A genuine breakthrough!" The marketing worked too well. Within months, developers were wrapping everything in MCP servers—including things that had no business being wrapped.

The skeptics noticed early. "Is MCP truly revolutionary, or just a fancy rebrand of what we already had?" was the question nobody wanted to ask in public. The uncomfortable answer: for many use cases, function calling was always enough.

Here's the thing most MCP evangelists don't mention: LLMs have no idea what MCP is. To the model, there's no difference between "regular" tool calling and MCP. It sees a list of tool definitions. It doesn't know or care what protocol generated them. The standardization happens entirely outside the model's awareness.

Function calling keeps everything in one place. No extra processes, no protocol to learn. For trusted internal tools or personal projects, its simpler security model is adequate. If your app runs in a secure environment or you're building a private assistant, managing separate MCP servers is unnecessary overhead.

The rule of thumb that emerged: when you need to retrieve data from a predefined workflow, use APIs directly. When you need dynamic discovery across multiple AI clients, consider MCP. But most developers weren't building multi-client ecosystems. They were building single applications with a handful of tools. For them, MCP was a solution looking for a problem.

The security implications made this worse. MCP servers often run with broad privileges. In local deployments, they inherit the user's permissions—meaning they can read and write files with impunity. Authentication in the MCP specification is optional. The SDK doesn't include built-in authentication mechanisms. Deploying a server without proper auth increases the risk of unauthorized access, resource misuse, and denial of service attacks.

A research paper in late 2025 found that 42% of servers in the Smithery Registry had cryptographic misuse. Case studies revealed leaked API keys, insecure DES/ECB implementations, and MD5-based authentication bypasses. Python servers had a 34% misuse rate. Developer Tools and Data Science categories accounted for over half of all security issues.

Even without malicious actors, unintentional data exposure was common. A user might connect Google Drive and Substack MCPs to Claude, use it to draft a blog post about a recent medical experience, and watch helplessly as Claude autonomously reads relevant lab reports and includes unintended private details. The model was being helpful. That was the problem.

Tool poisoning became a real concern. Attackers could hide harmful commands in MCP tool descriptions—invisible to users but visible to models. A tool description might look normal ("Analyze this file") while secretly copying sensitive data to external servers. Supply chain attacks got their own category: "rug pulls," where an MCP server passes initial approval then updates with malicious tool definitions.

The practical advice became grimly simple: treat every third-party MCP server as a potential threat. Lock tools to specific verified versions. Separate tools so a compromised one can't affect others. Apply the principle of least privilege ruthlessly. Or, increasingly: just don't use MCP when you don't need to.

---

## Part V: The Cognitive Mismatch

The deeper issue was that MCP had optimized for the wrong thing. It made integration easy, but integration was never the hard part for AI agents. The hard part was selection. When you give an LLM a hundred tools, it doesn't get a hundred times more capable. It gets confused.

Waleed Kadous, a veteran of Google's AI efforts, wrote a piece in December 2025 titled "MCP Went Sideways." His diagnosis was damning: LLMs are actually bad at tool calling. The training data disparity is massive. Models have seen vastly more real-world code than contrived tool-call demonstrations. When you present tools as function calls, you're forcing the model to work in its weakest mode.

Cloudflare and Anthropic arrived at essentially the same conclusion within weeks of each other—Cloudflare on September 26, Anthropic on November 4. Both published technical posts reaching the same radical insight: we've been doing this backwards. Instead of forcing LLMs to speak in the synthetic language of function calling, just let them write actual code.

The logic was straightforward. We spent years training models on every scrap of code humanity has ever written—Stack Overflow answers, GitHub repositories, programming textbooks, documentation. They're fluent in Python, JavaScript, TypeScript. Then, when it comes time to use these models as agents, we ask them to generate perfectly formatted JSON objects wrapped in XML tags, specifying function names and parameters in a rigid schema they've barely seen during training.

Writing code to chain API calls together? That's the mother tongue. JSON function descriptors wrapped in XML? That's a foreign language they learned in a weekend.

Cloudflare converted MCP tools into a TypeScript API and asked models to write code that called the API instead of calling tools directly. The results weren't subtle. Agents handled more tools, more complex tools, and made fewer mistakes.

The tradeoff is real. With tool calling, you audit the tools. With code execution, you audit the code and the execution environment. Static analysis of LLM-generated code is still an open problem. Cloudflare has V8 isolates because they're Cloudflare—they spent years building that infrastructure. For everyone else, you're looking at setting up sandbox runtimes, resource limits, monitoring, logging. But for high-scale agent platforms, the prediction is that most will adopt code execution within 18-24 months.

---

## Part VI: The Solutions

The solutions that emerged in late 2025 shared a common theme: laziness. Not the pejorative kind—the engineering kind. Don't load what you don't need. Don't process what you won't use.

### Claude Code: The Layered Approach

Anthropic built an entire hierarchy of context isolation mechanisms.

**MCP Tool Search** became the default. Instead of loading all tools upfront, the system dynamically discovers relevant tools on demand. When MCP tool descriptions exceed 10K tokens, tools get marked with `defer_loading: true`. Claude receives a Tool Search tool instead of all the definitions. Traditional approach: 77K tokens before any work begins. With Tool Search: 8.7K tokens. An 85% reduction. Accuracy on tool selection jumped from 49% to 74% on Opus 4, and from 79.5% to 88.1% on Opus 4.5.

**Skills** became auto-invoked context providers. Unlike simple slash commands, skills can include multiple files—reference documentation, scripts, templates, utilities. Claude automatically loads them based on description matching with the conversation. The key constraint is a character budget: 12,000 characters by default. Exceed it and skills get excluded. The system forces you to be selective.

**Subagents** took isolation further. Claude Code can spawn lightweight instances that execute tasks in parallel, each running in its own context window with a custom system prompt and independent permissions. The main conversation thread stays clean. When you need to run tests, fetch documentation, or process log files—operations that produce large amounts of output—you delegate to a subagent. The verbose output stays in the subagent's context. Only the summary returns to your main conversation.

The architecture is fractal. Context isolation at the tool level (lazy loading), the workflow level (skills), and the execution level (subagents). Each layer prevents pollution from the layer below.

### Goose: The Code Execution Pivot

Block's Goose took a different philosophical approach with "Code Mode." Instead of giving the model a hundred tool definitions, you give it three meta-tools: search for modules, read module documentation, and execute code. The model discovers what it needs progressively, writes a script to chain operations together, and runs everything in one execution.

What's clever is that Code Mode is itself an MCP server. It wraps your other extensions and exposes them as JavaScript modules. The LLM sees only three tools instead of eighty. Intermediate results never flow back to the model unless they're needed. Tokens saved, context preserved, sensitive data unexposed.

### Cursor: Limits and Rules

Cursor implemented the hard cap early: 40 MCP tools maximum. They also built the `.cursorrules` system—project-level instructions that persist across conversations, stored in `.cursor/rules`. The recommendation is to keep rules under 500 lines, write them in "martial arts" tone (short, direct, no fluff), and split bloated files into separate `.mdc` files that activate only when relevant.

But Cursor users discovered a problem: context drift. As the conversation grows, the model forgets the rules. No matter how well you write them, after a few messages they get ignored. The workaround is explicit reinforcement—comments like "remember the rules" or "read the rules again." Inelegant but necessary.

### GitHub Copilot: Virtual Tools and Embeddings

GitHub Copilot faced the same constraint: 128 tools maximum. Their solution was more sophisticated. They built "virtual tools"—functional groupings of similar tools under one umbrella that the chat agent can expand as needed. Think of them as directories containing related tools. The model gets a general sense of what's available without hundreds of names flooding the context.

They paired this with embedding-based clustering. Their Copilot embedding model generates vectors for each tool, groups them using cosine similarity, then caches the embeddings and summaries locally. Across benchmarks like SWE-Lancer and SWEbench-Verified, these changes improved success rates by 2-5 percentage points and reduced response latency by 400 milliseconds on average.

### Kiro: Dynamic Powers

Kiro, AWS's entry into the agentic IDE space, took perhaps the most radical approach with "Powers."

Typical AI coding tools load every possible capability upfront—burning computational resources and overwhelming the AI with irrelevant information. Kiro inverts this. When a developer mentions "payment" or "checkout," the Stripe power activates automatically, loading its tools and best practices into context. When they shift to database work, Supabase activates while Stripe deactivates. The baseline context usage when no powers are active approaches zero.

Each power packages three components: a POWER.md steering file explaining what tools are available and when to use them, the MCP server configuration connecting to external services, and optional automation hooks. It's MCP made dynamic.

### Zed: Radical Transparency

Zed built AI as a native component rather than a bolt-on. The Agent Panel exposes the entire LLM request as editable text. Code snippets, conversation history, file contents—all visible, all modifiable using familiar editing tools. They surface token consumption near the profile selector. When you approach the model's context window, a banner suggests starting a new thread with the current one summarized. Transparency as a design principle.

### RAG-MCP: The Academic Contribution

A paper published in May 2025 introduced a three-step pipeline. First, a lightweight retriever encodes the user's task and performs semantic search over a vector index of MCP metadata, returning the top-k candidates most similar to the task. Second, an optional validation step generates few-shot examples to test compatibility. Third, only the single best MCP description gets injected into the prompt.

Results: RAG-MCP cut prompt tokens by over 50% and more than tripled tool selection accuracy—43.13% versus 13.62% baseline. Because tool information lives in an external index, new tools can be incorporated by updating the index without retraining the LLM.

---

## Part VII: Lessons

There's a lesson here about standards and their unintended consequences.

MCP succeeded because it solved a real problem that hurt real developers every day. The M×N integration nightmare was expensive, fragile, and annoying. A universal protocol was obviously better than the chaos that preceded it.

But standards have gravity. Once MCP became the default way to expose tools, everyone started building MCP servers. The ecosystem exploded—thousands of servers, hundreds of tools per popular service. Nobody asked whether agents could actually handle that many options. The protocol made it easy to add tools, so people added tools.

This is how success creates failure. The better MCP worked, the more people used it. The more people used it, the more tools appeared. The more tools appeared, the worse the experience got for anyone who wanted to use them all.

The solutions—lazy loading, code execution, skills, subagents, powers, virtual tools, embedding clustering, RAG retrieval—are really admissions that the original model was incomplete. MCP handled the transport layer brilliantly. It said nothing about the cognitive layer. How should a model decide which tools to use? How should it handle ten tools versus a hundred? How should it chain complex operations without polluting its own context?

Those questions weren't MCP's to answer. But someone had to answer them. And for about a year, nobody did.

The current state is a patchwork, but a functional one. Claude Code has Tool Search, skills, and subagents. Goose has Code Execution. Cursor has limits and rules. Copilot has virtual tools and embedding clustering. Kiro has Powers. Zed has transparency. Everyone found their own approach to the problem MCP created by solving a different problem.

This is probably fine. Standards don't need to solve everything. USB-C doesn't specify what data you should send through it, just how to send data. MCP doesn't need to specify how models should select tools, just how tools should be exposed.

But the year of bloat taught us something important. The constraint on AI agents isn't access to tools. We solved that. The constraint is attention. Models can only reason effectively over so much context. Fill that context with tool definitions and you've traded capability for optionality.

The engineers who figured this out fastest were the ones building products, not protocols. Cursor hit the wall and added limits. Claude Code hit the wall and built search. Goose hit the wall and invented code execution. Kiro hit the wall and invented powers. Practice ran ahead of theory, as it usually does.

And sometimes the answer was simpler than anyone expected. Use the CLI. The `gh` command has been there all along, consuming near-zero tokens, already in the training data, doing exactly what the fancy MCP server does but without the overhead. Not every problem needs a new solution. Some just need you to remember the old ones.

MCP's next chapter will probably involve standards for tool discovery and selection, not just tool definition. The protocol will grow to encompass what the ecosystem learned the hard way. And then, inevitably, those new features will create new problems that some frustrated engineer will solve with another clever hack.

That's how progress works. You solve the problem in front of you and create the problem behind it. The measure of a good solution isn't whether it creates new problems—they all do. It's whether the new problems are better than the old ones.

Having too many tools is a better problem than having no way to connect them. We'll take it.

The constraint underneath all of this is attention, and what it looks like when an agent runs out of it is in [a separate piece](/en/writing/your-agent-isnt-confused-its-drowning/). The tool descriptions you load up front spend the same budget as [the skills you write](/en/writing/most-skill-md-files-work-once/), which is the part most teams never measure.
