# Renderer stack for HTML-rendered short explainers (1080×1920, 30 fps, 45–60 s)

Research date: 2026-11-01. Scope: an AI coding agent (Claude Code) producing ~20–25 faceless tech explainers per month with animated diagrams, burned-in word-level captions, AI voiceover, music and SFX. Constraint: stay HTML-based. Baseline: the existing in-house pipeline (pure `render(t)` composition, parallel Playwright frame capture, ffmpeg with poster-as-frame-0, Python SFX synth + −14 LUFS mixer).

---

## 0. TL;DR

| Option | Licence | Authoring model | Render model | Captions | Agent tooling | Verdict for this use case |
|---|---|---|---|---|---|---|
| **Own Playwright pipeline** | yours | `render(t)` pure function | parallel per-frame screenshots → ffmpeg | your own | your own skills | **Keep as primary renderer.** Already deterministic, already parallel, zero licence/vendor risk. Harden with the beginFrame trick and font/image/media rules below. |
| **HyperFrames (HeyGen)** | Apache 2.0 | plain HTML + `data-start`/`data-duration` + paused GSAP timeline (`window.__timelines`) | Puppeteer/chrome-headless-shell, seek-per-frame, N Chrome processes for segments; Lambda/Cloud Run/HeyGen cloud | word-timed caption groups from `transcribe --json` / TTS `words[]`; `data-track-kind="captions"`; catalog caption styles; per-word emphasis | 7 published skills, non-interactive CLI, `check`/`lint`/`snapshot`, ~450-block catalog, Kokoro TTS, Parakeet/Whisper transcribe | **Borrow heavily** (contract rules, caption/explainer references, lint/check ideas, catalog blocks). Use as a second renderer for the bake-off; adopt only if it beats yours on agent effort. Local single-machine speed reported as slower than parallel-frame approaches. |
| **Remotion** | free ≤3 headcount incl. one-person LLCs; otherwise $25/seat/mo (Creators) or $0.01/render with $100/mo min (Automators) | React, `useCurrentFrame()` | headless Chrome, `--concurrency` local; Lambda (chunked, 75–150 default concurrency, max 200) | `@remotion/captions` (`Caption` type, `createTikTokStyleCaptions`), Whisper.cpp installer | official skills (`npx skills add remotion-dev/skills`), 13 skills incl. `/remotion-captions`; no official MCP found | **Not primary** (React + build step, licence rules to track as the company grows, worse fit for the "stay HTML" constraint). Borrow the caption data model (`Caption` → pages → tokens), `visualizeAudio()` idea, and Lambda chunking pattern. |
| **Motion Canvas** | MIT | TypeScript generators, own canvas scene graph (no HTML/CSS) | editor RENDER button → image sequence → external ffmpeg | none built in | community skills only | **Not a fit** (not HTML, browser-editor-driven export, no narration/caption tooling). Borrow the generator-style "yield each beat" sequencing idea for your scene DSL. |

**Recommendation:** keep your own pipeline as the production renderer; adopt HyperFrames' *composition contract and references* as the authoring spec your agent follows (so compositions remain portable to HyperFrames' renderer if you ever want its cloud render); run the 15 s bake-off described in §9 before importing anything else.

---

## 1. HyperFrames (HeyGen) — state in 2026

### 1.1 What it is
- Open-source (Apache 2.0) framework that turns HTML/CSS + seekable animations into deterministic MP4s; used in production at HeyGen, with tldraw and TanStack cited as adopters. Launched publicly mid-April 2026. The repo page fetched today reports ~76.7k stars (treat as approximate).
- Requirements: Node 22+, FFmpeg. No React, no bundler; `index.html` previews directly in a browser.
- Local skills vs hosted MCP: the HeyGen MCP's `compose`/`render_video` are disabled from CLI agents like Claude Code; local authoring is via skills (`npx skills add heygen-com/hyperframes`, or `npx hyperframes skills update`, which installs from `main`). `skills add` can lag `main` by hours.

### 1.2 Skills shipped (as of Nov 2026)
Core set: `/hyperframes` (render contract + work loop + references), `/hyperframes-cli` (init/lint/check/preview/render/cloud/publish/history), `/hyperframes-registry` (~450 blocks: transitions, overlays, titles, captions, charts, maps, 3D, camera moves — installed as editable source), `/media-use` (music, SFX, images, voiceover, avatar/generated video, transcripts; mixing). On demand: `/figma`, `/slideshow`, `/remotion-to-hyperframes` (ports Remotion/Motion Canvas/Lottie/Three/canvas work, verified frame by frame). Third-party mirrors also list `/faceless-explainer` as a route ("explain a topic with invented visuals, no product capture").

