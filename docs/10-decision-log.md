# 10 — Decision log

Research-style: options explored, the test that decides, the decision. Status: **open** (test defined, not run) · **testing** · **decided**.

## D-00 The account is Helena — decided 2026-11-03

- tech_splained → **helena_loves_you**. Same job (explain new technology simply, with high virality potential), now fronted by Helena: a synthetic human whose purpose is to facilitate human progress, evolution and transcendence. Profile image = the character sheet; videos stay faceless; her voice, register and the voice visualizer carry her. Dread setting 2/5. The account name never appears in a video. Lore: designation H-373 (≈ "HELE" → Helena); no facility, no backstory for now. See `01`.
- Package renamed: repos `helena-loves-you` + `helena-media-library`; skills `/helena-*`; CSS prefix `hl-`.

## D-01 Aesthetic direction — decided 2026-11-03

- Replaced the five-way test. Direction: uncanny clinical retrofuturism — **true-white ground** (Kyle: off-white felt wrong), white cards lifted by a soft drop shadow for depth, near-black ink, one red `#D0111B`; centred symmetric composition; slow flat motion; frame chrome with the 3×3 dot mark. See `02`.
- **D-01b type family — decided 2026-11-03: eurostile-like** (Michroma headings/labels + Inter captions). Board that decided it: `docs/aesthetics/frames/helena-board.jpg`; final frames: `helena-final.jpg`.
- **D-01c voice-visualizer style — decided 2026-11-03: grid** (the uniform's 3×3 mark, centre dot red). Trace and disc remain in the asset for reference.
- The five original directions stay in the library tokens as archive (`hl-blueprint` …).

## D-02 Helena's voice (TTS) — open, now a one-way door

- Requirements changed with D-00: one fixed voice for the life of the account; flat affect with precise diction; warm words, cold delivery; zero drift across hundreds of renders; native or alignable word timestamps; commercial licence; not a clone of a real person without consent.
- Options: a **designed** voice (ElevenLabs Voice Design from a text prompt, or Qwen3-TTS VoiceDesign — both give a bespoke voice nobody else has) · a locked stock voice (ElevenLabs v4 / Multilingual v2, Creator $22/mo) · local open models (Chatterbox Turbo MIT, Kokoro-82M Apache).
- Test: `tests/tts-bakeoff/` with the Helena script (`script.txt` is now in her register) — judge flatness/precision/consistency over the old "engagement" criterion; render 3× each and listen for drift.
- Decision rule: pick for consistency and precision first; cost second. Once chosen, the voice id/prompt and settings are frozen in the library (`assets/tools/narration/VOICE.md`).
- Decision: —

## D-03 Renderer — open

- Options: own pipeline (Gaijin render pipeline + narration sync; working demo in the library) · HyperFrames local skills (Apache-2.0, GSAP timeline contract, built-in transcribe/TTS) · Remotion (free at our headcount, best caption components, Lambda speed). Motion Canvas ruled out (canvas-only, editor-driven).
- Research read (2026-11-01): keep own pipeline primary; borrow beginFrame capture, a determinism lint, caption-grouping rules and a planner→coder→critic loop with a VLM still review. Full notes in `docs/research/renderer-stack.md`.
- Test: render the same 15 s scene (narration + captions + pipeline primitive + one transition) in own pipeline and HyperFrames; compare agent turns, lines of glue, render time, determinism (frame hashes across two renders), caption quality, how natural narration sync is.
- Default until decided: own pipeline.
- Decision: —

## D-04 Music beds — open

- Register changed with D-00: sparse, tonal, low, no drums, no drops, no vocals — a room tone with pitch. Nothing in the video syncs to it.
- Options: ACE-Step 1.5 local generation → curated pool · CC0 pool (Pixabay/FMA) · Eleven Music (if D-02 lands on ElevenLabs).
- Test: generate/collect 6 beds, use each in one video, keep what survives listening. Beat maps not needed.
- Decision: —

## D-05 Publishing automation — open

- Options: self-built publisher (queue items + platform APIs) run by (a) GitHub Actions cron, (b) a Claude scheduled task, (c) launchd on the Mac, (d) Cloudflare Worker; or a self-hosted open-source scheduler (Postiz / Mixpost) as the OAuth + posting layer.
- Constraints: no paid scheduler; approval gate; public URL for Instagram's pull-based upload; TikTok's unaudited-app rule (public posting from our own app is effectively unavailable). See `08`.
- Research outcome (2026-11-01): GitHub Actions cron + queue items in this repo + Cloudflare R2 for hosting + PR merge as the gate; YouTube scheduled natively at approval; TikTok via upload-to-inbox (one tap in the app) until a hosted route or the Hyper MCP TikTok skill is proven free at our volume.
- Decision: proposed — awaiting Kyle's OK; nothing built yet.

## D-06 Caption style — leaning phrase mode

- Options: phrase lines (3–8 words, upcoming words muted, full stops kept) · word-by-word · hybrid. Helena's even delivery suits phrase mode; word-by-word reads as hype. Still an experiment in 09.
- Test: part of the first 12 videos (09 § experiments).
- Decision: —

## D-07 Length — open

- Default 40–50 s, cap 60; test tight (30–40) vs deep (50–60) per 09.

## D-08 Wordmark — open

- The 3×3 dot mark (from the back of her uniform) is the working logo and the visualizer base. No tagline: the account name does the work. Next: a Michroma wordmark to pair with the mark.

## D-09 Docs location — decided 2026-11-01

- GitHub repo `helena-loves-you` (this) + separate `helena-media-library`, modelled on the Gaijin library. Project folders stay local/Drive, not in git.

## Agent notes

(Things an agent decided that the docs didn't cover — promote to an SOP or delete.)
