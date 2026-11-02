# 05 — Visual storytelling

The visual **is** the explanation. If a scene would still make sense with the diagram removed, the diagram is decoration — redesign it. Conversely, if the narration describes what's visibly happening, cut the narration.

## The primitive set

Every mechanism in a script maps to exactly one of these per beat. They live in the media library under `assets/diagrams/` (ids in code), built once per direction's tokens.

| Primitive | Library id | Use when the idea is… | What animates | Highlight |
|---|---|---|---|---|
| **Pipeline** (vertical) | `pipeline` | a sequence of stages (input → … → output) | nodes draw on in order; a token/packet travels down the edges | one stage |
| **Before / after** | `before-after` | a change in state, a comparison of old vs new approach | split or swap; the differing element morphs | the difference |
| **Zoom-in** | `zoom` | "inside this box there's…" | camera dollies into one node; the node expands into its own sub-diagram | the inner part |
| **Layered stack** | `stack` | abstraction layers (hardware → OS → runtime → app) | layers slide in from the bottom; one layer lifts out | one layer |
| **Tree / graph** | `graph` | dependencies, forks, branching choices | nodes grow from the root; an edge lights up | one path |
| **Timeline** | `timeline` | "it used to…, then…, now…" | a line draws left→right; markers pop at events | one event |
| **Comparison grid** | `grid` | 2–4 things × 2–4 properties | cells fill in row by row; one cell gets the accent | one cell |
| **Big number / counter** | `counter` | scale ("40,000 stars", "256 tiles", "3 lines of config") | count-up tied to the narration word; optional sparkline | the number |
| **Tile / partition** | `tiles` | chopping, batching, sharding, patches | a whole splits into parts; parts get labels | some parts |
| **Loop / cycle** | `cycle` | agents, feedback loops, training loops | a ring draws; a marker orbits; one step enlarges | one step |
| **Title card** | `title-card` | hook, scene titles, the CTA | text sets in; one word takes the accent | one word |

Rule of thumb: if a beat needs two primitives, it's two beats. If a primitive needs > 6 visible elements, zoom in.

## From script to storyboard

For each beat in `script.md`:

1. **Name the primitive** and the single highlighted element.
2. **List the reveal order** — the order the viewer should read it, which is also the order the narration mentions it.
3. **Bind each reveal to a narration word** (`narration.at("tiles")`). The element appears as the word is spoken, draw-on 600–900 ms.
4. **Decide what persists** into the next beat. Prefer carrying one object across the cut (the same node, now zoomed; the same number, now in a grid) over a clean slate.
5. **Caption line(s)** for the beat: the exact words, with the accent word marked.
6. **Transition in**: dip, stagger, wipe-up, or re-frame — never a crossfade between two busy frames.

That table is the shot list (`templates/shot-list.md`).

## Reveal rules

- One new element per spoken clause. Nothing else moves while it enters.
- Primary element first and most prominent; secondaries stagger 40–80 ms behind.
- Colour arrives last: the diagram builds in ink; the accent lands on the highlighted element when the narration reaches the point.
- Dim to focus: when the narration zooms in on one part, the rest drops to `--muted`.
- Objects are real things: move them, morph them, re-frame on them. Don't fade one out and another in at the same place.
- Default to stillness. A frame that's done building holds still until the next clause.

## Analogies on screen

The analogy gets its own small visual next to the mechanism, not instead of it: tiles ↔ puzzle pieces; cache ↔ a sticky note on the monitor; tokens ↔ Lego bricks. Draw the analogy in the same primitive style (ink lines), never as a clip-art illustration. When the analogy breaks, visibly break it (a strike-through, a "≠").

## Frame 0 / cover

Hook text (≤ 2 lines, upper-middle band) + one diagram element already present (a node, a number, a sparkline). Three objects max. It must work as a 200-px-wide thumbnail.

## Last frame

Mirrors frame 0: same ground, the diagram returned to its resolved state, the hook's key word on screen next to the CTA. Motion and music continue through the final frame.

## Anti-patterns

- Stock footage, screen recordings of other people's UIs, logos as decoration, emoji.
- Text walls (> 8 words per line, > 2 lines).
- Whole-frame pulsing, camera shake, particles, lens flares.
- Diagrams that are only pretty: boxes with arrows that don't correspond to a real data flow.
- A diagram that changes while a caption is being read.
