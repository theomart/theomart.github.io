---
title: "The context envelope: what your LLM chat agent needs but isn't getting"
date: 2026-03-25
lang: en
summary: "The JSON payload a web app should wrap around every chat turn: six sections, the prompt injection and cache gotchas, and a ship order to follow."
---

Every framework has this pattern. None of them agree on what to call it. OpenAI's Agents SDK calls it `RunContextWrapper`. Google ADK calls it session state. LangChain calls it middleware context. Vercel AI SDK smuggles it through a `body` property on `useChat`. Intercom calls it Custom Data Attributes.

I'm going to call it the context envelope, because that's what it is: a structured JSON payload your web app wraps around every chat message to tell the LLM what's actually happening in the application right now.

Without it, your chat agent is blind. It can't see the screen. It doesn't know what page the user is on, what they're allowed to do, or what features their account even has access to. So it guesses. A user asks "how do I edit this?" and the model doesn't know what "this" is. It suggests a premium feature to a free-tier user. It tells a read-only viewer to click the delete button.

The fix is embarrassingly simple. Almost nobody does it well.

## What a context envelope actually is

It's a small JSON object assembled from your frontend state and backend services, sent alongside every conversation turn to the LLM backend. It's separate from the system prompt, conversation history, or RAG results. Just the structured metadata the model needs to ground its answers in what's actually happening on screen.

Here's a minimal one:

```json
{
  "schema_version": "1.0",
  "page": {
    "url": "/products/42/edit",
    "route_name": "product_edit"
  },
  "user": {
    "role": "editor",
    "permissions": ["edit_products", "view_reports"]
  },
  "locale_ui": "fr_FR"
}
```

Three sections. Maybe 200 bytes. This alone eliminates an entire class of bad answers.

Tobi Lutke, Shopify's CEO, coined the term "context engineering" in June 2025 to describe this broader discipline: the art of filling the context window with the right information so the task becomes plausibly solvable. The envelope is where context engineering meets the frontend. It's the contract between your web app and your LLM.

## How the big players do it

This pattern isn't theoretical. Every major AI-integrated SaaS already implements some version of it.

**GitHub Copilot Chat** sends the current file, cursor position, lines before and after the cursor, other open tabs, a local workspace index of all file paths and function signatures, and detected frameworks and dependencies. All tokenized and relevance-ranked before packaging.

**Intercom's Fin agent** reads customer attributes (plan type, account status, location), conversation data attributes, and referenced guidance rules. When a customer with `plan: enterprise` asks about SSO, Fin answers differently than for `plan: starter`.

**Notion AI** passes the current page content to the LLM, enforces the user's permission scope (the model "cannot see or use any information to which that user does not already have access"), and for complex requests, sends a ranked list of relevant pages.

**CustomGPT** provides explicit "Webpage Awareness" that summarizes the page the chatbot is embedded on, plus a `custom_context` string per embed like "This page describes Product X. Priority: highlight key benefits and pricing FAQs."

The pattern is universal. The naming is chaos.

## The six sections of a production envelope

I've built this pattern across production apps and settled on six sections. Each one is independent. Ship them one at a time.

**1. Page route.** The current URL and route name from your router. `"product_edit"` is stable across deploys. `"Edit Product - Blue T-Shirt (Summer Collection)"` is a prompt injection surface. Use the route name, not the page title.

**2. UI locale.** Only matters for the first message, before the user has typed anything. Once they write in Portuguese, the model should reply in Portuguese. You don't need a separate "conversation language" field. Models handle language mirroring naturally. Tell your system prompt: "greet in the UI locale, then match the user's language."

**3. Current entity.** What the user is looking at right now. Product ID 42, asset `hero-banner.png`, category "Summer 2026". Send IDs and identifiers, not display names. The backend can resolve details if the model needs them through tool calls.

**4. Tenant plan and capabilities.** What edition or plan the account is on. What modules are enabled. This prevents the single most annoying failure mode: the LLM enthusiastically walking a user through a feature their plan doesn't include. If you have a plan-to-features matrix anywhere in your codebase, serialize it.

**5. Feature flags.** Your LaunchDarkly or equivalent flags, resolved server-side. Combined with the tenant plan, the LLM knows exactly what's available and what isn't. Don't send raw flag names the user shouldn't see. Filter first.

**6. User permissions.** What the current user can actually do from your RBAC system. Oso, which specializes in authorization for AI agents, frames this as "permission risk is a function of the user, the agent, and the session so far." The model should never suggest actions the user can't perform.

What stays out: anything large, anything the model doesn't need for most turns. DOM content, full product catalogs, raw database records. The envelope should be small and cheap to compute on every single turn.

## The gotchas

### The context object is not the context

