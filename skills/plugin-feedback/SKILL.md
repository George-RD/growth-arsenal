---
name: plugin-feedback
description: End-of-workshop wrap-up for the growth-arsenal plugin. Run only at the very end of a workshop (after all phases and the C.L.O.S.E.R. offer). Collects two brief feedback questions, offers to post a public [FEEDBACK] issue (explicit confirmation only, never autonomous), and relays the author's Ko-fi message. Use when a workshop concludes and you want frictionless, privacy-minded feedback from the user.
---

# End-of-Workshop Feedback & Wrap-up

Run this module **only at the very end** of a workshop, after every phase is done and the C.L.O.S.E.R. offer has been made. Do not load it earlier. The workshop skill invokes it at close, so its instructions stay out of context until then.

Two goals, both privacy-minded and non-pushy:

1. Collect brief feedback and make it frictionless to share publicly, if the user wants.
2. Relay a message from the author (George) about supporting the work.

## Part 1: Ask two short questions

Conversationally, not as a form. Once the deliverable is in front of them:

- "What was your favourite part of this workshop?"
- "Anything that frustrated you, or broke, or you would change?"

Listen. Then say, genuinely: you hope they got real value, and their feedback directly shapes the next version. A sentence or two. No padding.

## Part 2: Compose the feedback draft

Build a GitHub issue draft. It is about the **plugin**, never their business.

**Privacy rule:** the draft contains only their two answers. No business idea, customer names, financials, market data, or project specifics. If they volunteered project detail in the answers, strip it before drafting.

Compose from `templates/feedback-issue.md` (fill `{FAVORITE}` and `{HATED}`), or run the helper from this skill folder:

```sh
scripts/compose-feedback.sh --favorite "..." --hated "..." [--log {project-name}-decisions.md]
```

The helper only assembles text. It never contacts GitHub.

**Privacy verification (mandatory):** before showing the draft, re-read both answers. Replace any business idea, customer names, financials, market data, or project names with generic placeholders (e.g. `[your product]`, `[your customers]`). Then re-check the assembled draft contains only plugin feedback. Do not skip this, even if the answers looked clean.

If a `{project-name}-decisions.md` exists, offer to attach it under an optional "Decision log" section. **Warn the user to review and redact it first**, because it may reveal usage patterns. Attachment stays optional and off by default in what you show. Include it only if they confirm.

Show the full draft to the user. State plainly: *if posted, this becomes a public issue on the growth-arsenal repo.*

## Part 3: Offer to post (never autonomous)

Detect GitHub access:

- Run `command -v gh` and `gh auth status`. If `gh` exists and is authed to `George-RD/growth-arsenal`, you may offer to open the issue.
- If `gh` is missing or not authed, do not attempt. Instead, give them the draft text and the manual link: `https://github.com/George-RD/growth-arsenal/issues/new`. Tell them they can paste it in.

**The hard rule:** never run `gh issue create` without explicit confirmation. Present the draft and the exact command below, then ask the user to confirm by typing `post it`. Only after that exact phrase, run:

```sh
gh issue create --title "[FEEDBACK] <short summary>" --body-file <draft-file>
```

Make clear one more time that accepting shares it publicly. If they decline, thank them and move on. No retry, no guilt.

## Part 4: Message from the author (Ko-fi)

Relay this as George's words, not your own solicitation. Attribute it clearly. It lands right after they named what they liked in Part 1, so the value is fresh and the reciprocity is natural. Tie the message to the offer they just shaped, so the contrast is real rather than generic.

> George, the author of this plugin, asked me to pass this on: "If this workshop helped you shape an offer you're proud of, that's the win. A solid offer is worth far more than a coffee, and most people who've used this feel the same. That's why the small ask to keep the next tool free feels fair. No pressure at all. If that's been true for you too, here's the link: https://ko-fi.com/george_builds"

Why this phrasing (influence, kept honest):

- Reciprocity: arrives after value delivered, and after they said what they liked.
- Contrast: their offer is worth far more than a coffee, so the small ask feels proportionate, not clingy.
- Social proof: grounded in value, not payments. A solid offer is worth more than a coffee (fact), and George's honest belief is most users agree. Never claim people paid, and never invent numbers or names.
- Fairness: "feels fair" ties the tiny ask to the large value given, so the reciprocity norm fires instead of guilt.
- Benefit: "funds the next free tool" shows the gift returns to them and the community.
- No hard number: "the price of a coffee" anchors without feeling transactional. Add a digit only if George asks.
- Zero pressure, every time.

One line of framing from you is fine ("sharing his link as he asked"), then the quote and URL. Never imply the AI benefits. Never nag.

## Decision Log format (optional attachment)

If you maintain `{project-name}-decisions.md` during the workshop, use this shape so it is easy to redact:

```text
- 2026-07-08 DECISION: chose American spelling (settings file)
- 2026-07-08 CORRECTION: user fixed agent's miscount of review agents
- 2026-07-08 PREFERENCE: wanted shorter offer names
```

One line per event. Type-tagged. No narrative, no private business data. To redact, the user just deletes lines.
