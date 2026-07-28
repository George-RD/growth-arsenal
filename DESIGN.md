---
name: growth-arsenal
description: A qualification lab for offers, growth plans and customer-facing copy.
colors:
  test-bay-cobalt: "#1450ff"
  deep-cobalt: "#1744d1"
  instrument-navy: "#0e1630"
  instrument-navy-raised: "#172242"
  report-paper: "#f6f8ff"
  high-visibility-yellow: "#d9ff4f"
  revision-orange: "#ff5c35"
  evidence-blue-soft: "#dfe7ff"
typography:
  display:
    fontFamily: "Barlow Condensed, Avenir Next Condensed, Arial Narrow, sans-serif"
    fontSize: "clamp(3rem, 6vw, 5.8rem)"
    fontWeight: 900
    lineHeight: 0.9
    letterSpacing: "-0.025em"
  body:
    fontFamily: "Atkinson Hyperlegible, Avenir Next, Arial, sans-serif"
    fontSize: "clamp(1rem, 0.96rem + 0.18vw, 1.12rem)"
    fontWeight: 400
    lineHeight: 1.55
  data:
    fontFamily: "Spline Sans Mono, SFMono-Regular, Consolas, monospace"
    fontSize: "0.75rem"
    fontWeight: 600
    lineHeight: 1.45
    letterSpacing: "0.07em"
rounded:
  square: "0"
  control: "2px"
spacing:
  tight: "8px"
  control: "16px"
  section: "clamp(5rem, 10vw, 9rem)"
components:
  button-primary:
    backgroundColor: "{colors.high-visibility-yellow}"
    textColor: "{colors.instrument-navy}"
    typography: "{typography.body}"
    rounded: "{rounded.square}"
    padding: "14px 20px"
  status-pass:
    backgroundColor: "{colors.high-visibility-yellow}"
    textColor: "{colors.instrument-navy}"
    typography: "{typography.data}"
    rounded: "{rounded.square}"
    padding: "3px 8px"
  status-revision:
    backgroundColor: "{colors.revision-orange}"
    textColor: "{colors.instrument-navy}"
    typography: "{typography.data}"
    rounded: "{rounded.square}"
    padding: "3px 8px"
---

# Design System: growth-arsenal

## Overview

**Creative North Star: "The Qualification Lab"**

growth-arsenal presents business work as material entering a test bay. Ideas are labelled, attacked, revised and cleared for real-world testing. The system should feel engineered and decisive without becoming military theatre. It is allowed to be bold because the product itself challenges weak assumptions, but every expressive choice must improve comprehension of state, evidence or action.

The public landing page uses the system in **Persuade** mode. Generated workshop reports use it in **Operate** or **Read** mode: the same cobalt, navy, yellow, orange, typography and structural language, with less spectacle and more evidence density.

**Key characteristics:**

- saturated cobalt fields rather than neutral SaaS shells;
- square structural borders and offset shadows;
- condensed display type for claims and state, hyperlegible body type for decisions;
- yellow means approved/action, orange means revision or explicit risk;
- consoles, manifests and evidence rows show real work instead of decorative chrome.

## Colors

The palette uses industrial signal colour at page scale, not scattered accent confetti.

### Primary

- **Test-bay cobalt** (`#1450ff`): public hero fields, install regions and major report headers.
- **Deep cobalt** (`#1744d1`): pressed and active depth where cobalt needs a second plane.

### Secondary

- **High-visibility yellow** (`#d9ff4f`): primary action, approved state and calibration markers.
- **Revision orange** (`#ff5c35`): failed copy, stale state, revision work and accepted-risk emphasis.

### Neutral

- **Instrument navy** (`#0e1630`): primary ink, consoles and structural keylines.
- **Raised instrument navy** (`#172242`): active dark control surfaces.
- **Report paper** (`#f6f8ff`): reading surface.
- **Evidence blue-soft** (`#dfe7ff`): draft and in-review state.

### Named Rules

**The State Has a Colour Rule.** Yellow is not decoration. It means approved or actionable. Orange means revision, failure or acknowledged risk.

**The Coloured Field Rule.** Saturated colour owns coherent regions. Do not sprinkle cobalt, yellow and orange across unrelated components.

## Typography

**Display Font:** Barlow Condensed, with Avenir Next Condensed and Arial Narrow fallbacks.  
**Body Font:** Atkinson Hyperlegible, with Avenir Next and Arial fallbacks.  
**Label/Mono Font:** Spline Sans Mono, with SFMono-Regular and Consolas fallbacks.