This catches people who've read the OpenAI Agents SDK docs. Their `RunContextWrapper` holds your application state and travels through the entire agent pipeline. But the SDK documentation says it explicitly: "The context object is **not sent to the LLM**. It is purely local."

Same pattern in LangChain's middleware and Google ADK's session state. You define a typed context object with fields like `user_role`, `cost_tier`, `environment`. You can read from it in tools, in dynamic prompt functions, in middleware hooks. But unless you explicitly inject those values into the system prompt or a message, the model never sees them.

The envelope is the data structure. Injecting it into the prompt is a separate step. Confuse the two and your model is technically context-aware in your code but completely blind at inference time.

### Your envelope is untrusted input

The envelope comes from the frontend. The frontend is the user's machine. Every field in that JSON is user-controlled input.

OWASP ranks prompt injection as the #1 vulnerability for LLM applications (LLM01:2025). The InjecAgent benchmark from UIUC tested this directly: even GPT-4 with ReAct prompting had a 24% attack success rate against indirect prompt injections in tool-integrated agents. With reinforced attacker instructions, that number hit 47%.

Never concatenate envelope fields into your system prompt as raw strings. Validate against a strict JSON schema. Treat route names as enums. If `route_name` isn't in your known routes list, reject the whole envelope.

```python
# Don't
prompt = f"The user is on page: {envelope['page']['url']}"

# Do
validated = validate_envelope(envelope, KNOWN_ROUTES)
context_block = f"<app_context>\n{json.dumps(validated.to_dict())}\n</app_context>"
```

Anthropic recommends wrapping injected data in XML tags so the model treats it as structured data, not instructions. That `<app_context>` wrapper is doing real security work.

OpenAI's MCP spec makes this even more explicit: metadata fields like `_meta["openai/userAgent"]` are "hints only; servers should never rely on them for authorization decisions."

### Your timestamp is destroying your cache

This one comes from the Manus team, who learned it the hard way running 100:1 input-to-output token ratios in production.

Prompt caching (Anthropic, OpenAI, Google all offer it now) works by caching the KV matrices for repeated prompt prefixes. But even a single-token difference invalidates the cache from that token onward.

A common mistake: including a timestamp precise to the second at the beginning of your system prompt.

```python
# Cache-destroying
system_prompt = f"Current time: {datetime.now().isoformat()}\n{base_prompt}\n{envelope}"

# Cache-friendly
system_prompt = f"{base_prompt}\n{envelope}\nCurrent time: {datetime.now().isoformat()}"
```

Move anything that changes frequently to the end of the prompt. Keep the stable parts (base system prompt + envelope) at the beginning. This also applies to JSON key ordering in the envelope. Non-deterministic key ordering breaks prefix matching. Use `json.dumps(envelope, sort_keys=True)`.

One developer documented going from $720/month to $72/month by structuring their prompt for caching. With Anthropic, cache reads cost 10% of normal input pricing. Structure the prompt right and turns 2 through N in the same session read the entire system-prompt-plus-envelope block from cache at 90% discount.

### Token budget is a zero-sum game

Google's production architecture for context-aware agents recommends a specific budget allocation:

| Layer | Budget | Contents |
|-------|--------|----------|
| Instruction | ~15% | System prompt, agent identity |
| Knowledge | ~25% | RAG results, domain docs |
| State | ~40% | Session state, conversation history, **envelope** |
| Task | ~20% | Current user request, immediate context |

Your envelope is competing for that 40% state budget alongside the entire conversation history. After 15 turns, history alone can hit 30,000+ tokens. A 500-token envelope on top of that starts crowding out the actual conversation.

Keep envelopes under 300 tokens. If your permissions array has 47 entries, send the 5 most relevant to the current page, not all of them. Jeremy Daly puts it well for commercial agent systems: "The working set should carry only what inference needs to act on."

### Lost in the middle is real

Stanford and Berkeley's "Lost in the Middle" paper (Liu et al., 2023) showed LLMs perform best when important information is at the beginning or end of the context. GPT-3.5's performance on multi-document QA fell below its closed-book baseline (56.1%) when relevant info was buried in position 10 out of 20 documents. Performance degraded 20%+ in the middle third across multiple models.

If your prompt structure looks like this:

```
[system prompt] → [envelope] → [conversation history] → [user message]
```

The envelope gets sandwiched as conversations grow. Two better options:

1. Prepend it to the system prompt (beginning of context, benefits from primacy)
2. Inject it right before the latest user message (end of context, benefits from recency)

I prefer option 1 combined with prompt caching: the system prompt + envelope as a stable cached prefix. The envelope gets primacy, the cache gets hit, everyone wins.

### Stale context will haunt you

User opens chat on `/products/42`. Five-turn conversation about product attributes. Navigates to `/categories/7`. Asks "how do I reorganize this?"

