# 10 — Decision log

Research-style: options explored, the test that decides, the decision. Status: **open** (test defined, not run) · **testing** · **decided**.

## D-01 Aesthetic direction — testing

- Options: A blueprint · B instrument · C midnight · D clinical · E signal (+ the A/C/E hybrid). Frames in `docs/aesthetics/frames/`, tokens in the library.
- Test: `02 § The test that picks a direction` — Kyle cuts to 3 from the contact sheet → same 15 s scene rendered in each → 2 posted videos per finalist → 3-s hold, completion, sends.
- Current read (2026-11-01, frames only): B reads most "lab", A and D stand out most in a dark feed, E is cheapest and most distinctive but mono captions are wide, C is closest to the 3B1B reference. The research's suggested hybrid (A's paper + C's colour semantics + E's mono labels) is worth a sixth frame if Kyle is torn.
- Decision: —

## D-02 Voice (TTS) — open

- Options: ElevenLabs v4 / Multilingual v2 (Creator, $22/mo, ~$3–6 of credits for 25 videos) · Chatterbox Turbo (MIT, local) · Kokoro-82M (Apache, CPU, native timestamps) · Qwen3-TTS 1.7B (Apache).
- Test: `tests/tts-bakeoff/` (same script, 3 renders each, blind listen + WER + timestamp error + cost).
- Decision rule: best clarity × engagement with consistency ≥ 4 and commercial licence; if a free model is within ~0.5 of ElevenLabs, ship free and keep ElevenLabs for hooks.
- Decision: —

## D-03 Renderer — open

- Options: own pipeline (Gaijin render pipeline + narration sync; working demo in the library) · HyperFrames local skills (Apache-2.0, GSAP timeline contract, built-in transcribe/TTS) · Remotion (free at our headcount, best caption components, Lambda speed). Motion Canvas ruled out (canvas-only, editor-driven).
- Research read (2026-11-01): keep own pipeline primary; borrow beginFrame capture, a determinism lint, caption-grouping rules and a planner→coder→critic loop with a VLM still review. Full notes in `docs/research/renderer-stack.md`.
- Test: render the same 15 s scene (narration + captions + pipeline primitive + one transition) in own pipeline and HyperFrames; compare agent turns, lines of glue, render time, determinism (frame hashes across two renders), caption quality, how natural narration sync is.
- Default until decided: own pipeline.
- Decision: —

## D-04 Music beds — open

- Options: ACE-Step 1.5 local generation → curated pool · CC0 pool (Pixabay/FMA) · Eleven Music (if D-02 lands on ElevenLabs).
- Test: generate/collect 6 beds in the "quiet lab" register (minimal, 90–110 BPM, no vocals), beat-map them, use each in one video, keep what survives listening.
- Decision: —

## D-05 Publishing automation — open

- Options: self-built publisher (queue items + platform APIs) run by (a) GitHub Actions cron, (b) a Claude scheduled task, (c) launchd on the Mac, (d) Cloudflare Worker; or a self-hosted open-source scheduler (Postiz / Mixpost) as the OAuth + posting layer.
- Constraints: no paid scheduler; approval gate; public URL for Instagram's pull-based upload; TikTok's unaudited-app rule (public posting from our own app is effectively unavailable). See `08`.
- Research outcome (2026-11-01): GitHub Actions cron + queue items in this repo + Cloudflare R2 for hosting + PR merge as the gate; YouTube scheduled natively at approval; TikTok via upload-to-inbox (one tap in the app) until a hosted route or the Hyper MCP TikTok skill is proven free at our volume.
- Decision: proposed — awaiting Kyle's OK; nothing built yet.

## D-06 Caption style — open

- Options: phrase lines (3–8 words, upcoming words muted) · word-by-word (1–3 words, large) · hybrid (word mode in the hook, phrase mode in the body).
- Test: part of the first 12 videos (09 § experiments).
- Decision: —

## D-07 Length — open

- Default 40–50 s, cap 60; test tight (30–40) vs deep (50–60) per 09.

## D-08 Tagline / wordmark — open

- Options: "new tech, actually explained" · "how the new thing works". Wordmark not designed; depends on D-01.

## D-09 Docs location — decided 2026-11-01

- GitHub repo `tech-splained` (this) + separate `tech-splained-media-library`, modelled on the Gaijin library. Project folders stay local/Drive, not in git.

## Agent notes

(Things an agent decided that the docs didn't cover — promote to an SOP or delete.)
