# growth-arsenal design system

## Design thesis

The product is presented as a destructive qualification lab for business ideas. A weak offer enters a test rig, independent critics apply pressure and the approved decisions leave as usable files. This replaces the previous cream-paper, editorial-serif and red-pen identity, and avoids the literal military interpretation of “arsenal”.

The page should feel decisive and engineered, not aggressive or theatrical.

## Palette

- Test-bay cobalt: `#1450ff`. Owns the hero and install regions.
- Deep cobalt: `#1744d1`. Active depth and pressed states.
- Instrument navy: `#0e1630`. Primary ink, consoles and structural borders.
- Paper: `#f6f8ff`. Main reading surface.
- High-visibility yellow: `#d9ff4f`. Primary action, pass states and calibration markers.
- Revision orange: `#ff5c35`. Copy gate and explicit failure/revision moments.

Secondary text is tinted from navy or the field colour. Do not use neutral grey on coloured surfaces.

## Typography

- Display: Barlow Condensed, 700 to 900. Uppercase, tightly composed, maximum 5.8rem.
- Body: Atkinson Hyperlegible, 400 and 700. Long-form measure stays under 65 characters where possible.
- Data and code: Spline Sans Mono, 500 and 600. Use only for commands, files, states and measurements.

Headings carry their own weight. Do not add small eyebrow labels above ordinary section headings.

## Composition

- Maximum content width: 1180px with responsive page gutters.
- First viewport: claim and action on the left; working offer qualification rig on the right.
- Page rhythm alternates cobalt, paper, navy, high-visibility yellow and orange fields.
- Workshop descriptions are full-width benches, not equal cards.
- Structural borders are square and decisive. The test rig uses clipped corners to read as equipment.
- Measurement grids are permitted only inside instrument surfaces where they have a reason to exist.

## Components

### Buttons

Primary buttons use high-visibility yellow, navy border and an offset navy shadow. Hover moves the button up and left by 2px. Text links remain underlined.

### Test rig

The rig has four accessible tabs: Input, Attack, Rebuild and Clear. It is the only authored motion moment. It may auto-advance unless reduced motion is requested, and pauses on pointer or keyboard interaction.

### Workshop benches

Each bench spans the viewport and carries one stage of the product chain. Offer uses paper, Leads uses yellow, Copy uses orange. Outputs are shown as manifests or before/after material, not generic feature cards.

### Code consoles

Code, file trees and installation commands use navy fields with real text. Consoles have one structural border or one offset shadow, never a soft “ghost card” treatment.

## Interaction and accessibility

- Keyboard focus uses a 3px white outline with a 2px offset and a navy outer keyline, so it remains visible on every field.
- Interactive tab groups support arrow keys and correct ARIA state.
- Body text meets 4.5:1 contrast and display text meets 3:1.
- Content remains usable without JavaScript.
- Reduced-motion users get near-instant transitions and no auto-cycle.
- Mobile reading order is claim, action, demonstration, explanation, install.

## Anti-patterns

Do not return to cream paper, high-contrast editorial serif, red-pen stamps, section-number decoration, centred SaaS heroes, glass panels, gradient text, icon-card grids or monospace used as a general “technical” costume.
