---
title: "18 lessons for building products on LLMs"
date: 2024-10-09
lang: en
summary: "Practical rules for building on LLMs: few shot sample counts, prompt splitting, chain of thought, guardrails, LLM as judge, and assertion tests."
source: linkedin
legacy_url: /thoughts/2024/10/09/18-lessons-to-develop-better-products-using-llms-use-n.html
---

🚀 18 lessons to develop better products using LLMs:

- Use n ~= 5 samples is a good rule of thumb in few-shot prompting. It prevents over-anchoring and ensures generalization. Some tasks benefit from dozens more, but many others will plateau after ~5.

- Trimming unnecessary details from the prompt can improve accuracy significantly. Excess context can introduce noise, therefore reducing model performance.

- Break up complex prompts into focused ones. Complex prompts can become unwieldy, leading to worse performance. By breaking them into smaller, task-specific prompts, each prompt becomes easier to manage, debug, and optimize.

- If you need to reduce the size of the examples because it doesn't fit in the context window or because it is too expensive, try with outputs only instead of full input-output pairs.

- To create diversity, don't increase temperature. Modify the prompt without altering its semantics, e.g., shuffle lists, change order of instructions, or use different vocabulary. Increasing temperature can cause "semantic drift." Another way is to use multiple prompts and sample from them.

- Chain-of-thought (CoT) prompting reduces hallucinations. Guiding the model through a step-by-step reasoning process before it returns the final output helps it avoid making errors or generating unsupported information. It's more effective with larger models.

- To fight hallucination, use prompt engineering as the first line of defense and factual inconsistency guardrails as the second. Even with good prompt engineering, it's impossible to guarantee 0 hallucination. Add self-consistency checks, external tools, and fact-based metrics/classifiers to catch them. For example, consider the LLM's output as a hypothesis and verify its consistency with NLI.

- Implement robust guardrails to filter or regenerate outputs. LLMs can produce errors or unsafe content, so guardrails are essential to catch these issues before they reach the user, ensuring the model’s outputs remain safe and appropriate.

- When using LLM-as-judge, prefer pairwise comparison over assigning individual scores. Only use absolute measures when you really need to capture a full range of output quality or when the quadratic scaling of pairwise comparison becomes a problem.

- Use LLM-as-judge cautiously, especially when accuracy is critical. LLM judges have biases, struggle with mathematical reasoning, and don't capture subtle linguistic nuances well.

- Implement assertion-based unit tests on real data. Unit tests help maintain consistent output quality by ensuring the model’s responses adhere to specific criteria, such as including key phrases or staying within word count ranges. Beware of overfitting to your test cases. Get a human to check the output from time to time.

7 more in the comments.