### 1.3 Composition format (the "render contract")
- Root `div` with `data-composition-id`, `data-start`, `data-duration`, `data-width`, `data-height`. Default new video: 1920×1080 @ 30 fps.
- Every timed element: `class="clip"`, `data-start`, `data-duration` (seconds), visible over `[start, start+duration)`, `data-track-index` for layering.
- One **paused GSAP timeline** per composition, registered **last**: `window.__timelines["<id>"] = tl`. Registering before tweens are built renders blank.
- Forbidden: `Date.now()`, unseeded `Math.random()`, network fetches at render time, timers, `repeat: -1`. Never tween `display`/`visibility`/`autoAlpha` on a `.clip` (animate a child). Never call `play()`/`pause()`/seek on media yourself.
- Audio: separate `<audio>` elements with `id` (no id → dropped from mix), `data-start`, `data-duration`, `data-track-index`, `data-volume`; `<video>` with its own sound uses `data-has-audio="true"`, else `muted`.
- Runtime adapters: GSAP (default), CSS `@keyframes` (finite iteration count, `animation-fill-mode: both`, `data-start` on element), WAAPI (`animate(…, {fill:"both"})` then `pause()`), Lottie (`autoplay:false`, push to `window.__hfLottie`), anime.js v4 (`autoplay:false`, push to `window.__hfAnime`, `anime.createSeededRandom`), Three/WebGPU/p5/canvas (draw inside an `hf-seek` listener using `e.detail.time`; `e.detail.waitUntil(promise)` for async decodes; `window.__hf.buildReady[key]` for heavy setup), and a custom adapter (`renderAt(t)`, call `renderAt(0)` on load). Charts/maps: drive from a GSAP tween's `onUpdate`, not the library's own transitions.
- Fonts: build timelines inside `document.fonts.ready` if needed; `fitTextFontSize` / `pretext` for measurement without reflow.

### 1.4 Rendering and performance
- HeyGen's own write-up: the renderer never plays; it calls `seek(t)` per frame, with times quantised to frame boundaries. On Linux it uses `chrome-headless-shell` + CDP `HeadlessExperimental.beginFrame` with flags that disable async scheduling, so each call does one layout/paint/composite/screenshot; macOS/Windows fall back to `captureScreenshot` plus readiness heuristics. Long videos are split across N Chrome processes, each rendering a segment, then ffmpeg concatenates. Video-heavy compositions fall back to one worker because Chrome can't seek multiple `<video>` elements concurrently; `<video>` sources are pre-extracted to JPEG frames by ffmpeg and swapped in as `<img>`.
- Engine uses Puppeteer (not Playwright). Preview and render runtimes are SHA-256 verified to match.
- Numbers (third-party review, spring 2026, M2 Pro): 10 s 1080p → 35–50 s; 30 s 1080p → ~3 min locally vs ~25 s on Remotion Lambda. Author calls single-machine speed "not competitive" for simple compositions. A HeyGen-sourced prompt-to-video benchmark (one prompt, Opus 4.7) reported 60 s HyperFrames vs 162 s + 4 min build for Remotion, and 4 MB vs 14 MB output — secondhand and single-sample.
- CLI render: `render --quality draft|high --output out.mp4`, `--docker` (+`--strict`), `--batch rows.json`, `cloud render` (HeyGen-hosted, 200 MB upload cap), `lambda render`, `cloudrun render`. No documented fps/CRF/concurrency flags in the skill text I could retrieve.
- Quality gates: `lint` (fast), `check` (lint + one browser session + one seek pass: runtime errors, failed requests, layout, `*.motion.json` assertions, WCAG contrast), `snapshot --at t1,t2,t3`, `preview --background`, `timeline --json`, `beats --json`, `keyframes --json`, `audio <file> --json`, `doctor --json`.

