# 02 — Visual design system

Status: **decided (D-01, D-01b, D-01c — 2026-11-03).** Type family: eurostile-like (Michroma headings and labels, Inter captions and body). Voice visualizer: the 3×3 grid. Ground: true white. Final frames: `docs/aesthetics/frames/helena-final.jpg`.

The look is *uncanny clinical retrofuturism*: immaculate, symmetric, controlled, and slightly wrong because nothing is ever rushed. References: 2001 (white architecture, isolated red), THX 1138 (featureless white, dehumanising calm), Severance (institutional symmetry), Mirror's Edge (red on white), The Andromeda Strain (clinical equipment), Portal 2 (white test chambers). Kyle's longer description: `docs/aesthetics/helena_aesthetic.md`; character reference: `docs/aesthetics/helena-reference-sheet.png`.

Live tokens: `helena-media-library/assets/brand/helena/tokens.css` (class `hl-helena`; it carries the eurostile type by default — `hl-type-geometric|grotesk` remain for reference only). Test page: `docs/aesthetics/helena.html` → `node render-helena.mjs`. The earlier five-direction exploration (`explore.html`, `frames/`) and the type board (`helena-board.jpg`) are kept as an archive.

## Palette (from the reference sheet)

| Role | Hex | Use |
|---|---|---|
| Ground | `#FFFFFF` true white | the frame |
| Surface | `#FFFFFF` white, lifted by a soft shadow (`--hl-shadow`: `0 1px 2px rgba(14,14,16,.06), 0 10px 28px rgba(14,14,16,.09)`) and a faint `#E9E9EC` card edge | nodes, cards — white on white; depth, not contrast, separates them |
| Ink | `#0E0E10` near-black | all text, the structural marks |
| Muted | `#8A8A8E` | labels, indices, upcoming caption words |
| Line | `#C9C9CE` | hairline rules, diagram edges (card borders use the fainter `--card-line`) |
| **Accent** | `#D0111B` red | **one isolated object per frame**: the highlighted element, the spoken word, the centre of the visualizer |

The red is never a fill behind text, never a gradient, never more than one object at a time. Think of the red cup on the reference sheet.

## Shared (fixed)

### Canvas and safe area
- 1080×1920, 30 fps, 1×.
- Must-read zone: x 60–960, y 220–1440. Captions centred in a ≤ 840 px column at y ≈ 1300. Nothing to read in the bottom 480 px or the top 220 px.
- **Everything is centred.** Symmetry is the default; a deliberate off-centre element is a storytelling choice, not a layout choice.
- Frame chrome on every video: `HELENA · <index>` meta line at y 150 in tracked uppercase, a 300-px hairline rule under it, the voice visualizer at y ≈ 300, a hairline rule at y 1500, a beat index at y 1560 (`01 — hook`, `03 — mechanism`, `07 — request`).

### Type scale (px)
| Role | Size | Notes |
|---|---|---|
| Hook H1 | `--hl-h1` (104–112; 78 for Michroma) | centred, ≤ 3 lines |
| Scene title | `--hl-title` (44–64) | centred |
| Caption | 58 | weight per family |
| Node label | 36 | centred in the node |
| Label / index | 20–24, tracked .22–.32 em, uppercase | `--label` |

Family (D-01b, decided): **eurostile-like** — Michroma for the hook H1, scene titles, meta line, indices and node indices; Inter 600 for captions and node labels (Michroma is too wide to read at caption length). Both OFL. H1 78 px, line-height 1.3; title 44 px; labels 20 px tracked .22 em.

### Captions
- Word-synced from `narration.json`; the spoken word turns red; passed words stay ink; upcoming words muted. One accent word per line at most.
- Full stops stay in captions. Helena's sentences end.
- ≥ 0.3 s per word on screen; in sync in the first 3 s above all.

### Motion language — this is where the dread lives
- **Slow.** UI moves 500 ms; diagram draw-ons 1.2 s; stagger 120 ms. Roughly twice the durations of a normal explainer.
- **Flat.** Ease `cubic-bezier(.25,.1,.25,1)` in, `cubic-bezier(.42,0,1,1)` out. No overshoot, no bounce, no spring, ever.
- **Arrive, don't pop.** Elements fade and settle; nothing scales up from zero, nothing flies in.
- **Hold.** A finished frame holds still until the next spoken clause. Stillness is content.
- **Cut or dip.** Scene changes are a fade through the ground or a hard cut on a sentence boundary; never a wipe, whip or zoom-through.
- **Colour arrives last.** The diagram builds in ink; the red lands exactly on the spoken word.
- **No beat sync.** Music never drives motion; nothing pulses. The only thing that moves with sound is the visualizer, and only with her voice.
- **Precision as texture.** Hairlines align to a grid; indices increment; text is tracked evenly. Let the viewer sense that it was built by something that doesn't make mistakes.

### The voice visualizer (her carrier)
Top centre, under the meta line. Driven by `levels.json` (loudness bands from her narration, `levels.py`), never by music. Idle in silence, moving while she speaks. **Style (D-01c, decided): the grid** — the 3×3 dot mark from the back of her uniform, ink dots breathing with the low/mid/high bands, the centre dot red. (`trace` and `disc` remain in the asset for reference.) It is the only red object in frames where nothing else is highlighted; when a diagram element is highlighted, the visualizer's red stays — it's her, not a highlight — and the rule is "one red *idea*".

### Sound
- Her voice is dry and close. Music is a low, sparse, tonal bed well under her (≥ 12 dB), no drums, no drops. SFX are few and quiet: a soft tick when an element arrives, a single tone on the red landing, nothing on cuts. −14 LUFS, ≤ −1 dBTP.

## Diagram primitives
Same primitive set as `05`; in the Helena direction they render as white rectangles lifted by the soft shadow, a faint card edge, square corners, centred labels with a muted index at the left, one red chip (and ink border) on the highlighted stage. No glows, no rounded corners, no fills other than white. Shadows are the only depth cue and they never move.

## What was decided and what's left
- Decided: true-white ground, white-on-white cards with shadow, one-red rule, centred composition, slow-flat motion, frame chrome, eurostile-like type, grid visualizer, no stills of Helena.
- Wordmark: not designed (D-08). The 3×3 dot mark is the working logo; a Michroma wordmark is the obvious next step.
