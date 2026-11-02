# tech_splained — Candidate Aesthetic Directions

Research date: 2026-11-01
Brief: hyper-clean, sci-fi science lab, minimalist, colour used sparingly for focus, explanatory diagrams in the spirit of 3Blue1Brown. Output is 1080×1920 vertical, HTML/CSS-rendered, animated diagrams, burned-in captions.

All hex contrast ratios below were computed with the WCAG 2.x relative-luminance formula. Fonts listed are all available under the SIL Open Font License (OFL) via Google Fonts or the vendor's GitHub unless marked otherwise.

---

## 0. Shared constraints (apply to every direction)

These come out of the caption and motion research in sections 6–8 and should be fixed before picking a look.

- **Frame safe area for captions:** keep primary captions inside a centred band roughly 900 px wide, between ~520 px from the top and ~450–480 px from the bottom (Instagram's bottom chrome grew in late 2025). Avoid the right ~120 px (action column) and top ~220 px (status/search).
- **Caption type size:** 60–75 px at 1080 wide (≈3.1–3.9% of frame height); never below 55 px for primary captions, hard ceiling ~100 px. Weight 600–700 is the sweet spot; 1–3 words (word-by-word) or one 3–8 word line.
- **Caption treatment:** a 70–85% opaque box/pill is the most reliable (white on #262626 ≈ 15:1). A 3–4 px dark stroke is the common Reels alternative and works on neutral backgrounds; drop shadow alone is never enough. Because every direction here has a controlled, flat background, a pill is optional — the background itself can carry contrast, but the pill becomes useful whenever a caption overlaps a diagram.
- **Contrast floors:** body/caption text ≥ 4.5:1 (AA), aim ≥ 7:1 (AAA) because phones are viewed outdoors; diagram strokes and non-text graphics ≥ 3:1.
- **Motion defaults:** ease-out on entry, ease-in on exit, ease-in-out for in-frame moves; micro moves 150–250 ms, primary reveals 300–500 ms, diagram draw-ons 600–900 ms; stagger siblings 40–80 ms; never linear; default to stillness between beats.
- **One idea per frame.** Reveal in reading order, animate the primary element first, keep every object persistent (move it, don't blink it) so the viewer can track it between frames.

---

## 1. Direction A — "Lab Notebook / Blueprint"

### Description
A paper-light, off-white canvas with a barely-visible hairline grid, as if diagrams were drafted on engineering paper. Everything is ink-black line work with one cool ink accent; monospace annotations, dimension ticks and small-caps labels give it a technical-drawing register. It is the warmest of the five options and photographs well against a busy Reels feed because it is almost the only light frame in a sea of dark video.

### References
- Vercel "Blueprint Grid" aesthetic and the Geist design system — https://vercel.com/geist and the Setproduct guide https://www.setproduct.com/blog/complete-guide-to-blueprint-grid-design
- Stripe marketing/docs: cream/white ground, charcoal text, accent used only as punctuation — https://stripe.com/docs (token notes via https://opendesigner.io/blog/recreating-stripe-linear-vercel-design-systems-with-design-md)
- Tailwind CSS and Supabase marketing pages (same hairline-grid family, cited by Setproduct)
- NASA Graphics Standards Manual (1975, Danne & Blackburn): Helvetica, standardised grid, "unity, precision, thrust" — https://wearethemutants.com/2020/01/09/unity-precision-thrust-the-nasa-graphics-standards-manual-1975/
- Swiss International Typographic Style: mathematical grid, sans-serif, asymmetric layout, objectivity (Müller-Brockmann, Ruder, Hofmann) — https://www.printmag.com/?p=1387
- Braun / Dieter Rams: reduction, "less but better", neutral forms, function-led layout — https://designexplained.substack.com/p/dieter-rams-and-ten-principles-for
- Framer "Blueprint Grid" component (shows the look in motion) — https://www.framer.com/marketplace/components/blueprint-grid/

### Tokens
| Token | Value | Note |
|---|---|---|
| background | `#F7F6F2` | warm paper off-white |
| surface | `#FFFFFF` | cards / callouts |
| grid | `#DCDAD3` at 1 px, 24 px spacing (or 16 px dots) | 1.29:1 vs bg — "barely visible", as the Blueprint guide prescribes |
| text | `#1A1A1A` | 16.1:1 on bg |
| muted text | `#6B6B66` | 4.95:1 on bg (AA) |
| accent | `#1D4ED8` (ink blue) | 6.2:1 on bg — usable for text and strokes |
| secondary accent | `#D97706` (amber) | 2.95:1 — strokes/fills only, never text; use `#B45309` (4.6:1) if amber text is needed |
| display font | **Inter** or **Geist** (OFL) | Inter Tight for headlines if tighter tracking wanted |
| mono font | **Geist Mono** or **JetBrains Mono** (OFL) | labels, dimensions, data |
| stroke widths | 1 px grid, 2 px diagram lines, 3 px emphasised path | at 1080 px wide, 2 px reads as "pen" |
| corner radii | 0 px on diagram boxes; 4 px on callout cards | Linear-style cap of 8 px max |
| caption | Inter 700, 64 px, text `#1A1A1A`, optional pill `#FFFFFF` at 90% with 1 px `#DCDAD3` border | |

### Motion language
- **Draw-on** is the signature: strokes animate via `stroke-dashoffset` with ease-out over 600–800 ms, as if being inked. Arrowheads pop in last (120 ms).
- Labels **type on** in mono (character-reveal, ~20 ms/char, capped at 400 ms).
- Grid is static; the "paper" never moves. Camera moves are limited to a slow 2–4% zoom on a held diagram.
- Highlight = accent stroke thickens from 2 to 3 px and the hairline grid under the object fades to 0 for a moment ("spotlight by subtraction").
- Transitions between ideas: horizontal wipe along a hairline (300 ms), or cross-fade (250 ms). No slides.
- Dimension ticks and bracket annotations extend from the object (scaleX from 0, 250 ms).

### Diagram primitives that suit it
Boxes-and-arrows system diagrams, timelines with tick marks, call-outs with leader lines, dimension brackets, dotted "data in flight" paths, request/response sequence diagrams, exploded-view stacks (layers separated with hairline connectors), small inline tables set in mono.

---

## 2. Direction B — "Dark Instrument Panel / FUI"

### Description
Near-black ground with thin cyan line work, HUD-style readouts and tick-mark gauges — the sci-fi-lab reading of the brief, kept restrained so it stays explanatory rather than decorative. Texture (a faint scanline or vignette) is allowed only at 2–4% opacity; the Blade Runner 2049 lesson is that the most "advanced" interface in that film (Wallace Corp) was pure, minimal, geometric black-and-white, not busy.

### References
- Territory Studio — Blade Runner 2049 screen graphics (minimal/utilitarian for Wallace, degraded for K's spinner, interfaces built per story beat) — https://territorystudio.com/project/blade-runner-2049/
- GMUNK / Bradley Munkowitz — Oblivion GFX "Light Table" (brief: functionality and minimalism, bright unified palette that works on dark and light) — https://gmunk.com/OBLIVION-GFX
- HUDS+GUIS archive of film UI — https://www.hudsandguis.com/home/2018/blade-runner-2049 and https://www.hudsandguis.com/2013/05/02/oblivion-interface-design/
- Cantina Creative (BR2049 post-production screens) — https://www.cantinacreative.com/film/blade-runner-2049
- Apple WWDC dark keynote slides: colour carries meaning consistently, one element animated in at a time, generous spacing instead of bullets — https://medium.com/iconic-slides/iconic-slides-7-rules-apples-slide-decks-teach-us-about-creating-insanely-great-presentations-65bc45051c72
- Linear (dark by default, monochrome surfaces, accent capped to one appearance per viewport, radius ≤ 8 px, no drop shadows) — https://linear.app (tokens via opendesigner.io)
- Teenage Engineering (OP-1 / TP-7): instrument-grade restraint, grey body with one or two saturated accents — https://teenage.engineering

### Tokens
| Token | Value | Note |
|---|---|---|
| background | `#070A0D` | near-black with a blue bias |
| surface | `#0E131A` | panels |
| grid / rules | `#1C2430` at 1 px | 1.27:1 vs bg |
| text | `#E6EDF3` | 16.8:1 |
| muted text | `#7B8794` | 5.4:1 |
| accent | `#22D3EE` (cyan) | 11.0:1 — safe for text, strokes, glows |
| secondary accent | `#F59E0B` (amber) | 9.2:1 — warnings, "the thing to look at" |
| display font | **Space Grotesk** (OFL) for headings; **Inter** for body | Space Grotesk's squared forms read "instrument" |
| mono font | **JetBrains Mono** or **IBM Plex Mono** (OFL) | readouts, coordinates, hex |
| stroke widths | 1 px rules, 1.5 px diagram lines, 2 px active path; optional 6 px blurred glow at 30% behind active path | thin is the point |
| corner radii | 0–2 px; chamfered corners (clip-path) for panels instead of radius | |
| caption | Inter 700, 64 px, `#E6EDF3`, pill `#0E131A` at 85% with 1 px `#1C2430` border | |

### Motion language
- **Build-up readouts:** numbers count up (value-change principle) over 400–600 ms with ease-out; text labels decode (random glyphs → final string) over ≤ 300 ms, used at most once per video.
- **Radial sweeps:** gauges and progress rings fill via `stroke-dasharray`, 500 ms ease-in-out.
- **Scan-line reveal:** a 1 px cyan line sweeps top-to-bottom (400 ms) and the diagram appears behind it — the "wipe" for this look.
- Target brackets `[ ]` snap to the highlighted object (200 ms, slight overshoot), replacing colour-fill highlighting.
- Idle state has a 2–3 s subtle pulse on a single status dot only; everything else is still.
- Transitions: hard cut on a frame flash of the grid (2 frames) or a horizontal scan-wipe; no fades longer than 200 ms (fades feel soft, this look is crisp).

### Diagram primitives
Node graphs with glowing active edges, packet/signal paths with travelling dots, concentric radar/ring layouts, horizontal bar "telemetry" readouts, state machines with bracketed active state, cross-section views with reticle call-outs, vertical stack diagrams (layers as thin plates).

---

## 3. Direction C — "3Blue1Brown Midnight"

### Description
Deep navy-black with soft, slightly luminous vector primitives and a palette borrowed directly from Manim's defaults: a blue for the "thing", a yellow for the "attention", greys for scaffolding. It is the most pedagogical direction — colour is semantic, not decorative — and the one closest to the stated inspiration. Keep it from becoming a maths-channel clone by using Manim's palette logic (A→E tints) but a different type voice and vertical composition.

### References
- 3Blue1Brown / Manim (background `#1C1C1C` in 3b1b's own renders; community palette below) — https://www.3blue1brown.com/faq/ and https://docs.manim.community/en/stable/reference/manim.utils.color.manim_colors.html
- 3b1b-style guidance: motivate before defining, concrete before general, let visuals explain — https://cdn.jsdelivr.net/gh/subinium/3b1b-style-animation-skill@main/README.md
- Linear dark theme (monochrome surfaces, single accent) — https://linear.app
- Apple WWDC slides (colour = meaning, reveal as you speak) — see Direction B reference
- Vercel dark mode: pure black/white inversion, accent `#0070F3` only at CTAs — https://vercel.com/geist
- Josef Müller-Brockmann grid discipline — https://www.printmag.com/?p=1387

### Tokens
| Token | Value | Note |
|---|---|---|
| background | `#0B1020` | navy-black (3b1b uses `#1C1C1C`; the blue bias separates us from it) |
| surface | `#121A2E` | |
| grid | `#1E2A44` at 1 px (optional, usually off) | 1.33:1 |
| text | `#F2F4F8` | 17.2:1 |
| muted text | `#8A93A6` | 6.1:1 |
| accent | `#58C4DD` (Manim BLUE_C) | 9.3:1 — the subject |
| secondary accent | `#F4D345` (Manim YELLOW_D) | 12.9:1 — the highlight / "look here" |
| extended semantic set | GREEN_C `#83C167`, RED_C `#FC6255`, TEAL_C `#5CD0B3`, GREY_B `#BBBBBB` | positive, negative, alternate, scaffolding |
| display font | **Inter** (OFL), 600 for headings; or **Instrument Sans** for a slightly more editorial voice | |
| mono font | **IBM Plex Mono** (OFL) | formulas, code, values |
| stroke widths | 3 px primitives (Manim default feel), 1.5 px scaffolding/axes, 4 px emphasised | |
| corner radii | geometry is exact (circles, rects at 0 px); UI cards 8 px | |
| caption | Inter 700, 66 px, `#F2F4F8`; no pill by default; pill `#0B1020` at 85% when over a diagram | |

### Motion language
- **Create/Write:** paths draw on with ease-in-out, 800–1000 ms (slower than UI motion — this is thinking speed, not interface speed).
- **Transform:** one shape morphs into the next (SVG path interpolation / FLIP) rather than one fading out and another in — continuity of the object is the core idea.
- **Indicate:** highlight by a brief scale-up to 1.08 and colour flip to yellow (300 ms), then settle.
- **FadeIn with shift:** new labels rise 12 px while fading (350 ms).
- Camera: slow dolly in/out (2–3 s) to re-frame on the next idea instead of cutting.
- Soft glow (2–4 px blur at 25%) under the accent colour only, giving the "luminous chalk" feel.

### Diagram primitives
Number lines and axes, vectors/arrows that re-point, circles and arcs, grids that deform (linear-transform style), braces with labels, flow of dots along a path, highlighted sub-regions (translucent fills at 15–20%), equation-to-diagram mappings using matching colours.

---

## 4. Direction D — "Clinical White / Apple Keynote"

### Description
Pure white, very large type, grey diagrams, one saturated accent, and more negative space than feels comfortable. It is the loudest of the five in a feed precisely because it is empty; the diagram is the only object on screen and the caption is often the headline. Risk: without the grid or mono accents it can look generic, so keep the Swiss rigour (strict column grid, asymmetric placement).

### References
- Apple keynote / WWDC slide language (one idea, reveal-as-you-speak, consistent colour semantics, spacing instead of bullets) — https://medium.com/iconic-slides/iconic-slides-7-rules-apples-slide-decks-teach-us-about-creating-insanely-great-presentations-65bc45051c72
- Vercel marketing (pure white/black, foreground is the inverse, `#0070F3` accent only at key moments; 96 px / 56 px heroes, weight 700, line-height 1.0 for headlines) — https://vercel.com and https://vercel.com/design.md
- Stripe docs (whitespace-heavy, charcoal text, accent as punctuation) — https://stripe.com/docs
- Braun / Dieter Rams, "as little design as possible" — https://designexplained.substack.com/p/dieter-rams-and-ten-principles-for
- Swiss International Style / Helvetica lineage — https://www.printmag.com/?p=1387
- NASA Graphics Standards Manual (Helvetica + red, nothing else) — https://wearethemutants.com/2020/01/09/unity-precision-thrust-the-nasa-graphics-standards-manual-1975/

### Tokens
| Token | Value | Note |
|---|---|---|
| background | `#FFFFFF` | |
| surface | `#F5F5F7` | Apple-grey panels |
| grid | `#E8E8ED` (hairline, used only as dividers, never a full grid) | |
| text | `#111111` | 18.9:1 |
| muted text | `#6E6E73` | 5.1:1 |
| accent | `#0070F3` (or a single warm `#FF3B30`) | 4.55:1 — passes AA for text; prefer ≥ 24 px when used as text |
| secondary accent | none — use `#111111` fills | the discipline of this look is one colour |
| display font | **Inter Tight** or **Geist** (OFL), 600–700, tight letter-spacing (−0.02 em) | Geist explicitly cites Swiss principles and SF Pro as influences |
| mono font | **Geist Mono** (OFL), used sparingly for values only | |
| stroke widths | 2 px diagram lines in `#111111`; 2 px accent path; no hairline diagrams (they vanish on white at phone size) | |
| corner radii | 12–16 px on cards (Apple-like); 0 px on technical diagrams | |
| caption | Inter Tight 700, 72 px, `#111111`; no pill; when over a diagram use a white 90% pill with no border | |

### Motion language
- **Fade + scale:** elements enter from 0.96 → 1.0 scale with a 300 ms ease-out fade — the Keynote "magic move" feel.
- **Slide-in-place:** type blocks slide 24 px with 350 ms ease-out, never further.
- Diagrams build piece by piece, each piece on its own beat; nothing else moves while a piece enters.
- Colour arrives last: a diagram builds in grey, then the accent fills the one element the sentence is about (200 ms).
- Transitions: 250 ms cross-fade through white; occasional full-frame headline card between ideas.
- Large numbers count up with ease-out over 600 ms.

### Diagram primitives
Big-number statements, two-column before/after comparisons, simple flow arrows (3 nodes maximum per frame), pie/bar primitives with grey + one accent, device/screen mockups in grey outline, iconography in a single 2 px stroke weight.

---

## 5. Direction E — "Monochrome Mono-type / Terminal Lab"

### Description
Black and white only, every piece of text in monospace, one signal colour reserved for the active element, dotted connectors and ASCII-ish ligatures. It reads as "the lab's terminal", is extremely fast to produce in HTML/CSS (no illustration, no gradients), and leans into the 2026 trend of monospace moving out of code editors into editorial design. Risk is coldness; the signal colour and generous leading keep it human.

### References
- 2026 type trend: monospace as an editorial/brand voice (JetBrains Mono, Geist Mono, Fragment Mono, IBM Plex Mono, DM Mono named) — https://madegooddesigns.com/font-trends-2026/
- Vercel Geist Mono: intended for code editors, diagrams, terminals — https://github.com/vercel/geist-font
- Linear (engineering-first minimalism, monochrome, 4 px spacing multiples, radius ≤ 8 px) — https://linear.app
- Teenage Engineering product and web typography (mono labels, grey/black, single accent) — https://teenage.engineering
- Berkeley Mono (commercial — reference only, not usable) — https://usgraphics.com/products/berkeley-mono
- Braun / Rams reduction — https://designexplained.substack.com/p/dieter-rams-and-ten-principles-for
- Blade Runner 2049 Wallace Corp UIs: pure minimal geometric black-and-white — https://territorystudio.com/project/blade-runner-2049/

### Tokens
| Token | Value | Note |
|---|---|---|
| background | `#0A0A0A` | (invertible: `#F5F5F5` bg / `#0A0A0A` text works identically) |
| surface | `#141414` | |
| grid | `#222222` 1 px, or 2 px dot grid at 32 px | 1.24:1 |
| text | `#F5F5F5` | 18.2:1 |
| muted text | `#8C8C8C` | 5.9:1 |
| accent (signal) | `#39FF88` (phosphor green) or `#FF5A1F` (safety orange, 7.9:1) | green is 14.9:1 — use for exactly one element per frame |
| secondary accent | `#FFFFFF` (pure white = emphasis) | no second hue |
| display font | **JetBrains Mono** or **Geist Mono** (OFL), 700 for headlines at 72–88 px | mono headlines are the signature |
| mono font | same family at 400/500 | one family, all weights |
| stroke widths | 1 px rules, 2 px dotted connectors (`stroke-dasharray: 2 6`), 2 px solid for the active path | |
| corner radii | 0 px everywhere; bracket corners `┌ ┐` drawn as 1 px L-shapes on panels | |
| caption | JetBrains Mono 700, 60–64 px (mono is wider — 8 words at 64 px ≈ 900 px), `#F5F5F5`, pill `#0A0A0A` 85% | cap lines at ~22 characters |

### Motion language
- **Cursor and type-on:** the only entry animation for text (12–18 ms/char, a 1 ch blinking block cursor that leaves when the line finishes).
- **Dotted connectors march:** `stroke-dashoffset` loops slowly (1.5 s/cycle) to show direction of flow; stops when not the subject.
- **Blink-highlight:** active node inverts (white fill, black text) for 120 ms then settles to signal-colour outline.
- Panels appear by drawing their four bracket corners first (150 ms) then the content types in.
- Transitions: hard cuts, or a one-line "clear" (content wipes bottom-to-top in 200 ms like a terminal scroll). No fades.
- Nothing eases softly; use `cubic-bezier(0.2, 0, 0, 1)` (fast-out, abrupt-in) to keep it mechanical.

### Diagram primitives
Box-drawing-character style flowcharts (rendered as SVG, not actual glyphs), trees and nested lists, key→value tables, request/response logs that print line by line, memory/array cells, protocol frames (byte fields as boxes), status badges in brackets.

---

## 6. Typography: what "clean tech" looks like in 2026

Findings from the trend pieces and design-system docs reviewed:

- **Neo-grotesk has plateaued.** Inter, Geist and SF Pro now read as "default" rather than designed. They remain the safe workhorse, but a channel wanting a recognisable voice should pair one with a distinctive mono or a slightly softer/squarer grotesk.
- **Monospace moved into editorial.** JetBrains Mono, Geist Mono, IBM Plex Mono (called underused), DM Mono, Space Mono and Fragment Mono are the named free picks; Berkeley Mono is the paid favourite. A mono-headline voice is on-trend and cheap to render in CSS.
- **Soft/warm geometrics** (Space Grotesk, Outfit, Plus Jakarta Sans, Albert Sans, Hanken Grotesk, General Sans, Mona Sans) are the "bouba grotesk" counter-trend — rounded terminals, friendlier. Space Grotesk is the one that still reads technical.
- **Variable fonts are the default** for serious releases; one file covering weight/width/optical size helps HTML rendering stay light.
- **Geist specifics:** OFL 1.1; Geist Sans is a geometric sans drawing on Swiss principles, influenced by Inter, Univers, SF Pro, Suisse International and ABC Diatype; Geist Mono is intended for code, diagrams and terminals. Vercel's own guidance: design in monochrome, use colour only for meaning, mono only for code/paths/timestamps/identifiers, default to stillness.
- **Linear specifics:** Inter Variable only; hierarchy via weight/size/leading; radius capped at 8 px; spacing in 4 px multiples (8/12/16/24, sections 64/96); no gradients; no more than two accent colours per page.
- **Stripe specifics:** Söhne (commercial) for display; accent `#635BFF` used only as punctuation; body 17 px / 1.55 leading.

**Usable (OFL / free) shortlist for tech_splained**

| Role | Fonts | Why |
|---|---|---|
| Display sans | Inter / Inter Tight, Geist, Space Grotesk, Instrument Sans, Manrope | all OFL on Google Fonts; Inter Tight and Geist give the "Söhne-like" tight headline look without a licence |
| Mono | JetBrains Mono, Geist Mono, IBM Plex Mono, DM Mono, Space Mono, Fragment Mono | OFL; JetBrains Mono has the largest x-height (best at 60 px captions); IBM Plex Mono has the most character |
| Avoid | Söhne, Suisse Int'l, Berkeley Mono, SF Pro/SF Mono, Helvetica | commercial or Apple-platform-only |

---

## 7. Burned-in captions on mobile: accessibility and style

- **Size:** 60–75 px on a 1080×1920 frame (3.1–3.9% of height) is the consensus; 65–70 px semibold or 60–65 px bold are the recommended defaults; 55 px is the floor for primary captions; above ~100 px text covers the content. One source frames caption height at 7–10% of frame height (BBC standard ≈ 8%) for broadcast-style subtitles, which is more generous than the Reels norm.
- **Weight/size pairings:** 600 @ 65–70 px (polished), 700 @ 60–65 px (default), 800–900 @ 55–60 px (compact). Thin weights at any size test poorly.
- **Line length:** word-by-word (1–3 words) or short phrases (3–8 words) on one line; full sentences capped at two lines, ~42 characters/line (Netflix). Mono fonts are wider, so cap at ~22 characters/line at 64 px.
- **Placement:** centred, inside a ~900 px wide column; keep ≥ 450–480 px from the bottom and ≥ 220 px from the top; avoid the right 120 px.
- **Treatment ranking (readability):** background box > outline > drop shadow. A 70–80% opaque box keeps ~15:1 and is immune to the content behind it; a 3–4 px stroke (not 1–2 px) is reliable on neutral backgrounds and is the common Reels style; shadow alone can fall below 4.5:1 on light frames.
- **Contrast targets:** WCAG 1.4.3 — 4.5:1 normal text, 3:1 large text; aim for AAA (7:1) because viewing conditions outdoors are poor. Check the brightest and darkest frames, not just one.
- **Timing:** captions must sync with audio, especially in the first 3 s; a late caption is more distracting than none. Hold each caption long enough to read; don't flash words so fast the viewer reads ahead.
- **Implication for the five directions:** every direction has a flat, controlled background, so the caption can sit directly on the background with no pill most of the time (all five text/bg pairs are ≥ 16:1). Add the pill only when a caption overlaps a diagram. For Direction D (white), text must be the dark `#111111` — never the accent — because `#0070F3` only just passes AA.

---

## 8. Motion principles for explainer diagrams

Synthesised from the motion-design sources and the 3Blue1Brown approach:

1. **Purpose test:** if you cannot name what a motion communicates (state change, attention, continuity, relationship), it shouldn't move. Default to stillness.
2. **One idea per frame:** build the diagram one element per spoken clause; nothing else moves while the new element enters. Apple's decks and 3b1b both animate elements in as they are mentioned.
3. **Reveal order = reading order:** primary object first and most prominent, secondary elements staggered after (40–80 ms offsets); a cascade feels intentional, simultaneous appearance feels chaotic.
4. **Continuity / persistence:** treat every object as a real thing that moves through space. Transform A into B (morph, FLIP, shared-element) rather than fading A out and B in; the viewer must never lose track of "which one is that".
5. **Colour as meaning, consistently:** one colour = one concept for the whole video (and ideally the whole channel). 3b1b: blue = the subject, yellow = attention; Apple decks: each category keeps its colour across slides.
6. **Easing:** ease-out entering, ease-in leaving, ease-in-out moving; never linear. Objects should cover more distance mid-move than at the ends.
7. **Durations:** UI-scale 200–500 ms (under ~100 ms is missed, over ~500 ms feels slow); diagram draw-ons may run longer (600–1000 ms) because they are thinking speed, not interface speed. Micro-interactions shorter, large transitions slightly longer.
8. **Motivate before defining:** open with the question or the concrete example, then the mechanism, then the general rule (3b1b's "start with why").
9. **Highlight by subtraction as much as addition:** dim the rest (to muted grey) rather than only brightening the subject; this preserves the "colour used sparingly" brief.
10. **Camera moves are transitions:** a slow dolly/zoom to re-frame on the next idea beats a cut when the objects persist; cut only when the subject changes entirely.
11. **Reduced-motion fallback:** keep a cross-fade variant of every transition; also useful for very short clips where there isn't time for a draw-on.

---

## 9. Quick comparison

| | A Lab Notebook | B Instrument Panel | C 3b1b Midnight | D Clinical White | E Terminal Lab |
|---|---|---|---|---|---|
| Ground | off-white paper | near-black blue | navy-black | pure white | pure black |
| Accent discipline | 1 ink + amber strokes | cyan + amber | semantic palette (blue/yellow + 3) | one colour only | one signal colour |
| Type voice | sans + mono labels | squared grotesk + mono | humanist sans + mono formulas | tight sans, large | all mono |
| Signature motion | ink draw-on | scan-wipe, count-up | morph/transform | fade-scale, colour-arrives-last | type-on, marching dots |
| "Sci-fi lab" strength | low–medium (drafting lab) | high | medium | low (clinic) | medium–high |
| Feed differentiation | high (light frame) | medium (many dark FUI clips exist) | medium | high | medium |
| Production cost in HTML/CSS | low | medium (glows, gauges) | medium–high (path morphing) | low | lowest |
| Clone risk | Vercel/Stripe look-alike | generic HUD | "another Manim channel" | generic Keynote | hacker aesthetic |

A reasonable hybrid worth prototyping: Direction A's paper grid and ink draw-on as the default frame, with Direction C's semantic colour rules and Direction E's mono labels — that covers "clean", "lab", "diagram-led" and avoids the dark-FUI clone risk.

---

## Sources

Typography and design systems
- https://madegooddesigns.com/font-trends-2026/
- https://github.com/vercel/geist-font
- https://vercel.com/geist
- https://vercel.com/geist/font
- https://vercel.com/design.md
- https://opendesigner.io/blog/recreating-stripe-linear-vercel-design-systems-with-design-md
- https://www.setproduct.com/blog/complete-guide-to-blueprint-grid-design
- https://www.framer.com/marketplace/components/blueprint-grid/
- https://linear.app
- https://stripe.com/docs
- https://teenage.engineering
- https://usgraphics.com/products/berkeley-mono

Historical / industrial-design references
- https://wearethemutants.com/2020/01/09/unity-precision-thrust-the-nasa-graphics-standards-manual-1975/
- https://www.printmag.com/?p=1387 (Swiss Style principles, typefaces, designers)
- https://designexplained.substack.com/p/dieter-rams-and-ten-principles-for

FUI / screen graphics
- https://territorystudio.com/project/blade-runner-2049/
- https://www.hudsandguis.com/home/2018/blade-runner-2049
- https://www.hudsandguis.com/2013/05/02/oblivion-interface-design/
- https://gmunk.com/OBLIVION-GFX
- https://www.cantinacreative.com/film/blade-runner-2049
- https://vfxblog.com/2017/11/08/a-visual-journey-through-the-screen-graphics-of-blade-runner-2049

3Blue1Brown / Manim
- https://www.3blue1brown.com/faq/
- https://docs.manim.community/en/stable/reference/manim.utils.color.manim_colors.html
- https://docs.manim.community/en/stable/reference/manim.utils.color.html
- https://cdn.jsdelivr.net/gh/subinium/3b1b-style-animation-skill@main/README.md

Presentation design
- https://medium.com/iconic-slides/iconic-slides-7-rules-apples-slide-decks-teach-us-about-creating-insanely-great-presentations-65bc45051c72

Captions, safe zones, contrast
- https://www.clipspeed.ai/blog/instagram-reels-captions.html
- https://blitzcutai.com/blog/best-caption-size-instagram-reels-2026
- https://blitzcutai.com/blog/caption-background-vs-outline-vs-shadow
- https://kineclip.com/blog/caption-readability-checklist-short-videos-2026/
- https://www.hopperhq.com/blog/instagram-reel-size/
- https://www.trymypost.com/blog/instagram-reels-safe-zones-text-placement-2026

Motion design
- https://madegooddesigns.com/motion-design-principles/
- https://uxdesign.cc/a-guide-to-motion-design-principles-7f05f10ccd79
- https://uxdesign.cc/disneys-12-principles-of-animation-exemplified-in-ux-design-5cc7e3dc3f75