### 1.5 Audio, TTS, captions
- `/media-use`: HeyGen Voice Turbo free when signed in; other voices/cloning cost credits; local `npx hyperframes tts` runs Kokoro-82M on CPU (no key). Transcription: `npx hyperframes transcribe <file> --json` (Parakeet if installed, else whisper.cpp `small.en`); `--to srt|vtt`. Music: HeyGen catalog (10k+ tracks free when signed in), MusicGen locally. SFX: Openverse (CC BY, credit required) + 21 bundled sounds. Audio engine request/response (`audio_meta.json`) carries `voices[].words[]` word timestamps for captions, `sfx[]`, `bgm`, `total_duration_s`.
- Sound reference: narrated pieces — the voice sets the clock and text lands on its word; music-only — land payoffs on beats from `beats --json`. Music under voice ≈0.14 volume; true peak ≤ −1 dBTP; target −16 to −14 LUFS for social; SFX hits 3–6 dB above bed; align each SFX peak one frame after its picture; rotate 2–3 takes of repeated sounds; avoid chimes/dings. Verify the rendered file with `audio <video> --json` and state in the delivery note that loudness was measured.
- Captions reference: words are `{id, text, start, end}`; one host with `data-track-kind="captions"`; group size by energy (2–3 words high energy, 3–5 conversational, 4–6 calm); break on sentence end, ≥150 ms pause, or word limit; one group visible at a time; start the first group at 0.1–0.3 s not 0; hard-kill each group with `tl.set` at end time; size via `fitTextFontSize` (base 78 / min 42 px; `maxWidth` 900 portrait); portrait text 600–700 px from bottom, inside the 80% title-safe box; blend mode by background brightness (<60 screen, 60–180 overlay, >180 normal) with a text-sized scrim; whisper hallucination cleanup via `silencedetect=noise=-35dB:d=0.6`; per-word emphasis supported. Karaoke-style per-word highlight isn't spelled out as a mechanism, but the word timings and per-word styling support it.
- Audio-reactive: pre-extracted per-frame band data (0–1) mapped to GSAP-tweenable properties; runtime audio analysis is explicitly discouraged.

### 1.6 Limitations
- Seek-per-frame on one machine is slower than parallel-frame renderers; Lambda setup heavier than Remotion's; Studio GUI "evolving"; catalog still young; no first-party React adapter; audio sync "fiddly" (manual `data-start` math); Git LFS baselines ~240 MB (`GIT_LFS_SKIP_SMUDGE=1`); project-local skill installs can overwrite uncommitted `skills/` edits.

---

## 2. Remotion — state in 2026

### 2.1 Licence
- Free Licence: individuals (personal or commercial), teams of ≤3 people, non-profits, evaluators. **A one-person incorporated company qualifies** as long as total headcount is ≤3 (headcount counts the whole company, not just Remotion users). So a solo LLC is free today; it stops being free at 4 people.
- Company Licence: Creators $25/mo per person who writes Remotion code (including with agentic tools); Automators $0.01/render with $100/mo minimum; combined $100/mo minimum; Enterprise $500 minimum. Previews in Studio/Player don't count as renders; an image sequence counts as one render. Cloud rendering for companies needs Automators.
- Some third-party articles still describe older ARR-based tiers ($50/$200 per month) — the official FAQ above is authoritative.

### 2.2 Captions
- `@remotion/captions`: `Caption = {text, startMs, endMs, timestampMs, confidence|null}` (leading space on each word; spaces are delimiters). `createTikTokStyleCaptions({captions, combineTokensWithinMilliseconds, breakOnSilenceAfterMilliseconds})` → `pages[] = {text, startMs, durationMs, tokens[] = {text, fromMs, toMs, pageBreakAfter}}`. Low `combineTokensWithinMilliseconds` (or `breakOnSilenceAfterMilliseconds: 0`) yields word-by-word pages. Highlighting = find active page by `startMs ≤ t < startMs+durationMs`, then active token by `fromMs ≤ t < toMs`, render tokens as spans with `white-space: pre`. Whisper.cpp install/transcribe helpers feed this type.

### 2.3 Audio visualisation
- `@remotion/media-utils` (MIT): `getAudioData`/`useAudioData` + `visualizeAudio({audioData, frame, fps, numberOfSamples (power of 2), smoothing, optimizeFor:"speed"|"accuracy"})` → array of 0–1 amplitudes, bass on the left; `dataOffsetInSeconds` for windowed data. Usable outside Remotion (except the hook) — handy to pre-bake band data for your pipeline.

### 2.4 Rendering
- Local: headless Chrome, `--concurrency` (tune with `npx remotion benchmark`), JPEG faster than PNG, VP8/VP9 very slow, GPU-dependent CSS (shadows, blur, gradients, WebGL, 2D canvas) is slow on GPU-less cloud instances → pre-render to images. New `@remotion/media` `<Video>` is the optimised tag. Third-party figure: 150 frames at 1080p in 8–15 s on a typical CI runner.
- Lambda: project deployed to S3, many Lambdas each render a frame chunk, stitched by the first Lambda. Defaults: `framesPerLambda` ≥ 20, default concurrency 75→150 (interpolated to 10 min), hard max 200, min 5 frames/Lambda; ~80 min FHD max (15-min Lambda timeout), no AV1; "pennies" per few minutes of video. Cloud Run alternative. Third-party: ~25 s for a 30 s 1080p render.
- `@remotion/web-renderer` (stable from 4.0.491): renders in the browser via WebCodecs/Mediabunny, no bundling, limited CSS/tag subset.

