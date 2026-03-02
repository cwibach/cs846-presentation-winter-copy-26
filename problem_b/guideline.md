# Code Review Guideline

<!-- ## Guideline: Provide full context when asking for code review

**Description:**  
Design your prompt so the LLM receives a clear “job description” before reviewing code. Include sufficient and relevant context—goal of the change, constraints the code must satisfy, and what aspects you want reviewed—so the problem space is constrained and the feedback is targeted.

**Reasoning:**  
This serves several purposes.

- **Clarifies intent.** The process of writing goal, constraints, and review focus forces you to articulate what the change is for, what must be preserved, and what “good” feedback looks like.
- **Reduces generic feedback.** Without context, models often default to generic comments (naming, style, add type hints). With goal and constraints, the model can tie feedback to your actual PR (e.g. “don’t expose internal `id` here,” “add timeout to this call”).
- **Improves actionability.** Explicit review criteria (correctness, error handling, security, performance, edge cases) yield concrete, actionable comments rather than vague suggestions.
- **Structured prompts perform better.** Prior work on prompt patterns suggests that structured, high-information-density prompts lead to more correct and evaluable outputs than free-text “review this” prompts.

**Good Example:**

```
You are reviewing a code / pull request.

Constraints: Must not expose internal user IDs to the front end; API calls should timeout after 2 seconds; dashboard must stay responsive.

Review the following code for: correctness, error handling, security (what we expose to the UI), performance (e.g., unnecessary API calls), and edge cases. Give actionable comments as if posting on GitHub.
```

**Bad Example:**

```
Please review the code above and give feedback on correctness, security, and edge cases.
``` -->

<!-- 
<<<Rethinking Code Review Workflows with LL Assistance: An Empirical Study>>>


Guideline: Request AI-Led Contextual Summaries Before Issue Detection

Description:
When asking an LLM to review a pull request, first request a structured summary of the PR’s intent, affected components, and major changes before asking for issue detection. Use the summary to guide deeper inspection.

Reasoning:
The study found that developers struggle with context switching and insufficient contextual information when reviewing pull requests, especially large or unfamiliar ones. Participants preferred AI-led summaries that provided an overview before detailed analysis. This reduced cognitive load, improved understanding, and increased perceived usefulness of the AI assistant. Requesting a contextual summary before issue detection aligns with the empirically preferred “AI-led” review mode identified in the paper.

Good Example:
This is a pull request in a service I’m not familiar with.
First:
- Summarize what the PR is trying to achieve.
- Identify which components are affected.
- Highlight complex or high-risk areas.
Then provide specific review comments.

Bad Example:
Review this pull request and list problems.
 -->

 <!--
<<<Automated Code Review in Practice>>>


Guideline: Filter and Prioritize Automated Comments to Reduce Noise

Description:
Configure or prompt automated review tools to focus on high-impact issues (correctness, security, performance) and avoid low-value or out-of-scope suggestions.

Reasoning:
26.2% of automated comments were labeled “Won’t Fix” or “Closed.” Developers reported frustration with irrelevant or trivial comments and recursive re-reviews that slowed development. The study shows that unnecessary comments increase PR closure time and cognitive overhead. Signal-to-noise ratio directly affects developer trust and productivity.

Good Example:

Review this pull request focusing only on:

correctness

potential bugs

performance regressions

security risks
Do not suggest stylistic or refactoring improvements unless critical.

Bad Example:

Review this PR and suggest all possible improvements.
 -->


 <!--
<<<Blog1: Unlocking the full power of Copilot code review: Master your instructions files>>>


Guideline 2: Use Structured Rules (Headings + Bullet Points)
Description

Structure your code review prompts using headings and bullet points instead of long paragraphs.

Reasoning

The blog emphasizes that structure improves how Copilot processes instructions. LLMs respond better to clear sections and enumerated rules. This reduces ambiguity and improves comment consistency.

Good Example:
Review Focus

Correctness

Performance regressions

Security risks

Constraints

Do not suggest formatting-only changes

Assume this is production code

Bad Example:

This is production code and I want you to review it carefully for correctness performance and security but also keep in mind not to change formatting and just generally give useful suggestions.
 -->


 <!--
<<<<<Detecting malicious pull requests at scale with LLMs>>>>>


Guideline 6: Break Large PRs into Logical Segments
Description

When reviewing large diffs, instruct the LLM to analyze changes file-by-file or chunk-by-chunk before producing a final verdict.

Reasoning

The blog shows performance degradation with large context windows and solved it with recursive chunking. Large PRs can hide small malicious inserts inside huge refactors.

Good Example

Analyze this PR file-by-file.
For each file:

Identify security risks

Summarize intent

Then provide an overall classification.

Bad Example

Review this entire 10,000-line diff at once.

(Leads to shallow or degraded analysis.)
 -->








 <!--
<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<FINAL GUIDELINE>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
-->


## Guideline: Use a Structured, Context-First Review Prompt

### Description

When prompting an LLM for code review, first have it produce a structured summary of the pull request (intent, affected components, and high-risk areas). Then, give explicitly scoped review criteria (for example, correctness, security, and performance) as clear bullet-point instructions.

### Reasoning

This guideline merges the strongest findings across sources:

- **Rethinking Code Review Workflows (empirical study)**: Developers preferred AI-led summaries before issue detection to reduce cognitive load and improve contextual understanding.
- **Automated Code Review in Practice**: Unfocused, noisy feedback increases PR closure time and reduces trust; review criteria must be scoped to high-impact areas.
- **Copilot Instructions blog**: Structured prompts (headings + bullet points) improve consistency and reduce ambiguity in LLM outputs.

Together, these findings show that effective LLM-assisted code review requires:

- Context understanding first  
- Clear scoping of review focus  
- Structured prompt formatting  

### Good Example

You are reviewing a pull request.

**Step 1 — Context summary**

- Summarize the intent of the PR.  
- Identify affected components.  
- Highlight complex or high-risk areas.  

**Step 2 — Focused review**

Review only for:

- correctness  
- security risks  
- performance regressions  

Do not suggest stylistic changes unless they affect correctness.

### Bad Example

Review this pull request and suggest improvements.





## Guideline: Explicitly State Assumptions and Non-Goals

### Description

When prompting an LLM for code review, explicitly state what assumptions the model should make and what it should **not** evaluate. Clarify system boundaries, trust model, and review scope exclusions to prevent overreach and hallucinated concerns.

---

### Reasoning

Even when given context, LLMs may:

- Assume missing system components  
- Critique hypothetical architectures  
- Suggest redesigns outside the PR scope  
- Flag issues that are handled elsewhere in the system  

By explicitly stating assumptions and non-goals, you:

- Prevent hallucinated architectural criticism  
- Reduce overreach beyond PR scope  
- Keep feedback aligned with the actual change  
- Improve precision in real-world reviews  

This complements the structured, context-first guideline:

- **Structured, context-first guideline** → Controls *how* the review is structured  
- **This guideline** → Controls *what boundaries* the model must respect  

---

### Good Example

```text
You are reviewing this pull request.

Assumptions:
- Authentication is handled upstream.
- Input validation occurs in the API gateway.
- This service does not manage database transactions directly.

Non-goals:
- Do not suggest architectural redesign.
- Do not propose new frameworks.
- Do not refactor unrelated modules.

Review only the changes in this diff for:
- correctness
- security within this service boundary
- performance regressions

### Bad Example

```text
Review this PR and suggest improvements.
OR
Review this PR for correctness and security