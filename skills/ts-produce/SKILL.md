---
name: ts-produce
description: Produce a tech_splained video from a scripted project folder — TTS + word alignment, a narration-synced HTML composition built from media-library primitives in the chosen design direction, stills check, music/SFX mix at −14 LUFS, render with poster-as-frame-0, textless master, assets export, and library candidates. Use for "/ts-produce <folder>", "render this one", or the batch render week.
---

# /ts-produce <project folder>

Input: a project folder at `storyboarded`. Output: `Exports/`, `Raw_Footage/`, `Assets/`, `Project_Files/` filled per `templates/video-README.md`; `Docs/library-candidates.md`; status → `produced`.

Read first: `docs/02-visual-design-system.md`, `docs/05-visual-storytelling.md`, `docs/06-production-pipeline.md`, the media library's `INDEX.md` (then only the `ASSET.md` of assets you'll use), and `docs/10-decision-log.md` for the current design direction and TTS choice.

## Steps

1. **Library.** Get an up-to-date local copy of `tech-splained-media-library` (clone or pull). Read `INDEX.md`. Pick primitives/motion/captions/audio that fit the shot list; note reused ids + library commit in `Docs/plan.md`. Creative assets: respect `used_in` (not in the last two videos).
2. **Voice.** Run the TTS step on `Project_Files/script.txt` with `lexicon.json` (provider per decision log) → `Project_Files/narration.wav` + word-level `narration.json` (+ `.js` twin). If the provider gives no timestamps, run the alignment step. Listen once: mispronunciations → fix the lexicon and re-run. Delete the stub timings.
3. **Compose.** Start from `examples/explainer-demo/demo.html`. Set the direction class. Build each shot-list beat with the named primitive; every reveal time is `N.at(...)`; captions via `GML.captions`; one accent; safe area respected. Poster = the chosen settled frame.
4. **Stills check.** `capture.mjs … stills` at every scene boundary and mid-transition plus the three busiest moments. Look at them. Fix overflow, collisions, fallback fonts, low contrast, muddy crossfades, captions overlapping diagrams.
5. **Music + SFX.** Pick a bed (library or approved source; record licence). Use `audio.sh` to trim/fade and mix narration over music with ≥ 10 dB ducking, SFX from `sfx-kit` on reveals/transitions only, −14 LUFS. No whole-frame beat pulsing.
6. **Render.** `capture.mjs frames` (and `--query textless=1` for the master) → `encode.sh` with `--poster <frame>`. Name per the template. Export Assets graphics (`element` mode) and check transparent PNGs on a checkerboard.
7. **Self-QA.** Run `/ts-qa` on the folder. Fix anything blocking before reporting.
8. **Library candidates.** List new reusable pieces (primitives, motion, a caption style, a music bed + beat map) in `Docs/library-candidates.md`, numbered, with thumbnails and a contact sheet. Do **not** add anything to the library; Kyle picks.
9. **Queue.** Append the video to `pipeline/queue/items/*.json` with `status: produced` (→ `ready_for_review` once QA passes) and the caption-pack front matter.
10. Report in a few lines: what was reused vs new, duration, direction, voice, music window, QA result, the candidates list, and one thing you'd re-roll if asked.

## Rules

- Never hand-type a reveal time. If a word isn't in the narration, change the lookup or the script — don't guess.
- One full render per video unless QA fails; before it, stills.
- Nothing from outside the library or the approved audio sources goes in the mix.
- Project folders are self-contained: copy used library files into `Assets/`, reference them relatively, and confirm `render.sh` works from the final location.