### 2.5 Agent support
- Official Agent Skills: `npx skills add remotion-dev/skills` or `gh skill install remotion-dev/skills`; also offered by `bun create video`. Skills: `/remotion-best-practices`, `/remotion-create`, `/remotion-markup`, `/remotion-studio`, `/remotion-render`, `/remotion-maps`, `/remotion-captions`, `/remotion-saas`, `/remotion-interactivity`, `/remotion-docs`, `/remotion-license` (≥4.0.540), `/remotion-upgrade`, `/remotion-multimedia` (Mediabunny). Supported agents: Claude Code, Cursor, Codex, Kimi Code. No official MCP server on the skills page.
- TTS: official TTS template uses Azure Speech (`npx create-video@latest --tts`); community ElevenLabs skills exist. No first-party word-timing TTS integration beyond Whisper-based captioning.

---

## 3. Motion Canvas — status in 2026
- MIT, TypeScript, generator-based sequencing (`yield*` per beat), own canvas scene graph (`Txt`, `Rect`, `Img`…) — **no arbitrary HTML/CSS**. ~15–19.5k stars depending on snapshot, ~8k weekly npm downloads, core v3.x (v3.2.0 blog: status bar, world-space node caching, `Polygon` node). Repo last pushed within days of this research; 94–152 open issues; no maintenance-mode notice found, but also no 2026 roadmap found.
- Export: editor RENDER button writes an image sequence (PNG/JPEG/WebP) to `/output`; convert with external ffmpeg. Browser-driven; no documented CLI/headless render in the official rendering doc. Revideo (MIT) forks it with a Node render API + hosted rendering (re.video).
- Fit: strongest *authoring ergonomics* for long, scripted diagram explanations, but violates the "stay HTML" constraint and lacks captions/narration tooling. Borrow: the generator/"yield each beat" mental model and the "layout once, animate signals" discipline.

---

## 4. Keep-your-own-Playwright pipeline — best practices

### 4.1 Determinism rules (all converge across HeyGen, overcrank, Remotion)
- **Time**: everything derives from `t`. No `Date.now()`, `performance.now()`, `setTimeout`, rAF loops, unseeded `Math.random()`, `repeat:-1`, or network at render time. Quantise `t` to frame boundaries before seeking to avoid sub-pixel jitter between runs.
- **Fonts**: self-host and inline (HeyGen rewrites Google Fonts `@import` to base64 `@fontsource` copies); await `document.fonts.ready` *before* building timelines; measure layout once, never in `onUpdate`.
- **Images/SVG**: await `img.decode()` for every raster; inline SVG; wait for `complete` on all images before frame 0.
- **Video sources**: don't rely on `<video>` seeking under capture — pre-extract to JPEG frames at target fps and swap an `<img>` per frame (HeyGen's approach) or avoid video entirely in explainers.
- **Audio**: never in the browser. Mix separately (you already do this at −14 LUFS).
- **Canvas/WebGL**: draw synchronously inside the seek handler; for async GPU work, await a promise before capture. Patch/disable OffscreenCanvas; WebGPU makes determinism harder.
- **Readiness**: a naive screenshot loop races the renderer (missing fonts, unanimated styles). Either use `HeadlessExperimental.beginFrame` on Linux `chrome-headless-shell` (one layout/paint/composite per call) or wait two rAF ticks after seek with the Playwright clock paused.