**Character:** Display type is compressed, blunt and declarative. Body type is calm and easy to scan. Mono is reserved for code, files, measurements, phase state and provenance.

### Hierarchy

- **Display** (900, up to `5.8rem`, line-height `0.9`): first-view claims and final offer names.
- **Headline** (900, `clamp(3rem, 6vw, 5.2rem)`, line-height `0.9`): report and section headings.
- **Title** (800, `2rem`, line-height `1`): phase, stack and persona titles.
- **Body** (400, responsive `1rem–1.12rem`, line-height `1.55`): explanations and evidence, generally under 70 characters per line.
- **Label** (600, `0.72–0.75rem`, tracked uppercase): state, files, scores, timestamps and categories.

### Named Rules

**The Mono Earns Its Place Rule.** Use mono only when the content is code, data, measurement, state or provenance.

## Layout

The primary frame is `min(1180px, 100vw - 3rem)`. Public pages may use asymmetric two-column first viewports. Reports use clear rails, full-width rows and evidence tables. Dense information sits inside bounded instruments; the surrounding page remains spacious.

Responsive layout preserves the information order: decision or claim, current state, evidence, next action. Below 860px, primary grids collapse to one column. Below 560px, controls remain full-width and tables may scroll horizontally rather than compressing into illegibility.

Section spacing uses `clamp(5rem, 10vw, 9rem)` on screen and reduces for print. Generated reports must print without navigation or interactive controls.

## Elevation & Depth

Depth is structural. Major instruments use a hard offset shadow, normally `10px 10px 0 #0e1630`. Small components stay flat and use borders or tonal separation. Do not combine a fine border with a soft ambient shadow.

### Shadow Vocabulary

- **Instrument lift** (`10px 10px 0 #0e1630`): qualification panels and install/report consoles.
- **Cobalt report lift** (`10px 10px 0 #1450ff`): dark file and evidence consoles on light report surfaces.

### Named Rules

**The One Elevation Signal Rule.** A component gets a border or a deliberate offset shadow. It does not get layered ghost-card elevation.

## Shapes

The system is square by default. Buttons and status chips may use at most a `2px` control radius. Signature test rigs may clip two opposing corners to suggest equipment. Borders are usually 1–2px. Rounded cards, pills and glass panels are outside the system unless a native platform requires them.

## Components

### Buttons

- **Shape:** square, 2px structural border.
- **Primary:** yellow field, navy text and keyline, `14px 20px` padding.
- **Hover / Focus:** move up-left by 2px and increase the offset shadow; focus uses a 3px white outline with a navy outer keyline.
- **Secondary:** transparent field with an underlined or bordered text action.

### Status

- **Approved:** yellow field with navy label.
- **Draft / In review:** blue-soft field with navy label.
- **Stale / Revision:** orange field with navy label.
- **Not started:** transparent with tinted navy text.

### Cards / Containers

Use containers only when the content needs a boundary. Reports prefer full-width rows, tables, manifests and instrument panels over same-size cards. Persona records may use bordered containers because each is a distinct record with a repeated schema.

### Navigation

Public navigation sits on cobalt. Report navigation uses the same cobalt header but remains compact and operational. Active report links use yellow text and a visible border. Mobile report navigation scrolls horizontally instead of disappearing.

### Qualification Rig

The rig is the signature component. It exposes an input, independent attacks, revisions and clearance. It may animate once as authored material, but the state must remain usable with JavaScript disabled and when reduced motion is requested.

### Phase Rail

Each phase row shows label, status, revision, review count, open critical issues and score. Stale work remains visible with its reason; it is never presented as approved.

## Do's and Don'ts

- **Do** show the product mechanism with real state, findings, files and decisions.
- **Do** use yellow and orange consistently as semantic state.
- **Do** keep generated reports self-contained, printable and usable without network access.
- **Do** let report density vary by surface: offer summary can persuade, progress must operate, research must read.
- **Don't** return to cream paper, editorial serif, red-pen stamps or literal weapon imagery.
- **Don't** use centred SaaS heroes, glass panels, gradient text or equal icon-card grids.
- **Don't** invent scores, customer proof, prices or evidence to make a report look complete.
- **Don't** manually edit generated HTML. Change workspace state or the shared renderer and regenerate.
