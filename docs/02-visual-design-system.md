# 02 — Visual design system

Status: **palette and ground decided (D-01, 2026-11-03)**; type family (D-01b) and voice-visualizer style (D-01c) are being picked from `docs/aesthetics/frames/helena-board.jpg`. Everything in § Shared is fixed.

The look is *uncanny clinical retrofuturism*: immaculate, symmetric, controlled, and slightly wrong because nothing is ever rushed. References: 2001 (white architecture, isolated red), THX 1138 (featureless white, dehumanising calm), Severance (institutional symmetry), Mirror's Edge (red on white), The Andromeda Strain (clinical equipment), Portal 2 (white test chambers). Kyle's longer description: `docs/aesthetics/helena_aesthetic.md`; character reference: `docs/aesthetics/helena-reference-sheet.png`.

Live tokens: `helena-media-library/assets/brand/helena/tokens.css` (class `hl-helena` + one `hl-type-*`). Test frames: `docs/aesthetics/helena.html` → `node render-helena.mjs`. The earlier five-direction exploration (`explore.html`, `frames/`) is kept as an archive.

## Palette (from the reference sheet)

| Role | Hex | Use |
|---|---|---|
| Ground | `#F0F0F2` off-white | the frame |
| Surface | `#FFFFFF` white | nodes, cards — white objects on off-white, like her uniform on the backdrop |
| Ink | `#0E0E10` near-black | all text, the structural marks |
| Muted | `#8A8A8E` | labels, indices, upcoming caption words |
| Line | `#C9C9CE` | hairlines, node borders, rules |
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

Family candidates (D-01b): **geometric** Jost (Kubrick/2001), **grotesk** Inter Tight + IBM Plex Mono labels (Severance/THX), **eurostile-like** Michroma headings + Inter captions (70s sci-fi). All OFL.

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
Top centre, under the meta line. Driven by `levels.json` (loudness bands from her narration, `levels.py`), never by music. Idle in silence, moving while she speaks. Three candidate styles (D-01c): **grid** (the 3×3 dot mark from the back of her uniform; centre dot red), **trace** (one red line), **disc** (red disc in hairline rings). It is the only red object in frames where nothing else is highlighted; when a diagram element is highlighted, the visualizer's red stays — it's her, not a highlight — and the rule becomes "one red *idea*".

### Sound
- Her voice is dry and close. Music is a low, sparse, tonal bed well under her (≥ 12 dB), no drums, no drops. SFX are few and quiet: a soft tick when an element arrives, a single tone on the red landing, nothing on cuts. −14 LUFS, ≤ −1 dBTP.

## Diagram primitives
Same primitive set as `05`; in the Helena direction they render as white rectangles with hairline borders, square corners, centred labels with a muted index at the left, one red chip or border on the highlighted stage. No glows, no rounded corners, no fills other than white.

## What was decided and what's left
- Decided: palette, ground/surface logic, one-red rule, centred composition, slow-flat motion, frame chrome, no stills of Helena, visualizer as carrier.
- D-01b type family and D-01c visualizer style: pick from the board; the library tokens carry all three families until then.
- Wordmark: not designed (D-08). The 3×3 dot mark is the working logo.