### 4.2 Animation runtimes under seek
- **GSAP** (now 100% free including former Club plugins, thanks to Webflow — DrawSVG, MorphSVG, SplitText, ScrollSmoother, MotionPath, Inertia, Physics2D, CustomBounce/Wiggle): build one paused root timeline, `tl.seek(t, false)` per frame; absolute positions with `fromTo`; seed randomness (mulberry32). DrawSVGPlugin is the cheapest path-drawing primitive; MorphSVG for "morph each step out of the last".
- **anime.js v4**: `createTimeline({autoplay:false})`, `tl.seek(ms, muteCallbacks)`; `createSeededRandom`.
- **WAAPI**: `el.animate(kf, {fill:"both"}).pause()`, then set `anim.currentTime = ms` (ms, works while paused). `document.getAnimations()` lets you seek *every* WAAPI/CSS animation on the page generically — the simplest universal adapter if you avoid GSAP.
- **CSS `@keyframes`**: either `animation-play-state: paused` + negative `animation-delay: -t` (negative delay starts partway through the cycle — re-apply per frame), or convert to WAAPI via `getAnimations()`. Beware: compositor-driven CSS animations ignore JS clock patches (overcrank lists pure CSS as known-incorrect under virtual time), so prefer explicit seeking.
- **Theatre.js**: core Apache-2.0, studio AGPL; development moved to a private repo pending 1.0 — treat as risky dependency.
- **rough-notation** (MIT, 3.8 KB): underline/box/circle/highlight/strike/cross/bracket, `animationDuration`; it's `show()`-driven, not seekable. Port the idea by rendering rough.js paths and driving `stroke-dashoffset` from `t` (same technique HyperFrames' "marker-style highlighting" uses: highlight, circle, burst, scribble, sketchout via transforms + dashoffset).
- **Mermaid → SVG → animate**: render with mermaid (headless) to an SVG string, then DrawSVG/dashoffset the edges and stagger nodes. Dashmotion (MIT Claude skill) shows the pattern (flowchart/graph/stateDiagram-v2 → self-contained HTML/SVG with `stroke-dashoffset` streaming and `animateMotion` dots) but recomputes layout top-down and loops; use it for ideas, not as a renderer.
- **excalidraw-animate** (hand-drawn stroke reveal, SVG/WebM export, imperfect WebM) — treat as a style reference; drive your own hand-drawn look via rough.js + dashoffset.
- **D3**: use D3 for layout/scales only; drive attribute values from `t` (no `.transition()`).

### 4.3 Capture speed
- Per-frame `captureScreenshot` is deterministic and parallelises trivially across workers/segments (what you do; what HeyGen does). JPEG q≈80–90 for opaque frames; PNG only when alpha needed.
- `beginFrame` (Linux `chrome-headless-shell`, `--enable-begin-frame-control` family) ≈5 ms p50 per capture in overcrank's measurement vs tens of ms for screenshot — the biggest single-machine win, with caveats (stalled event loop needs a warm-up loop; `waitForFunction` can hang → poll manually).
- Canvas readback (`toDataURL`/`convertToBlob` of a single canvas) ≈0.6 ms p50 — only if your whole frame is one canvas.
- CDP screencast (`Page.startScreencast` / Playwright 1.59 `page.screencast.start`) is **variable-rate**: frames arrive only on repaint, size locks to the first client, timing must be rebuilt from wall clock, encoders must beat realtime or frames drift (reported 2 s drift over 90 s, 32% short recordings). Fine for live capture, wrong tool for deterministic offline rendering.
- Playwright `page.clock`: `install()` first, then `pauseAt()` + `runFor(ms)` steps `Date`, timers, rAF, `performance`, `Event.timeStamp`. Does not claim control over compositor CSS animations. Useful if you ever render third-party pages; for your own `render(t)` contract you don't need it.
- Parallelism: N browser contexts/processes over frame ranges, each encoding its own segment, then ffmpeg concat (HyperFrames) — or one encoder fed in order (yours). Keep poster-as-frame-0.

---

## 5. Burned-in captions in HTML

- Data model: adopt Remotion's `Caption` (`text` with leading space, `startMs`, `endMs`, `timestampMs`, `confidence`) as the interchange type; group into pages with the `createTikTokStyleCaptions` algorithm (page breaks on duration budget or silence gap), or HyperFrames' grouping heuristics (2–6 words by energy; break on sentence end, ≥150 ms pause, or limit).
- Rendering: one absolutely positioned full-width container (not `left:50%` + `translateX(-50%)`, which clips at edges), `overflow: visible`, tokens as inline-block spans, `white-space: pre`. Per frame: active page → active token → styles. Karaoke styles: (a) colour flip on the active word, (b) scale pop 1.0→1.08 with a 60–90 ms ease, (c) progressive fill via `background-clip:text` on the inner span with `background-size` driven by `(t - fromMs)/(toMs - fromMs)`.
- Safe zones (1080×1920): keep captions inside the 80% title-safe box; HyperFrames places portrait text 600–700 px from the bottom; never over a face; `maxWidth` ≈900 px; auto-fit font (base 78 / min 42). Use a text-sized scrim (30–40%) over busy backgrounds rather than a full bar.
- Hygiene: hard-kill every group at its end (`tl.set` opacity/visibility) so stale groups never linger; start the first group ≥0.1 s; fade group *or* words, not both; match transcript words to script words by position, not text.
- Timestamps sources (see §6): TTS alignment (ElevenLabs `with-timestamps`, HeyGen TTS `words[]`) or forced alignment (WhisperX, Parakeet, whisper.cpp). Normalise numbers/symbols: ElevenLabs returns both `alignment` and `normalized_alignment`; WhisperX borrows neighbouring timing for unalignable tokens (digits, symbols).

