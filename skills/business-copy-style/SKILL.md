---
name: business-copy-style
description: "Use when the task is to write or polish short, consumer-facing marketing text itself — ad copy, offer wording, outreach emails, landing page or headline copy, lead magnets, README intros, billboard/product taglines — making it read at a 5th-grade level and sound human, not AI-generated. Trigger on requests to simplify, humanize, or de-AI existing copy, or to draft new short promotional text. Do NOT trigger for building marketing/lead-gen strategies, campaign plans, or technical/engineering documentation (API references, white papers, release notes) even if asked to sound \"less like AI\" — this skill is about the wording of consumer-facing copy, not strategic planning or technical writing."
---

# Business Copy Style

Use this skill whenever you write or revise customer-facing business copy — offers, outreach scripts, lead magnets, landing pages, README files, ads, or emails. The goal is plain, human prose a 5th grader can read and no one mistakes for AI.

## Core Rules

1. **Read the rules first.** Before writing or editing, scan the plain-language and de-AI references.
2. **Target ≤5th-grade reading level.** Short sentences. One idea per sentence. Active voice. Concrete nouns. No jargon without a one-line translation.
3. **Cut AI tells.** Remove inflated significance, formulaic triads, dead vocabulary ("delve", "landscape", "unlock", "robust", "seamless"), crutch transitions ("Moreover", "That said"), synonym cycling, boldface overuse, hedging, and uniform sentence rhythm. Count em dashes and cut them; short copy should have zero.
4. **Take a position.** If every reasonable person would agree with the line, it is not copy — it is noise. Say something specific, opinionated, or risky.
5. **Vary sentence length.** Mix short punchy lines with longer ones. Avoid metronomic medium-length sentences.
6. **No hedging without a reason.** Delete "it's worth noting", "arguably", "could potentially", "studies show", "many believe". Name the source or say the thing directly.
7. **One translation per jargon term.** If you must use a term your avatar would not say out loud, follow it immediately with plain English in parentheses. Then remove the jargon in the next pass.
8. **Compute Flesch-Kincaid before finishing.** If the grade is >6, shorten the worst sentences and swap abstractions for concrete nouns.
9. **Read it out loud.** Flag anything that sounds like a press release, a chatbot, or no human would say.

## Edge Case

If invoked standalone with no copy to review, write new copy under these rules rather than erroring or asking for copy to review. Ask the user what the copy is for, who it is to, and what action they want.

## Routing Table

| Need | Read |
|---|---|
| Lower reading level and enforce plain-language rules | references/plain-language.md |
| Strip AI-sounding prose and structural tells | references/de-ai-prose.md |
