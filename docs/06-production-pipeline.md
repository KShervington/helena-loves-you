# 06 — Production pipeline

How a scripted, storyboarded video becomes an MP4. Everything here is HTML-based (Kyle's call) and built on the render pipeline already proven in the Gaijin Motorsports library, extended with narration sync. Renderer and voice choices are still under test — see `10-decision-log.md`; the evidence is in `docs/research/renderer-stack.md` and `docs/research/audio-tts-music-sfx.md`.

## The stack

```mermaid
flowchart LR
  S[script.txt + lexicon.json] --> T[TTS → narration.wav]
  T --> A[word timestamps → narration.json]
  A --> C[comp.html<br/>library primitives · render(t)]
  C --> ST[stills check]
  ST --> F[capture.mjs frames<br/>+ textless]
  M[music bed + SFX] --> X[audio.sh mix −14 LUFS]
  F --> E[encode.sh → MP4 + poster]
  X --> E
  E --> Q[/ts-qa/]
```

| Step | Tool | Where it lives |
|---|---|---|
| Voice | ElevenLabs (v4 / Multilingual v2, Creator plan) **or** a local open model (Chatterbox Turbo, Kokoro-82M) — bake-off pending | `tests/tts-bakeoff/` runners → promoted to `library/assets/tools/narration/` |
| Word timestamps | native from the TTS when available; otherwise CTC forced alignment against the known script (`align.py`); ASR only as a last resort | same |
| Composition runtime | `GML.core` (easing, keyframes, beat grid), `GML.narration`, `GML.captions`, diagram primitives | media library |
| Frame capture | `capture.mjs` (Playwright, parallel workers, stills, transparent element export) | media library `tools/render-pipeline` |
| Audio | `audio.sh` (trim, fade, duck, mix, −14 LUFS), `sfx-kit` (synth SFX tuned to the bed's key) | media library |
| Encode | `encode.sh` (H.264, yuv420p, poster as frame 0) | media library |
| Music | a vetted pool of beds in the library (generated with ACE-Step on the Mac, or CC0 from Pixabay/FMA; Eleven Music if on the ElevenLabs plan) with beat maps | media library `assets/audio/` |

Alternatives evaluated (`docs/research/renderer-stack.md`): HeyGen **HyperFrames** (Apache-2.0; `data-start`/`data-duration` clips driven by one paused GSAP timeline; Puppeteer capture with CDP `beginFrame`; a 450-block registry; `transcribe --json` and Kokoro TTS built into its media skill; ~3 min for 30 s of 1080p locally) and **Remotion** (React → video; free for ≤ 3 people, so a one-person LLC qualifies; `@remotion/captions` with TikTok-style paging; Lambda rendering ~10× faster than local; official agent skills). Motion Canvas is canvas-only and editor-driven — not a fit. Verdict: **own pipeline stays primary** (it exists, it's a pure function of time, narration sync is already native to it), hardened with what the others do better: CDP `beginFrame` capture instead of per-frame screenshots, a lint that forbids `Date.now`/`Math.random`/timers/network in compositions, HyperFrames' caption grouping rules (2–6 words, hard cuts between groups), and a VLM pass over stills before the full render. The formal bake-off (same 15 s scene in own pipeline vs HyperFrames) is D-03 in the decision log.

## The composition contract

A video is one HTML page, `Project_Files/comp.html`:

```html
<link rel="stylesheet" href="../Assets/Brand/tokens.css">
<body class="ts-<direction>">
<script>window.GML = { root: "<library root or ../Assets" }</script>
<script src="…/core.js"></script> <script src="…/narration.js"></script> <script src="…/captions.js"></script> <script src="…/pipeline.js"></script>
<script src="narration.json.js"></script>
<script>
  const N = GML.narration.create(window.NARRATION);
  window.SIZE = { width: 1080, height: 1920 }; window.DURATION = Math.ceil(N.duration + 0.5);
  window.ready = (async () => { /* create primitives; await GML.core.ready([...images]); render(0) */ })();
  window.render = (t) => { /* pure function of t; every reveal time is N.at("word") */ };
  window.isolate = (sel) => { /* hide everything but sel, for transparent exports */ };
</script>
```

Rules the contract enforces:
- `render(t)` is pure. No timers, no `requestAnimationFrame`, no CSS animations that depend on wall-clock.
- **Every reveal time comes from `narration.json`** (`N.at`, `N.end`, `N.beat`). Re-record the voice → the video re-times itself.
- `?textless=1` hides the caption layer for the master in `Raw_Footage/`.
- Fonts and images are awaited before frame 0 (`GML.core.ready`).
- One direction class on `<body>`; components read only tokens.

`tech-splained-media-library/examples/explainer-demo/demo.html` is the working starter.

## Step by step (what `/ts-produce` runs)

```bash
L=../tech-splained-media-library; P=$L/assets/tools/render-pipeline; PF=Project_Files
# 1 voice + timestamps (provider per decision log)
node   $L/assets/tools/narration/elevenlabs.mjs $PF/script.txt $PF --model eleven_v4 --voice $VOICE --lexicon $PF/lexicon.json
#  or: python3 $L/assets/tools/narration/kokoro.py $PF/script.txt $PF --voice af_heart
#  or: python3 chatterbox.py … && python3 align.py $PF/narration.wav $PF/script.txt $PF/narration.json
# 2 compose → comp.html (from the demo), then stills at scene boundaries, mid-transitions, busiest frames
node $P/capture.mjs $PF/comp.html stills /tmp/stills 0 2.8 9.1 9.4 21 33.5 47
# 3 music + SFX (bed from the library; cues from the shot list; duck under speech)
bash $P/audio.sh $L/assets/audio/<bed>/<bed>.mp3 <start> <dur> /tmp/bed.wav
node $L/assets/tools/sfx-kit/cues.mjs $PF/cues.json > /tmp/sfx-args          # reveal ticks, transition whooshes, CTA chime
bash $P/audio.sh --voice $PF/narration.wav --music /tmp/bed.wav --duck 12 /tmp/mix.wav $(cat /tmp/sfx-args)
# 4 frames (+ textless) and encode
node $P/capture.mjs $PF/comp.html frames /tmp/frames --workers 4
node $P/capture.mjs $PF/comp.html frames /tmp/frames-textless --query textless=1
bash $P/encode.sh /tmp/frames          /tmp/mix.wav Exports/<slug>_1080x1920.mp4 --poster <frame>
bash $P/encode.sh /tmp/frames-textless /tmp/mix.wav Raw_Footage/<slug>_textless_1080x1920.mp4
# 5 assets: stickers/cards as transparent PNGs, clean scene stills, fonts, audio stems → Assets/
node $P/capture.mjs $PF/comp.html element Assets/Graphics/Cards/hook.png --t 2.4 --selector '#h1'
```

(`audio.sh --voice/--duck` is the one extension the Gaijin script needs for narration; until it lands, mix with the ffmpeg `sidechaincompress` recipe in the script's header comment.)

Render budget: a 50 s video is 1,500 frames; with 4 workers expect ~3–6 min capture on a laptop, ~1 min encode. One full render per video — stills first.

## Project folder

```
YYYY-MM-DD_Topic-Slug/
├── Assets/        Brand/ (tokens, fonts) · Graphics/{Cards,Diagrams,Screens} · Audio/ (voice, bed as used, each SFX, final mix) · Fonts/
├── Docs/          brief.md · script.md · shot-list.md · caption-pack.md · plan.md · qa.md · library-candidates.md (+ .jpg) · README.md
├── Exports/       <slug>_1080x1920.mp4 (poster = frame 0) · <slug>_poster.jpg
├── Project_Files/ comp.html · script.txt · lexicon.json · narration.{wav,json,json.js} · cues.json · render.sh · tools/ (copied pipeline)
└── Raw_Footage/   <slug>_textless_1080x1920.mp4 · untouched source media
```

Self-contained: `render.sh` must rebuild Exports from this folder alone (relative paths into `Assets/`).

## Media library

`tech-splained-media-library` mirrors the Gaijin library's rules: `INDEX.md` first, `ASSET.md` per asset, plumbing vs creative, `used_in`, candidates after every video, Kyle picks, PR per video, `build-index.mjs --check` in CI. Seeded with: brand tokens (five directions + fonts), `narration-sync`, `captions-word-sync`, `diagram-pipeline`, the render pipeline, the SFX kit, and the explainer demo. Next primitives to build, in order of how often scripts will need them: `counter`, `tiles`, `before-after`, `zoom`, `stack`, `graph`, `timeline`, `grid`, `cycle`, `title-card`, `cta-card`.

## Audio sources and licences

| Need | Use | Record in README |
|---|---|---|
| Voice | ElevenLabs paid plan (commercial) or Chatterbox Turbo (MIT) / Kokoro (Apache) / Qwen3-TTS (Apache). Never ElevenLabs Free, Edge-TTS, Fish, Higgs, F5, XTTS for finals. | provider, model, voice, date |
| Music beds | ACE-Step 1.5 generated on the Mac → library; CC0 from Pixabay / Free Music Archive; Eleven Music if on the plan. Not MusicGen (non-commercial), not YouTube Audio Library off-YouTube, Uppbeat free only with credit. | asset id, licence, window |
| SFX | `sfx-kit` synth; Freesound CC0; ElevenLabs SFX for organic sounds | asset id / source |

Any CC-BY asset adds its credit line to the caption pack automatically.

## Environments

- **Mac (daily):** everything above; local TTS and music generation run here.
- **Cloud agent session (no GPU, limited network):** composition, capture, encode and QA all work; use Kokoro CPU or the ElevenLabs API for voice; never generate music there — pull beds from the library.
