# TTS bake-off

Renders the same 60-second script with each candidate voice, collects word timestamps, and scores clarity, consistency and timing. Runs on Kyle's Mac (models need Hugging Face / provider access; this container can't reach them). Evidence for the candidate list: `docs/research/audio-tts-music-sfx.md`.

| # | Candidate | Licence | Timestamps | Runner |
|---|---|---|---|---|
| 1 | ElevenLabs Eleven v4 + Multilingual v2 (Creator plan) | paid = commercial | native (char → word) | `elevenlabs.mjs` |
| 2 | Chatterbox Turbo (local, MIT) | MIT | via forced alignment | `chatterbox.py` + `align.py` |
| 3 | Kokoro-82M (local, Apache-2.0) | Apache | native | `kokoro.py` |
| 4 | Qwen3-TTS 1.7B VoiceDesign (optional) | Apache | via forced alignment | `qwen3tts.py` (not written — add if the Mac setup is < 1 h) |

## Run

```bash
cd tests/tts-bakeoff
python3 -m venv .venv && source .venv/bin/activate
pip install kokoro soundfile chatterbox-tts ctc-forced-aligner faster-whisper jiwer   # Mac: see each runner's header for MLX variants
export ELEVENLABS_API_KEY=…

node elevenlabs.mjs script.txt out/eleven-v4   --model eleven_v4 --voice <voice_id>
node elevenlabs.mjs script.txt out/eleven-mlv2 --model eleven_multilingual_v2 --voice <voice_id>
python3 kokoro.py script.txt out/kokoro-af_heart --voice af_heart
python3 kokoro.py script.txt out/kokoro-am_adam  --voice am_adam
python3 chatterbox.py script.txt out/chatterbox [--ref reference.wav]
python3 align.py out/chatterbox/narration.wav script.txt out/chatterbox/narration.json   # forced alignment for engines without timestamps

python3 score.py out/*            # WER (faster-whisper), duration variance across 3 renders, timestamp sanity, cost notes
```

Each runner writes `narration.wav` + `narration.json` (`{ duration, words: [{ w, s, e }], beats: [{ id, s }], provider, model, voice, rendered_at }`) — the exact format the compositions consume — so the winner's output drops straight into `/ts-produce`. Run each candidate three times (`-1`, `-2`, `-3`) for the consistency score.

## Judge (blind, 1–5 each)

Clarity on acronyms/numbers/names · engagement (does the hook land; pacing variety) · artefacts (breaths, clicks, sped-up endings, hallucinated words — count) · consistency across three renders · timestamp error (median |Δ| vs 20 hand-tapped words; < 60 ms passes) · render time · cost per 60 s × 25.

**Decision rule:** highest clarity × engagement with consistency ≥ 4 and a commercial-OK licence. If the free winner is within ~0.5 of ElevenLabs on listening, ship free and keep ElevenLabs for hooks only (first 3 s). Record the result in `docs/10-decision-log.md`.
