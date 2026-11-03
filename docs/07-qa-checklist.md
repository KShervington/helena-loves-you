# 07 — QA checklist

Run by `/helena-qa` on every produced video; results go to `Docs/qa.md` as pass/fail per line with a note. A video can't move to `ready_for_review` with any **blocking** fail.

## A. Accuracy (blocking)

- [ ] Every factual claim in narration and on screen appears in the script's source-check table with a source location.
- [ ] Numbers on screen match the source at render time (star counts, parameter counts, dates). Hot-lane numbers carry the "as of <date>" form if they'll move.
- [ ] The analogy's break-point is stated, or the analogy doesn't overclaim.
- [ ] Author/org credited on screen and in the caption pack.
- [ ] No claim that the source itself marks as preliminary/unverified is stated as fact.
- [ ] **Tone guardrail (01):** no line encourages the viewer to sacrifice, endure, deprive or change themselves; Helena's perfectionism is aimed at systems only.
- [ ] The account name / "Helena loves you" does not appear in narration or on screen. No image of Helena.

## B. Structure (blocking)

- [ ] Hook is on screen and spoken within the first 1.0 s; complete thought ≤ 12 words.
- [ ] The gap is opened by 3 s and re-opened between 30–45 s.
- [ ] One idea per scene; no scene with > 6 simultaneous elements.
- [ ] CTA present in the last 8 s; the comment prompt is specific ("what should we explain next?").
- [ ] Duration 45–60 s (hot lane may run 40–60).

## C. Readability (blocking)

- [ ] All must-read text inside the safe area (x 60–1020, y 220–1500).
- [ ] Each caption line visible ≥ 0.3 s × word count, counted from fully on screen.
- [ ] Caption contrast ≥ 4.5:1 against whatever is behind it at every frame it's shown (check the three busiest frames).
- [ ] No text under 32 px tall at 1080 wide.
- [ ] Caption words highlight in sync with narration (spot-check 3 points: start, middle, end; drift ≤ 100 ms).

## D. Visual system (non-blocking unless flagrant)

- [ ] Red appears as one idea per frame (the visualizer's centre plus at most one highlighted element/word); no red fills, gradients or glows.
- [ ] Motion is Helena's: no overshoot/bounce/spring, no wipes or zoom-throughs, no beat-synced motion; the visualizer is idle in silence and moves only with her voice (`levels.json` present and not stubbed).
- [ ] Composition is centred; frame chrome (meta line, rules, index) present.
- [ ] Fonts are the design-system fonts; no fallback font rendered (check stills from frame 0).
- [ ] Reveals are tied to narration words (not arbitrary timers).
- [ ] Transitions: no muddy crossfade between two busy layouts; no caption leaving and arriving at the same moment.
- [ ] Poster frame is settled (nothing mid-transition), shows the hook, works as a thumbnail at 200 px wide.

## E. Audio (blocking)

- [ ] Integrated loudness −14 LUFS ± 1; true peak ≤ −1 dBTP.
- [ ] Narration clearly above music (bed ducked ≥ 12 dB; no drums or drops in the bed).
- [ ] No clipped or mispronounced words (listen to the full track once; fix pronunciations in the TTS lexicon).
- [ ] SFX only on reveals/transitions, never on every beat; sits under the music.
- [ ] Music licence recorded in the video README; track not used in the previous two videos (creative asset rule).

## F. Files (blocking)

- [ ] `Exports/<slug>_1080x1920.mp4`: H.264 High, yuv420p, 30 fps, ≤ 60 s, AAC 48 kHz; frame 0 = poster.
- [ ] `Exports/<slug>_poster.jpg` present.
- [ ] `Raw_Footage/<slug>_textless_1080x1920.mp4` present and same duration.
- [ ] `Docs/caption-pack.md` front matter valid; `Docs/library-candidates.md` present (can be empty).
- [ ] `Project_Files/render.sh` rebuilds Exports from the final folder location.

## G. Automated checks (run by the skill)

```bash
# duration, codec, loudness
ffprobe -v error -show_entries format=duration:stream=codec_name,width,height,r_frame_rate -of default=nw=1 Exports/*.mp4
ffmpeg -i Exports/*.mp4 -af loudnorm=print_format=json -f null - 2>&1 | tail -12
# stills at the three busiest moments + every scene boundary, for the human-style watch
node <library>/assets/tools/render-pipeline/capture.mjs Project_Files/comp.html stills /tmp/qa-stills <t1> <t2> <t3>
```

## H. The human-style watch (agent, then Kyle)

Watch once at 1× on a phone-sized viewport, muted, captions only: does it still make sense? Then once with sound. Write down the single weakest second; if it's in the first 5 s, it's a `changes_requested`.
