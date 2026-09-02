---
name: voice-calibration
description: Derive or update a writing voice profile from user-approved examples, edits, historical writing or conversation history. Use when the user wants prose to sound consistently like them across genres. Separates stable writing DNA from presentation, email, social, technical and private-thinking variants.
---

# Voice Calibration

Infer preferences from accepted evidence, not stereotypes about how a person should sound.

This skill produces or updates a voice profile. It does not draft the final deliverable.

## 1. Build the sample set

Prefer:

1. user-approved final outputs;
2. user rewrites of AI drafts;
3. clearly user-authored writing;
4. conversation turns that show stable phrasing preferences;
5. outside exemplars the user explicitly likes.

Sample more than one genre when the profile is meant to be general.

Tag each sample by genre, date, provenance and whether the user explicitly approved it.

*Done when:* the corpus distinguishes `user-authored`, `user-edited`, `approved`, and merely `available`.

## 2. Extract stable DNA

Look for repeated behaviour across genres:

- how quickly the point appears;
- direct vs indirect syntax;
- specificity and use of examples;
- sentence-length distribution and rhythm;
- punctuation;
- certainty, hedging and qualification;
- first-person usage;
- humour and informality;
- tolerance for imperfection;
- preferred technical density;
- how conclusions end.

Do not infer a rule from one memorable phrase.

*Done when:* every stable preference is supported by several examples or an explicit user statement.

## 3. Separate genre variants

Conversation is not automatically presentation copy. Record surface-specific differences.

Typical branches:

- executive presentation;
- email/message;
- social/public writing;
- technical documentation;
- private thinking/research.

A stable rule can apply everywhere; a genre rule lives only in that branch.

*Done when:* the profile can explain why two different-looking samples can both sound like the same person.

## 4. Compare against rejected AI output

When available, pair a rejected draft with the user's rewrite. Identify the **earliest generative difference**, not just the words that disappeared.

Useful dimensions:

- abstraction became a concrete fact;
- caveat moved from headline to note;
- three points became one;
- polished contrast became a direct statement;
- context was left for the speaker rather than written;
- certainty was split from evidence.

These before/after pairs are stronger than generic anti-AI rules.

*Done when:* the calibration captures causes, not only banned phrases.

## 5. Use external exemplars carefully

For provenance, pre-2022 examples can be useful because they are less likely to be AI-generated. This is only a sampling heuristic. Age does not imply quality, and many patterns associated with AI originated in human writing.

Extract structural principles, never distinctive wording.

*Done when:* external material supports a principle rather than becoming a style imitation target.

## 6. Update the profile

Write the smallest durable change. Preserve existing accepted guidance unless the new evidence clearly supersedes it.

For George's wiki, propose changes to `notes/george-voice.md`; do not silently rewrite the canonical profile.

*Done when:* the profile is shorter than the evidence behind it and can guide `writing-core` without forcing one genre onto another.
