# 02 — Visual design system

Status: **direction not yet chosen** (see `10-decision-log.md` § Aesthetic). Everything in § Shared is fixed regardless of direction; § Directions describes the five candidates and the test that picks one.

Evidence: `docs/research/aesthetic-directions.md`. Live tokens: `tech-splained-media-library/assets/brand/techsplained/tokens.css`. Rendered test frames: `docs/aesthetics/frames/`; regenerate with `node docs/aesthetics/render.mjs`.

## Shared (fixed)

### Canvas
- 1080×1920, 30 fps. Design at 1×; nothing scales.
- **Must-read zone:** x 60–960 (keep the right ~120 px for the action column), y 220–1440. Captions sit centred in a ≤ 900 px column at y ≈ 1200–1380. Nothing the viewer must read goes in the bottom 480 px or the top 220 px. Decorative lines may bleed to the edges.
- Frame 0 = cover: hook text + one diagram element, ≤ 3 objects. Centre the title so the 4:5 (feed) and 1:1 (grid) crops still show it.

### Colour discipline
- Three roles only: **ground** (background), **ink** (text + structure), **accent** (the one thing to look at). A fourth, `--accent2`, exists for a second semantic meaning (a "before" state, a warning) and most videos never use it.
- One colour = one meaning for the whole video. The accent marks the highlighted element and the highlighted caption word — nothing else.
- Highlight by subtraction: dim the rest to `--muted` rather than only brightening the subject.
- Contrast: captions ≥ 7:1 on the ground (all five directions clear 16:1); diagram strokes ≥ 3:1. Check the brightest and darkest frames.

### Type scale (px at 1080 wide)
| Role | Size | Weight | Font |
|---|---|---|---|
| Hook H1 | 120–140 | direction's `--h1-weight` | `--display` |
| Scene title | 64–72 | 600–800 | `--display` |
| Caption | 60–66 | 700 (600 for lighter faces) | `--caption` |
| Node label | 36–40 | 600 | `--display` |
| Mono annotation / index | 24–28, +0.08–0.14 em tracking | 400–500 | `--mono` |
Floor: nothing under 32 px. Mono captions cap at ~22 characters/line.

### Captions
- Word-synced from `narration.json`; the current word takes the accent; spoken-but-passed words stay ink; upcoming words aren't shown (or shown at `--muted` in the 3–5-word style — pick per direction, record in the decision log).
- Sit directly on the ground; add an 80 %-opaque pill only when a caption overlaps a diagram.
- A caption is on screen ≥ 0.3 s per word from the moment it's complete. Captions must be in sync in the first 3 s above all.

### Motion language
- Purpose test: if you can't name what a move communicates (state change, attention, continuity, relationship), it doesn't move. Default to stillness between beats.
- Ease-out in (`cubic-bezier(.16,1,.3,1)`), ease-in out, ease-in-out for in-frame moves. Never linear.
- Durations: UI moves 200–400 ms; diagram draw-ons 600–900 ms; sibling stagger 40–80 ms.
- Reveal order = reading order, primary element first. Every object persists: move or morph it, never blink it out and in.
- Transitions: dip through the ground, or a stagger (old out, then new in); a slow re-frame (dolly/zoom) when objects persist. No crossfades between two busy layouts.
- Reveals are triggered by narration words, not timers (see 05 and the composition contract in 06).
- No whole-frame pulsing on beats. Music sync is for specific events: a reveal landing, a transition, the CTA card.

### Sound
- Music bed under the voice at ≥ 10 dB ducking; SFX on reveals and transitions only; −14 LUFS integrated, ≤ −1 dBTP.

## Directions (candidates)

Each is implemented as a body class in `tokens.css` and rendered in `docs/aesthetics/frames/`.

| Id | Ground / ink / accent | Fonts | Signature | Trade-offs |
|---|---|---|---|---|
| **A blueprint** | paper `#F3F1EA` / ink navy `#14213D` / international orange `#FF4F1F` (secondary blue `#1D4ED8`) | Space Grotesk + JetBrains Mono | hairline grid, ink draw-on, dimension lines, "FIG. 03" annotations | Light frames stand out in a dark feed; low HTML cost; least "sci-fi"; Vercel/Stripe adjacency |
| **B instrument** | near-black `#06080C` / `#E6EDF3` / teal `#2DD4BF` (amber `#F5B942` for warnings) | Geist + Geist Mono | corner brackets, readouts, count-ups, scan-wipes, faint scanlines | Most literally "sci-fi lab"; many dark HUD clips exist (clone risk); glows cost a little |
| **C midnight** | navy `#0E1320` / `#ECEFF6` / yellow `#FFC857` (blue `#58C4DD` = structure) | Inter + IBM Plex Mono | soft glow, rounded primitives, morphs, 3B1B colour semantics | Closest to the 3B1B reference; path morphing is the costliest motion; "another Manim channel" risk |
| **D clinical** | white / `#0A0A0A` / blue `#0A84FF` | Inter Tight + Inter | big tight type, grey structure, colour arrives last | Cleanest; high feed differentiation; least lab-like; blue on white is borderline, so body captions stay black |
| **E signal** | black / `#F2F2F2` / green `#00E07A` | JetBrains Mono everywhere | type-on, dashed connectors, `>` prompts, inverted highlight | Cheapest to build; strong identity; mono captions are wide (short lines); hacker-aesthetic risk |

Hybrid worth testing (from the research): A's paper grid and draw-on as the frame + C's colour semantics + E's mono labels.

### Diagram primitives per direction
All directions implement the same primitive set (05) — only stroke, radius, glow and connector style differ. Primitives read `--stroke`, `--radius`, `--line`, `--accent` and never hard-code colour.

## The test that picks a direction

1. Render the same 15 s mechanism scene (narration + captions + a pipeline primitive + one transition) in the top 3 directions after Kyle's first cut from the contact sheet.
2. Judge on: readability on a phone at arm's length; how distinct it is in a feed of dark videos (screenshot the three frames into a mock feed); how much the agent had to fight the style to express the diagram; render cost.
3. Post 2 videos per finalist over 3 weeks (same hook archetype), compare 3-s retention and completion (09). Keep the losers' tokens for occasional "special" videos.

Record the result in `10-decision-log.md`; after that, `/ts-produce` uses only the chosen class.