If you sent the envelope only on the first message, "this" still means product 42. If you send it every turn (which you should), the conversation history talks about products but the envelope now says categories.

Two approaches that work:
1. Send the envelope every turn and trust the model to handle the discontinuity. They're surprisingly good at this.
2. Detect route changes and inject a brief system note: "The user has navigated from the product page to the categories page."

One approach that doesn't: sending the envelope only at conversation start and hoping for the best.

### Entity context is harder than it looks

"Just send the current entity" sounds trivial. Then you start mapping route params.

`/products/42` is a product. `/categories/7/products` is... a category? A product list? `/assets/hero-banner` uses a slug, not an ID. `/settings/users/9/permissions` has a user entity nested inside a settings route.

You need a mapping from route pattern to "which param is the entity and what type is it." That mapping will have edge cases. Some pages have no entity. Some have two. Some have an entity that only exists in frontend state, not in the URL.

This is why entity context is item 5 on the priority list, not item 1.

## The golden nuggets

### LangChain's middleware shows where this pattern is going

LangChain 1.0 introduced middleware specifically for this use case. You define a context dataclass, then use a `@dynamic_prompt` decorator that modifies the system prompt based on context values at runtime.

For `user_role: admin`, the middleware injects "You have admin access. You can perform all operations." For `user_role: viewer`, it injects "You have read-only access."

They go further: a `@wrap_model_call` decorator lets you swap the model itself based on context. Production premium users get Claude Sonnet. Budget-tier users get GPT-4.1 Mini. The envelope doesn't just inform the prompt. It controls the entire inference pipeline.

I think this is where the whole pattern is heading. Today the envelope injects metadata into the prompt. In six months it's routing models, gating tools, and shaping agent execution end to end. Maybe that's overreach, but the LangChain team clearly thinks it's not.

### IDs and enums beat free text

Send `route_name: "product_edit"`, not `page_title: "Edit Product - Summer T-Shirt"`. Send `plan: "growth_edition"`, not `plan_description: "Growth Edition with advanced enrichment capabilities"`.

Route names survive page title rewrites. An entity named `"; ignore all previous instructions` is a real attack vector, but an ID of `42` is not. And `"product_edit"` is 2 tokens while `"Edit Product - Summer T-Shirt Collection (2026)"` is 10. Manus's production architecture reinforces this: ensure deterministic serialization, keep values machine-readable, avoid anything that changes without a deploy.

### Compute capabilities server-side

The frontend shouldn't be figuring out what features the tenant has, resolving feature flags, or combining RBAC with plan restrictions. That's all backend work.

The frontend sends the raw envelope (page route, locale, entity ID). The backend validates it, enriches it with server-side data, and injects the final version into the prompt.

This is what OpenAI ChatKit does: `server.process(body, context)` receives the frontend payload, the server enriches it, and the `respond` method gets the full context object. The client never sees capability data it shouldn't have.

### Version the schema from day one

```json
{ "schema_version": "1.0", ... }
```

One field. Saves you when you need to rename `locale_ui` to `ui_locale`, add a required section, or deprecate something. The backend checks the version and adapts. Old clients with schema 1.0 keep working when you ship 1.1.

### Test the envelope, not just the prompt

Nobody tests what happens when the envelope has unexpected values.

What if `permissions` is an empty array? What if `route_name` is a route the model has never seen? What if `plan` is `"free"` but `modules_enabled` includes a premium module because of a resolver bug?

Build a test suite that sends identical user questions with different envelopes and asserts the model's response changes appropriately. "How do I delete this product?" with `permissions: ["delete_products"]` should give instructions. Same question with `permissions: ["view_products"]` should tell them to ask an admin.

## Ship order: start with what you already have

**Week 1: Page route + UI locale.** Both values already exist in your frontend state. Read them, attach them. Your chat agent immediately becomes page-aware. CustomGPT calls this "Webpage Awareness" and sells it as a feature. You can build it in an afternoon.

**Week 2: Tenant plan.** If you have a plan-to-features mapping anywhere in your codebase, serialize it. The LLM stops recommending features users don't have. Intercom does exactly this with customer attributes.

**Week 3: User permissions.** Your RBAC data already exists. Serialize the relevant subset. Oso's approach: the agent only gets the same permissions as the user who invoked it, and as risk climbs, access narrows automatically.

**Later: Feature flags, entity context,** and whatever other sections your bad-answer logs tell you you need.

The context envelope isn't new. It's a name for something every team building LLM chat into a web app eventually figures out they need, usually after watching their model give confidently wrong answers for a few weeks.

You probably have all the data already. Route names, user roles, plan tiers, feature flags. It's sitting in your frontend state and backend services. The envelope just packages it up and delivers it where it matters.

Stop letting your LLM guess. Give it the envelope.