---

## 6. Voice-synced and audio-reactive animation

- **Narration sets the clock** (HyperFrames' explainer and sound references): reveal each diagram part when its word is spoken; ~19 spoken words per scene; labels appear with the part they name; text-only lines hold 0.5 s + 0.3 s/word.
- **Pipeline**: script → TTS → word timings → `beats.json` → composition. Word timings from: ElevenLabs `POST /v1/text-to-speech/{voice}/with-timestamps` (character start/end arrays → word spans by splitting on spaces); HeyGen TTS (`voices[].words[]`); or forced alignment of any TTS output via WhisperX 3.8.6 (May 2026; wav2vec2 phoneme alignment + DTW; JSON with per-word start/end), Parakeet, or whisper.cpp. Prefer TTS-native alignment when available and use forced alignment as a fallback/validator (diff the two; flag words differing by >120 ms).
- **Mapping words to beats**: tag the script with inline markers (`[[beat:db-write]]`) before TTS; strip markers for synthesis; map each marker to the start time of the next spoken word; emit `{beat_id, t}`; compositions reference beats by id, never by hard-coded seconds. Rule from HyperFrames: SFX peak lands one frame after its picture; captions land on the word.
- **Audio-reactive**: precompute per-frame band energies (0–1) offline (`visualizeAudio`-style FFT, or ffmpeg `astats`/`ebur128`) into `audio_features.json`; sample per frame inside `render(t)`. Never analyse audio at render time. Use for subtle pulses only (HyperFrames discourages equalizer-style visuals).
- **Music beats**: `beats --json`-equivalent (librosa `beat_track` or aubio) → land transitions/payoffs on strong beats; your preference stands: sync specific animations (button presses, stickers, transitions) to the beat, not the whole frame.

---

## 7. 2025–2026 open-source "AI explainer video" projects — what to borrow

| Project | Stack | Borrowable idea |
|---|---|---|
| **TheoremExplainAgent** (TIGER-AI-Lab, ACL 2025 oral, MIT) | Manim CE, planner → per-scene implementation plans → code; optional RAG over Manim docs (Chroma); Kokoro voiceover; `--use_visual_fix_code` (VLM fixes code from rendered frames); TheoremExplainBench (240 items) | **Plan-then-render split** with reviewable scene plans; **VLM visual-fix loop** on rendered stills (you have `snapshot`-style stills already); RAG over your own composition contract + block catalog; bounded retries and per-scene parallelism; multi-modal eval (text/image/video). |
| **Code2Video** (Show Lab NUS, NeurIPS 2025) | Planner / Coder / Critic agents; visual anchor prompts for spatial layout; MMMC benchmark from 3Blue1Brown-style tutorials; TeachQuiz (unlearn→relearn) metric; ~40% over direct codegen | **Critic with visual anchors**: give the Critic a grid of named anchor regions and have it flag overlap/occlusion per still. **TeachQuiz-style eval**: ask a fresh model to answer 3 questions after "watching" the transcript+stills. |
| **manimvox** (MIT, alpha 0.4.x) | Manim + 8 TTS engines (Kokoro default, Piper, edge-tts, OpenAI, ElevenLabs, XTTS/F5 non-commercial); `say(text, *anims)` / `steps(text, [anims])` spread animations across a line; emits `.srt` | The **`say`/`steps` DSL**: a scene declares which animations belong to which narration line and whether they fire at line start or spread across it — map directly onto your beat contract. Also its licence-matrix habit for voice models. |
| **HyperFrames `/faceless-explainer` + explainer type** | HTML/GSAP | Explainer dramaturgy: open on a person/situation + question, bring the device in as the answer, run **one concrete input** through every step, build diagrams incrementally, morph rather than cut, end on one line; avoid bullet slides, icons-in-circles, three-cards-in-a-row, whole-diagram-at-once, narrator reading on-screen text. |
| **html-video** (Open Design / nexu-io, Apache-2.0) | Agent writes a content graph (nodes/edges) + one HTML per frame; HyperFrames adapter; MiniMax music + TTS with ducking; 21 licence-tracked templates | **Content graph → scene order** (topological sort) and licence-tracked template manifests (YAML inputs + licence per template). |
| **Dashmotion** (MIT Claude skill) | Mermaid → single-file animated SVG | Mermaid as the *diagram source of truth*; animate edges with `stroke-dashoffset` and travelling dots. |
| **overcrank** (MIT) | Patches rAF/Date/timers/performance; virtual 16 ms steps; `beginFrame` on Linux; ffmpeg | The `beginFrame` capture path and self-reported capture costs; its "pure CSS is wrong under virtual time" warning. |

---

## 8. Recommendation

### 8.1 Primary renderer: your own Playwright pipeline (hardened)
Reasons: it already satisfies the two things that matter (pure `render(t)` and parallel capture); it has no licence surface (Remotion's free tier ends at 4 headcount; HyperFrames is Apache but its skills are tuned for 1920×1080 story films and its single-machine render is seek-serial); and 20–25 videos/month × ~1,650 frames is ~40k frames/month — trivially local. Harden it with: Linux `chrome-headless-shell` + `beginFrame` capture (measure vs your screenshot path), font/image preload gates, a `check`-style lint (missing durations, elements outside safe zone, contrast, forbidden APIs via static grep + runtime `Proxy` traps on `Date.now`/`Math.random`), and `snapshot --at` stills for the VLM review loop.

### 8.2 What to borrow from each
- **HyperFrames**: adopt its contract wording almost verbatim (clip visibility window, forbidden APIs, register-timeline-last, never tween visibility on a clip, `fitTextFontSize`-style auto-fit, hard-kill caption groups). Import its *references* (captions, sound, explainer type, motion) into your Claude Code skill as house rules; `npx hyperframes add` catalog blocks (caption styles, transitions, marker highlights) as editable source where their licence permits. Keep compositions HyperFrames-compatible (`data-composition-id`, `data-start`, `data-duration`, `window.__timelines`) so `npx hyperframes render`/`cloud render` remains an escape hatch.
- **Remotion**: `Caption` + `createTikTokStyleCaptions` data model (port the algorithm; MIT package is also usable standalone in Node), `visualizeAudio` for pre-baked band data, the Lambda chunking defaults as a template for your own multi-worker scheduler.
- **Motion Canvas / manimvox**: the "yield/say each beat" scene DSL.
- **TEA / Code2Video**: planner→coder→critic with VLM visual-fix and anchor-based layout checks; a TeachQuiz-style comprehension eval.

### 8.3 Proposed composition-contract extension: narration-synced scenes

```jsonc
// beats.json — produced by the narration step, consumed by render(t)
{
  "fps": 30, "width": 1080, "height": 1920,
  "voice": { "file": "vo.wav", "words": [ { "id": "w0", "text": "Every", "start": 0.12, "end": 0.31 } ] },
  "beats": [ { "id": "intro.question", "word": "w3", "t": 0.84 },
             { "id": "db.write", "word": "w17", "t": 4.92 } ],
  "captions": { "pages": [ { "startMs": 100, "durationMs": 860, "tokens": [ { "text": " Every", "fromMs": 120, "toMs": 310 } ] } ] },
  "audio_features": { "hop": 1, "bands": [[0.12,0.04,0.01]] },   // per frame, 0–1
  "music": { "file": "bed.wav", "beats": [0.50, 1.00, 1.50], "duck": 0.14 },
  "sfx": [ { "file": "click.wav", "at_beat": "db.write", "offset_frames": 1, "gain_db": 4 } ]
}
```

Composition side (keeps `render(t)` pure):
- `scene(id, {from: "beat:intro.question", to: "beat:db.write"})` resolves beat ids to seconds at load; nothing in HTML hard-codes seconds.
- Per element: `data-reveal="beat:db.write"` (+ optional `data-reveal-offset="0.1"`), `data-hold-until="beat:next"`; a tiny resolver sets `data-start`/`data-duration` so the file stays HyperFrames-valid.
- `data-caption-host` region with `data-track-kind="captions"`; caption renderer reads `captions.pages` and the active token at `t`.
- `data-react="band:0"` maps a band energy to a CSS variable (`--energy`) each frame; animations consume the variable.
- Lint rules: every beat referenced exists; no beat reveal lands within 2 frames of a page break (avoid visual pile-ups); every scene's spoken word count ≤ ~19; all caption text inside the 80% box; SFX peak = picture frame + 1.

Script authoring: Claude writes `script.md` with `[[beat:id]]` markers; the TTS step strips markers, synthesises, aligns (TTS-native or WhisperX), and emits `beats.json`. If timings are re-generated, compositions don't change.

### 8.4 Test plan: same 15 s scene, two stacks
Scene: "What is a write-ahead log?" — 3 beats (request arrives → append to WAL → ack), one Mermaid-derived diagram built incrementally, karaoke captions, one whoosh + one click SFX, music bed, Kokoro or ElevenLabs VO, 1080×1920 @ 30 fps (450 frames).

| Measure | How |
|---|---|
| Agent effort | Same prompt + `beats.json` given to Claude Code twice: (A) your skill/pipeline, (B) `/hyperframes` skills in a fresh `npx hyperframes init`. Count turns, tool calls, tokens, wall time to first clean render, number of lint/check failures fixed, manual interventions. |
| Render time | Cold and warm: your parallel capture (N workers), your capture with `beginFrame`, `npx hyperframes render --quality high`, optionally `cloud render`. Record frames/s and peak RAM. |
| Determinism | Render twice, hash frames (and the MP4); expect identical. |
| Output quality | Blind side-by-side on a phone: caption legibility in the safe zone, reveal timing vs spoken word (measure offset in ms for each beat from the waveform), SFX alignment (peak = frame+1), loudness (−14 LUFS ±1, TP ≤ −1 dBTP), file size, VMAF/SSIM vs a PNG master. |
| Maintainability | Diff size of the composition; how many seconds are hard-coded; how portable the HTML is to the other renderer without edits. |

Decision rule: switch primary renderer only if HyperFrames wins on agent effort by a clear margin *and* render time is within 2× of yours; otherwise keep yours and keep borrowing.

---

## Sources
- https://github.com/heygen-com/hyperframes
- https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/hyperframes/SKILL.md
- https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/media-use/SKILL.md
- https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/hyperframes-cli/SKILL.md
- https://raw.githubusercontent.com/heygen-com/hyperframes/main/skills/hyperframes/references/runtimes.md
- https://cdn.jsdelivr.net/gh/heygen-com/hyperframes@main/skills/hyperframes/references/captions.md
- https://cdn.jsdelivr.net/gh/heygen-com/hyperframes@main/skills/hyperframes/references/types/explainer.md
- https://cdn.jsdelivr.net/gh/heygen-com/hyperframes@main/skills/hyperframes/references/sound.md
- https://cdn.jsdelivr.net/gh/heygen-com/hyperframes@main/skills/media-use/references/audio.md
- https://www.heygen.com/research/html-to-video
- https://dev.to/andrew-ooo/hyperframes-review-heygens-html-to-video-for-ai-agents-170i
- https://besthub.dev/articles/hyperframes-vs-remotion-how-html-is-redefining-programmable-video-fb556d60f55d
- https://download.hermesedi.duckdns.org/.hermes/hermes-agent/optional-skills/creative/hyperframes/references/features.md
- https://skillselion.com/skills/heygen-com/hyperframes/faceless-explainer
- https://www.remotion.dev/docs/license/faq
- https://www.remotion.dev/docs/ai/skills
- https://www.remotion.dev/docs/captions/create-tiktok-style-captions
- https://www.remotion.dev/docs/captions/
- https://www.remotion.dev/docs/media-utils/
- https://www.remotion.dev/docs/visualize-audio
- https://www.remotion.dev/docs/lambda/
- https://www.remotion.dev/docs/lambda/concurrency
- https://www.remotion.dev/docs/performance
- https://www.remotion.dev/docs/web-renderer/
- https://www.remotion.dev/templates/tts
- https://www.pkgpulse.com/guides/remotion-vs-motion-canvas-vs-revideo-programmatic-video-2026
- https://motioncanvas.io/blog/version-3.2.0
- https://motioncanvas.io/docs/rendering/
- https://github.com/motion-canvas/motion-canvas
- https://repos.ecosyste.ms/hosts/GitHub/repositories/motion-canvas%2Fmotion-canvas
- https://github.com/upspawn/overcrank
- https://fooqux.com/article/3163
- https://dev.to/mutsuntsai/replacing-playwrights-hardcoded-vp8-encoder-a-deep-dive-into-pagescreencast-43ee
- https://playwright.dev/docs/clock
- https://developer.mozilla.org/en-US/docs/Web/CSS/animation-delay
- https://developer.mozilla.org/en-US/docs/Web/API/Animation/currentTime
- https://webflow.com/blog/gsap-becomes-free
- https://gsap.com/pricing/
- https://animejs.com/documentation/timeline/timeline-methods/seek
- https://github.com/theatre-js/theatre
- https://github.com/rough-stuff/rough-notation
- https://cdn.jsdelivr.net/npm/excalidraw-animate@0.7.2/README.md
- https://cdn.jsdelivr.net/gh/csthink/dashmotion@main/README.md
- https://www.forasoft.com/learn/ai-for-video-engineering/articles-ai/whisperx-diarization-word-level-timestamps
- https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps
- https://github.com/tiger-ai-lab/theoremexplainagent
- https://opencv.org/code2video/
- https://pypi.org/project/manimvox/0.1.0/
- https://github.com/iblueer/html-video
