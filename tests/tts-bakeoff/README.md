# TTS bake-off

Renders the same ~55-second script — in Helena's register — with each candidate voice, collects word timestamps, and scores precision, flatness, consistency and timing. This picks **Helena's one voice for the life of the account** (D-02), so weight consistency above everything. Runs on Kyle's Mac (models need Hugging Face / provider access; this container can't reach them). Evidence for the candidate list: `docs/research/audio-tts-music-sfx.md`.

| # | Candidate | Licence | Timestamps | Runner |
|---|---|---|---|---|
| 0 | **Designed voice** — ElevenLabs Voice Design (prompt: "calm, precise, emotionless female narrator, late twenties, close-mic, no vocal fry, no smile") or Qwen3-TTS VoiceDesign | paid = commercial / Apache | native / aligned | `elevenlabs.mjs` with the designed voice id / `qwen3tts.py` |
| 1 | ElevenLabs Eleven v4 + Multilingual v2 (Creator plan), stock narrators | paid = commercial | native (char → word) | `elevenlabs.mjs` |
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

Each runner writes `narration.wav` + `narration.json` (`{ duration, words: [{ w, s, e }], beats: [{ id, s }], provider, model, voice, rendered_at }`) — the exact format the compositions consume — so the winner's output drops straight into `/helena-produce`. Run each candidate three times (`-1`, `-2`, `-3`) for the consistency score.

## Judge (blind, 1–5 each)

Precision on acronyms/numbers/names · **flatness** (even pitch, no performed emotion, no smile, yet not robotic) · warmth-in-words-only (does "I will explain it" land as unsettling rather than friendly) · artefacts (breaths, clicks, sped-up endings, hallucinated words — count) · **consistency across three renders** (the one-way door) · timestamp error (median |Δ| vs 20 hand-tapped words; < 60 ms passes) · render time · cost per 55 s × 25.

**Decision rule:** highest precision × flatness with consistency ≥ 4 and a commercial-OK licence; a designed voice wins ties because nobody else has it. Freeze the winner's voice id / prompt and settings in `helena-media-library/assets/tools/narration/VOICE.md`. Record the result in `docs/10-decision-log.md`.
