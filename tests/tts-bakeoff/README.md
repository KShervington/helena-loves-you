# TTS bake-off

Renders the same ~55-second script — in Helena's register — with each candidate voice, collects word timestamps, and scores precision, flatness, consistency and timing. This picks **Helena's one voice for the life of the account** (D-02), so weight consistency above everything.

Runs on **Windows, macOS or Linux**. Needs Python 3.10+, Node 18+, and `ffmpeg` on PATH. An NVIDIA GPU (CUDA) makes Chatterbox/Qwen3-TTS/alignment much faster; Apple Silicon uses MPS/MLX; CPU works for everything but is slow for Chatterbox. On Windows, either run natively (commands below) or in **WSL2 Ubuntu** — WSL2 is the cleanest option because the rest of the production pipeline (`audio.sh`, `encode.sh`) is bash, and CUDA passes through to WSL2. Runs on Kyle's Mac (models need Hugging Face / provider access; this container can't reach them). Evidence for the candidate list: `docs/research/audio-tts-music-sfx.md`.

| # | Candidate | Licence | Timestamps | Runner |
|---|---|---|---|---|
| 0 | **Designed voice** — ElevenLabs Voice Design (prompt: "calm, precise, emotionless female narrator, late twenties, close-mic, no vocal fry, no smile") or Qwen3-TTS VoiceDesign | paid = commercial / Apache | native / aligned | `elevenlabs.mjs` with the designed voice id / `qwen3tts.py` |
| 1 | ElevenLabs Eleven v4 + Multilingual v2 (Creator plan), stock narrators | paid = commercial | native (char → word) | `elevenlabs.mjs` |
| 2 | Chatterbox Turbo (local, MIT) | MIT | via forced alignment | `chatterbox.py` + `align.py` |
| 3 | Kokoro-82M (local, Apache-2.0) | Apache | native | `kokoro.py` |
| 4 | Qwen3-TTS 1.7B VoiceDesign (optional) | Apache | via forced alignment | `qwen3tts.py` (not written — add if the Mac setup is < 1 h) |

## Run

macOS / Linux / WSL2:

```bash
cd tests/tts-bakeoff
python3 -m venv .venv && source .venv/bin/activate
pip install kokoro soundfile chatterbox-tts ctc-forced-aligner faster-whisper jiwer   # Mac: see each runner's header for MLX variants
export ELEVENLABS_API_KEY=…
```

Windows (PowerShell, native):

```powershell
cd tests\tts-bakeoff
py -m venv .venv; .\.venv\Scripts\Activate.ps1
pip install torch --index-url https://download.pytorch.org/whl/cu124    # NVIDIA GPU; skip for CPU-only
pip install kokoro soundfile chatterbox-tts ctc-forced-aligner faster-whisper jiwer
winget install ffmpeg; winget install eSpeak-NG.eSpeak-NG                # Kokoro needs espeak-ng for out-of-dictionary words
$env:ELEVENLABS_API_KEY = "…"
# then the same commands as below with `python` instead of `python3`
```

node elevenlabs.mjs script.txt out/eleven-v4-flatcalm-1 --model eleven_v4 --voice <voice_id>                 # tags default to [flat][calm]
node elevenlabs.mjs script.txt out/eleven-v4-notags-1   --model eleven_v4 --voice <voice_id> --tags ""
node elevenlabs.mjs script.txt out/eleven-mlv2-1        --model eleven_multilingual_v2 --voice <voice_id>   # no tags on v2
python3 kokoro.py script.txt out/kokoro-af_heart --voice af_heart
python3 kokoro.py script.txt out/kokoro-am_adam  --voice am_adam
python3 chatterbox.py script.txt out/chatterbox-e035-1 [--ref reference.wav]        # exaggeration 0.35 default; try --exaggeration 0.3
python3 align.py out/chatterbox/narration.wav script.txt out/chatterbox/narration.json   # forced alignment for engines without timestamps

python3 score.py out/*            # WER (faster-whisper), duration variance across 3 renders, timestamp sanity (globs expand on any shell)
```

Each runner writes `narration.wav` + `narration.json` (`{ duration, words: [{ w, s, e }], beats: [{ id, s }], provider, model, voice, rendered_at }`) — the exact format the compositions consume — so the winner's output drops straight into `/helena-produce`. Run each candidate three times (`-1`, `-2`, `-3`) for the consistency score.

## Flatness — how each engine is steered

`script.txt` is kept clean; each runner applies Helena's delivery its own way and records it under `delivery` in `narration.json`, so the winning settings can be frozen in `VOICE.md`.

| Engine | Lever | Default in the runner | What to vary |
|---|---|---|---|
| ElevenLabs v3 / v4 | inline audio tags prepended to every beat (`--tags`), plus `stability` (higher = less expressive), `style 0`, `speed 0.95` | `[flat][calm]`, stability 0.8 | render `--tags ""` vs `[flat][calm]` vs `[flat][calm][quiet]`; stability 0.8 vs 1.0. Tags are the first thing to check for *consistency across takes* |
| ElevenLabs Multilingual v2 | no tags (ignored/misread, never sent); `stability` 0.8–1.0, `style 0` | stability 0.8 | stability only |
| Voice Design (v4) | the design prompt itself: "calm, precise, emotionless female narrator, late twenties, close-mic, even pace, no vocal fry, no smile" | — | two prompt variants, then the tags above |
| Chatterbox Turbo | `--exaggeration` (0.3–0.4 flat) and `--cfg`; a flat 10–15 s reference clip | 0.35 / 0.5 | 0.3 vs 0.4; with vs without a reference |
| Kokoro | voice choice and `--speed` ≤ 1.0 only | af_heart, 0.95 | af_heart / af_bella / bf_emma |

Name output folders by setting so `score.py` can group them: `out/eleven-v4-flatcalm-1`, `out/eleven-v4-notags-1`, `out/chatterbox-e030-1`, …

## Judge (blind, 1–5 each)

Precision on acronyms/numbers/names · **flatness** (even pitch, no performed emotion, no smile, yet not robotic) · warmth-in-words-only (does "I will explain it" land as unsettling rather than friendly) · artefacts (breaths, clicks, sped-up endings, hallucinated words — count) · **consistency across three renders** (the one-way door) · timestamp error (median |Δ| vs 20 hand-tapped words; < 60 ms passes) · render time · cost per 55 s × 25.

**Decision rule:** highest precision × flatness with consistency ≥ 4 and a commercial-OK licence; a designed voice wins ties because nobody else has it. Freeze the winner's voice id / prompt and settings in `helena-media-library/assets/tools/narration/VOICE.md`. Record the result in `docs/10-decision-log.md`.
