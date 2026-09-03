---
name: voice-calibration
description: Derive or update a writing voice profile from user-approved examples, edits, historical writing or conversation history. Use when the user explicitly wants prose to sound consistently like them across genres. Separates stable writing DNA from presentation, email, social, technical and private-thinking variants.
---

# Voice Calibration

Infer preferences from **approved evidence**, not stereotypes about how a person should sound.

This skill calibrates a voice profile. It does not silently mine available history.

## 1. Define approval scope

Before collecting samples, establish what the user has authorised for this calibration run.

Approval can name:

- specific supplied examples;
- a folder or corpus the user explicitly selected;
- a date range or conversation-history scope the user explicitly asked to analyse.

Merely available content is not approved content. Exclude unapproved samples, including sensitive material, even when they would appear stylistically useful.

Raw calibration samples are working evidence only. Do not copy them into the resulting profile. Do not persist a sample corpus unless the user explicitly asks for it; otherwise keep only the derived rules and compact provenance notes needed to explain them.

*Done when:* the allowed corpus and persistence boundary are explicit.

## 2. Build the sample set

Within the approved scope, prefer:

1. user-approved final outputs;
2. user rewrites of AI drafts;
3. clearly user-authored writing;
4. approved conversation turns that show stable phrasing preferences;
5. outside exemplars the user explicitly likes.

Sample more than one genre when the profile is meant to be general.

Tag each sample by genre, date, provenance and approval status. Do not treat a sample as profile evidence when its provenance or approval is unclear.

*Done when:* every sample used for inference is inside the approval scope and has known provenance.

## 3. Extract stable DNA

Record structured calibration findings before writing profile prose. Look for repeated behaviour across genres:

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

*Done when:* every stable preference is supported by several approved examples or an explicit user statement.

## 4. Separate genre variants

Conversation is not automatically presentation copy. Record surface-specific differences.

Typical branches:

- executive presentation;
- email/message;
- social/public writing;
- technical documentation;
- private thinking/research.

A stable rule can apply everywhere; a genre rule lives only in that branch.

*Done when:* the profile can explain why two different-looking samples can both sound like the same person.

## 5. Compare against rejected AI output

When the approved corpus contains both versions, pair a rejected draft with the user's rewrite. Identify the **earliest generative difference**, not just the words that disappeared.

Useful dimensions:

- abstraction became a concrete fact;
- caveat moved from headline to note;
- three points became one;
- polished contrast became a direct statement;
- context was left for the speaker rather than written;
- certainty was split from evidence.

These before/after pairs are stronger than generic anti-AI rules.

*Done when:* the calibration captures causes, not only banned phrases.

## 6. Use external exemplars carefully

For provenance, pre-2022 examples can be useful because they are less likely to be AI-generated. This is only a sampling heuristic. Age does not imply quality, and many patterns associated with AI originated in human writing.

Extract structural principles, never distinctive wording.

*Done when:* external material supports a principle rather than becoming a style imitation target.

## 7. Draft the profile through writing-core

The structured calibration findings are derived evidence; the durable voice profile is prose generated from them. Before drafting that profile, resolve `writing-core` by skill name and pass the findings to it as the factual kernel input.

If `writing-core` is unavailable:

- return the structured calibration findings without turning them into durable profile prose;
- show `npx skills add George-RD/growth-arsenal --skill writing-core`;
- pause the profile-writing step rather than recreating the missing skill locally.

When `writing-core` is available, write the smallest durable change. Preserve existing accepted guidance unless the new evidence clearly supersedes it.

If the workspace already defines a canonical voice-profile format, preserve that format and update the smallest relevant sections. If no canonical format exists, copy and fill [`templates/voice-profile.md`](templates/voice-profile.md). Do not silently invent a different durable structure from run to run.

The profile may store:

- derived writing rules;
- genre branches;
- compact citations or provenance descriptions of the approved evidence;
- dated feedback that explains a rule change.

Do not store sensitive sample text merely to justify the rule. If a later audit needs the original evidence, return to the approved source rather than duplicating it into the profile.

If the workspace already defines a canonical voice-profile path, propose changes there. If it does not, return the filled profile template in the current response and ask where the user wants it stored before creating a durable file. Do not assume an author-specific path.

*Done when:* the profile has a stable structure, is shorter than the evidence behind it, contains no unnecessary raw samples, and can guide future `writing-core` runs without forcing one genre onto another.
