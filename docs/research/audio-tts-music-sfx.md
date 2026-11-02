# Audio tooling for the tech_splained pipeline: TTS, music, SFX

Research date: 2026-11-01. Scope: faceless 45–60 s tech explainers, ~20–25/month, AI voiceover + music bed + SFX, produced on a Mac (Apple Silicon) and/or a Linux cloud container, driven by an AI coding agent. Owner prefers free/open-source but will pay for ElevenLabs if the value is clear.

Working numbers used throughout: a 60 s narration at ~150 wpm is ~150 words ≈ 900–1,000 characters. 25 videos/month ≈ 25k chars/month of final TTS, realistically 50–75k/month once you count retakes and A/B voice tests. That is a tiny workload; price is almost never the deciding factor below the Pro tier of any vendor.

---

## A. Text-to-speech

### 1. ElevenLabs (state of play, Nov 2026)

**Plans (monthly billing, per elevenlabs.io/pricing and /pricing/api).** Credits ≈ characters for the premium models.

| Plan | $/mo | Credits | ≈ TTS minutes | v4/v3/Multilingual v2 chars | Flash/Turbo/v4-Turbo chars | Commercial licence |
|---|---|---|---|---|---|---|
| Free | 0 | 10k | ~10 | 10k | 20k | **No** (attribution required) |
| Starter | 6 (promo $1 first month) | 30k | ~30 | 75k* | 150k | Yes |
| Creator | 22 (50% off first month) | 121k | ~121 | 275k* | 550k | Yes; 192 kbps MP3 |
| Pro | 99 | 600k | ~600 | 1.24M* | 2.48M | Yes; 44.1 kHz PCM/WAV via API |
| Scale | 299 | 1.8M | ~1,800 | 3.7M* | 7.5M | Yes |
| Business | 990 | 6M | ~6,000 | 12.4M* | 24.8M | Yes |

\*The /pricing/api page quotes larger "characters included" figures than the credit counts on the main page; the main page's credit numbers are the conservative ones. Either way Starter/Creator cover this workload many times over.

**API rates:** $0.08 per 1k chars for v4, v3 and Multilingual v2; $0.04 per 1k chars for v4 Turbo, v3 Conversational, Flash v2.5 / Turbo v2.5. Overage per extra minute: roughly $0.20 (Starter) → $0.17 (Pro+).

**Commercial-use terms (help-center "Can I publish the content I generate").** Free plan: no commercial licence, and published output must credit "elevenlabs.io" or "11.ai" in the title. Any paid plan: commercial licence for content generated during the subscription, usable indefinitely, except content from Beta services (no commercial or production use). Content generated before/after a paid period cannot be used commercially. Implication: do the free-tier voice shootout, but render anything you post while on Starter or above.

**Models (docs "Text to speech" overview, Nov 2026).**

| Model | Char limit | Languages | Positioning |
|---|---|---|---|
| Eleven v4 (released 2026-10-07) | 10,000 | 90+ | Most emotive; inline audio tags; multi-speaker |
| Eleven v4 Turbo | — | 90+ | Same family, ~100 ms latency, half price |
| Eleven v3 | 5,000 | 70+ | Dramatic delivery, audio tags |
| Eleven v3 Conversational | — | 70+ | Realtime variant |
| Multilingual v2 | 10,000 | 29 | "Most stable on long-form generations"; ElevenLabs' own recommendation for voice-over/audiobook narration |
| Flash v2.5 | 40,000 | 32 | Fast, 50% cheaper per character |

For a 60 s explainer the "long-form stability" argument for Multilingual v2 barely applies; v4 (or v4 Turbo) is the quality leader on the Artificial Analysis Speech Arena (v4 Turbo Elo 1336, v4 1334, v3 1188, Multilingual v2 1093). Practical recommendation: default to **Eleven v4** with stability ~0.5–0.7 and sparse audio tags; fall back to **Multilingual v2** if v4 wanders on technical vocabulary, acronyms or numbers.

**Timestamps / alignment.**
- `POST /v1/text-to-speech/{voice_id}/with-timestamps` returns `alignment` and `normalized_alignment`, each with parallel arrays of characters and start/end seconds. It is **character-level**; you build words by splitting on spaces (use `normalized_alignment` so "GPT-5" or "2026" line up with what was spoken). Default model is Multilingual v2; the docs do not list a per-model support table, so test v4 explicitly.
- Third-party hosts (fal.ai `elevenlabs/tts/eleven-v3`, Segmind "TTS ElevenLabs with timestamps") expose a `timestamps: true` flag returning per-word arrays, which confirms v3 supports alignment via the API.
- `POST /v1/forced-alignment` takes any audio + transcript and returns `words[]` and `characters[]` with start/end plus a `loss` confidence. Useful if you post-edit audio or use a non-ElevenLabs voice but want ElevenLabs-grade alignment.

**Cost for 25 × 60 s/month.** ~25k chars final + ~50% retakes ≈ 40–75k chars. On v4 at $0.08/1k that is $3–6 of credits; Starter ($6) is borderline, **Creator ($22/mo)** is comfortable and unlocks 192 kbps MP3. Pro ($99) is only worth it if you need 44.1 kHz WAV via API; for social video, 192 kbps MP3 or the 128 kbps default is fine.

### 2. Open-source / open-weight TTS (Nov 2026 status)

Licence, hardware and timestamp facts below come from each project's README/model card unless noted; quality notes combine the Artificial Analysis Speech Arena, the OpenVox and LocalAIMaster 2026 roundups, and a Mac M4 hands-on comparison.

| Model | Licence (weights) | Commercial? | Size | Apple Silicon | CPU-only | Word timestamps | Arena Elo | Narration verdict |
|---|---|---|---|---|---|---|---|---|
| **Kokoro-82M v1.0** | Apache 2.0 | Yes | 82M | Yes (MPS via `PYTORCH_ENABLE_MPS_FALLBACK=1`; CoreML/MLX ports exist) | Yes, fast | **Yes**: Kokoro-FastAPI `/dev/captioned_speech` returns word timestamps; the `kokoro` KPipeline exposes token timings for English | 1062 | Clean, dependable, slightly flat; the best "it just works" local option; no cloning; ~54 voices |
| **Chatterbox (Resemble)** — Turbo 350M / Nano 110M / Multilingual V3 500M | MIT | Yes (output carries an imperceptible Perth watermark) | 110–500M | Yes (`mps`; `chatterbox-mlx` gives ~0.7 RTF on M4) | Nano yes (~3× realtime on 8 cores) | No native; use forced alignment | Chatterbox 1024 / "Chatterbox HD" 1110 | Most natural-sounding open English voice; paralinguistic tags; needs chunking + retries for stability on long text |
| **Qwen3-TTS** (0.6B / 1.7B; CustomVoice, VoiceDesign, Base) | Apache 2.0 | Yes | 0.6–1.7B | Yes via MLX 8-bit community port (~0.65 RTF on M4); official code is CUDA-first | Slow | No | 929–941 (open models; hosted Qwen-Audio-3.1-TTS-Plus is 1305) | Voice design from text prompt is unique; quality tracks the reference clip; strong pick when you want a bespoke voice |
| **Fish Audio S2-Pro / Drama 3** | Fish Audio Research Licence (S2-Pro) / Fish Audio Community Licence (Drama 3) | **Not without agreement** | 4B / 35B-A3B | Not documented | No | No | Drama 3 1278 (top open-weights model) | Best-sounding open weights in 2026 but licence blocks commercial posting without a deal |
| **Dia 1.6B / Dia2 (Nari)** | Apache 2.0 | Yes | 1.6B | Not supported (CUDA only; macOS on TODO) | No | No | — | Dialogue-oriented ([S1]/[S2]); voice drifts per run without a seed/clip; poor fit for single-voice narration |
| **Orpheus 3B (Canopy)** | Apache 2.0 code; weights inherit Llama 3.2 licence | Yes (Llama terms) | 3B | Runs via llama.cpp/Metal, ~1.75× slower than realtime on M4 | Slow | No | — | Expressive English, preset voices only; experimental |
| **CosyVoice 2/3** | Apache 2.0 | Yes | 0.5B | Not documented | No | No | — | Chinese-first; good cloning; engineering-heavy |
| **XTTS-v2 (Coqui)** | Coqui Public Model Licence | **No** (non-commercial) | — | Yes | Slow | No | 916 | Legacy; skip |
| **IndexTTS-2.5 (bilibili)** | bilibili Model Use Licence | **Restricted**; commercial by enquiry | — | Not documented (CUDA) | No | No | — | Good emotion/duration control for dubbing; licence friction |
| **Higgs Audio v3 (Boson)** | Research & Non-Commercial Licence | **No** without commercial licence | ~4B | GGUF on CPU works but slow (1.7× slower than realtime on M4) | Slow | No | — | High quality, 100+ languages; licence blocks use |
| **F5-TTS** | Code MIT; weights CC BY-NC 4.0 | **No** | — | Yes | Slow | No | — | Research cloning model; skip |
| **VibeVoice (Microsoft)** | MIT, "research use only" wording | Risky | 1.5B | Partial | No | No | 957 | Long-form multi-speaker; not a narration tool |
| **Breeze TTS 2** | Research/non-commercial | **No** | — | — | — | No | 1228 | Highest-rated open weights after Fish; licence blocks |
| **Supertonic 3 / Piper / MeloTTS** | Permissive | Yes | small | Yes | Yes | Piper: phoneme-level only | — | Fast CPU voices, noticeably robotic; captions-only fallback |

**Ranking for "clear, engaging explainer narration" under a commercial-OK licence:**

1. **Chatterbox Turbo** (English, MIT) — the most human-sounding open option; bracket tags for emphasis; voice clone from a 10 s reference lets you lock a house voice. Needs sentence-level chunking and a retry-on-garble loop (the agent can automate this with a Whisper WER check).
2. **Qwen3-TTS 1.7B** (Apache 2.0) — VoiceDesign lets you prompt "calm, precise, slightly warm male narrator, studio" and then save it as a reusable clone prompt. Mac path is community MLX, so expect setup friction.
3. **Kokoro-82M** (Apache 2.0) — the agent-friendliest: pip install, CPU-fine, deterministic, native word timestamps via Kokoro-FastAPI. Delivery is a bit flat for hooks but fine for the body of a video; `af_heart`, `am_adam`, `bm_george` are the usual picks.
4. **Orpheus 3B** — expressive but preset voices and slower; try only if 1–3 fail.
Fish Drama 3, Breeze, Higgs v3, IndexTTS and F5 are excluded on licence, not quality.

### 3. Cheap/free hosted alternatives (price per 1M characters)

| Service | Model | $/1M chars | Free tier | Commercial use | Word timestamps | Arena Elo | Notes |
|---|---|---|---|---|---|---|---|
| **OpenAI** | gpt-4o-mini-tts | ~$15 (billed $0.60/1M text tokens + $12/1M audio tokens) | No | Yes; usage policy requires disclosing the voice is AI | **No** | tts-1-hd 1106 | `instructions` param for tone; `marin`/`cedar` best; tts-1/tts-1-hd deprecated, shut down 2027-01-06 |
| **Google Cloud** | Chirp 3: HD | $30 | 1M chars/mo | Yes (GCP ToS) | **No** for Chirp 3 HD (no SSML `<mark>`/timepoints; forum confirms markup unsupported) | 1062 | Neural2 $16 supports SSML marks; Gemini 3.8 Flash TTS (token-billed, roughly $9/1M audio tokens ≈ $0.36/min) is Elo 1283 but also no word timing |
| **Azure AI Speech** | Neural / Neural HD | $16 / $22 | 500k chars/mo (F0), does not expire | Yes | **Yes** — WordBoundary events in the Speech SDK | — | Largest free tier of any major vendor; voices are competent but corporate-sounding |
| **Edge-TTS** (unofficial) | Edge "Read Aloud" neural voices | $0 | Unlimited | **No clear right**; Microsoft Q&A says using its services commercially without an Azure subscription "could be a violation" of ToS | Yes (WordBoundary) | — | Same voices as Azure; good for prototyping, do not ship published videos on it |
| **Inworld** | TTS-2 / TTS-2 Flash | $25 / $15 on-demand, down to $5–7 at volume | Small | Yes | Not confirmed | Realtime TTS-2 1267 | Cheapest high-quality API if you ever scale |
| **Cartesia** | Sonic 3.x | Pro $5/mo for 100k credits (1 credit/char ⇒ ~$50/1M equivalent) | 20k credits, personal use only | Pro+ | Yes (Sonic supports timestamps) | Sonic 3.6 1296 | Real-time oriented; strong quality; cheap entry tier |
| **Hume** | Octave 2 | Creator $14/mo for 140k chars; overage $0.15/1k | 10k | Commercial licence listed only on Enterprise per CostBench — check before use | Not confirmed | 1060 | Emotion/acting direction; weaker on licence clarity |
| **HeyGen / HyperFrames** | HeyGen "Starfish" voices via `npx hyperframes tts` | HeyGen plan | — | HeyGen plan | **Yes** with `--words` | — | Provider order in the skill is HeyGen → ElevenLabs → local Kokoro; ElevenLabs/Kokoro paths need `transcribe` for words |

Takeaways: Azure's 500k free characters with native word boundaries is the best "free and legal" hosted option; Edge-TTS is the same voices without the licence. OpenAI and Chirp 3 HD both lack word timing, so they'd need forced alignment anyway.

### 4. Caption timing: getting word-level timestamps

You already know the script, so the problem is **alignment**, not transcription. Options in order of preference:

1. **Native TTS timestamps.** ElevenLabs `with-timestamps` (character → word grouping), Kokoro-FastAPI `captioned_speech`, Azure WordBoundary, Cartesia, HeyGen `--words`. Zero extra inference, exact to the engine's own frame grid. Caveat: alignment is against the *normalised* text, so map back to your display script (numbers, acronyms, code names).
2. **Forced alignment with a known transcript.** Feed the script + audio to a CTC aligner: `torchaudio` MMS_FA / `ctc-forced-aligner` (multilingual wav2vec2; CoreML port exists for Mac), WhisperX's `align()` step on your own segments (wav2vec2 CTC, <100 ms accuracy claimed), or ElevenLabs `/v1/forced-alignment` (hosted, returns words + loss). Best route for Chatterbox and Qwen3-TTS output. Runs fine on CPU for 60 s clips.
3. **ASR with word timestamps** (WhisperX, stable-ts, whisper-timestamped, faster-whisper `word_timestamps=True`). Use only when you do not have the exact text. WhisperX = faster-whisper + wav2vec2 alignment; runs on Apple M-series via MPS (~20× realtime for transcribe+align on M4 Max) and on CPU (~8×). Vanilla Whisper word times are interpolated and drift by hundreds of ms — do not use them for karaoke-style captions.

Pipeline recommendation for the agent: TTS → (native timestamps if available, else `ctc-forced-aligner` against the script) → run a cheap sanity check (faster-whisper small.en WER against the script; re-render the sentence if WER > ~5%) → emit a flat `[{text,start,end}]` word array → caption renderer. Treat sub-80 ms word boundaries as "good enough" for burned-in captions at 30 fps (one frame = 33 ms).

---

## B. Music

### 5. Royalty-free and AI music for commercial social posting

**Library sources (no subscription):**

| Source | Licence | Attribution | Commercial / social use | Fit for "hyper-clean sci-fi lab" beds | Agent-friendliness |
|---|---|---|---|---|---|
| **Pixabay Music** | Pixabay Content Licence | Not required | Yes; may not redistribute standalone or use in trademarks | Decent minimal-techno / ambient selection; quality uneven; some tracks are Content-ID registered by uploaders (check "cleared" flags) | Good: public search, direct MP3 download |
| **Free Music Archive** | Per-track CC (BY, BY-SA, BY-ND, BY-NC-*, CC0) | Required for all CC except CC0 (title, artist, URL, licence) | Only CC BY / BY-SA / CC0 — **BY-ND cannot be synced to video**; NC excluded | Large experimental/electronic catalogue; filter by licence | Medium: filter by licence; paid Tribe of Noise PRO tier if you want indemnity |
| **Uppbeat (free tier)** | Uppbeat free licence | **Required**: paste the per-track credit in the description | 3 downloads/month; personal channels and small creators OK; no client/corporate/advertising use | Curated, modern, lots of "tech/ambient" tags; free catalogue is a subset | Low volume (3/mo); Premium $8.25/mo removes attribution and limits |
| **YouTube Audio Library** | YouTube Audio Library licence / some CC BY | CC tracks: credit required | **Off-YouTube use is not granted**; YouTube says it cannot resolve off-platform questions; guides say contact the artist | Fine on YouTube Shorts only | Poor for TikTok/IG cross-posting |
| **Incompetech (Kevin MacLeod)** | CC BY 4.0, or paid no-attribution licence | Required (exact wording template on site) | Yes with credit; monetised YouTube explicitly OK | Many ambient/electronic cues, recognisable "stock" sound | Good: direct download; dated production for a premium look |

**AI music generation:**

| Tool | Plan needed for commercial use (Nov 2026) | Cost | Notes for ambient/minimal-techno beds |
|---|---|---|---|
| **Suno** | Pro ($10/mo) or Premier ($30/mo); Free/Basic is non-commercial and Suno retains ownership of free-tier output | Pro: 2,500 credits + 20 downloads/mo; Premier: 10,000 credits + 60 downloads | Download caps introduced after the Warner deal (Nov 2025); v5.x models to be deprecated for licensed models, no date; strong at instrumental genre prompts; tracks made while subscribed keep commercial status |
| **Udio** | Pro ($30/mo) only; Standard ($10) is private use | 6,000 credits/mo | Post-UMG-settlement; Pro-only commercial rights make it pricier than Suno for this use |
| **ElevenLabs Music (Eleven Music)** | Any paid plan (Starter+); "cleared for nearly all commercial uses" incl. social, ads | Uses plan credits; API for paid subscribers; 3 s–5 min, instrumental mode | If you already pay for ElevenLabs TTS this is the zero-extra-subscription route; quality is good for beds, less distinctive than Suno |
| **ACE-Step 1.5** (StepFun/ACE) | MIT code; model card states generated music may be used commercially (terms not yet in a versioned LICENSE — GitHub discussion #1256 unanswered) | Free; <4 GB VRAM for 2B; **MPS/MLX on Apple Silicon and CPU supported**; 10 s–10 min output | Best open option: fast (seconds on GPU), instrumental prompts work, "between Suno 4.5 and 5" by its own claim; keep provenance notes |
| **Stable Audio Open 1.0 / Stable Audio 3** | Stability AI Community Licence: free commercial use under $1M annual revenue after self-registration | Free; 47 s max for Open 1.0 (stereo 44.1 kHz); Stable Audio 3 Medium to 6:20 | Explicitly better at SFX/ambience than music; 47 s is enough for a 60 s video if you loop/crossfade; training data licensed (Stability claim) |
| **MusicGen (Meta)** | Weights CC BY-NC 4.0 → **non-commercial only** | Free | HyperFrames `bgm` can call it locally, but do not use its output in posted videos |
| **Google Lyria (via Gemini API)** | Gemini API terms | Metered | HyperFrames `bgm` default when `GEMINI_API_KEY` set; check output-rights clause before publishing |
| **Magenta RealTime 2** | CC BY 4.0 weights; Google claims no rights in outputs | Free; 230M/2.4B on-device | Steerable continuous instrumental; worth a look for loopable ambient |

**What suits a "hyper-clean sci-fi lab" bed?** You want 90–110 BPM minimal techno or beatless ambient with sidechain-ducked pads, a soft sub pulse, filtered white-noise risers and sparse, bright UI-like plucks, mixed with lots of headroom (−18 to −20 LUFS under narration). Practical ranking:
1. **ACE-Step 1.5** locally with prompts like "minimal techno, clean sub kick, airy pads, glassy plucks, no vocals, 100 BPM, laboratory, sterile, futuristic, loopable" — generate 8 bars, pick, loop. Free, commercial-OK by the model card, agent-scriptable, runs on the Mac.
2. **Eleven Music** if you are already on ElevenLabs Creator; prompt the same way, request instrumental.
3. **Pixabay** + **FMA CC0/CC BY** search terms: "minimal techno", "ambient technology", "cyberpunk ambient", "laboratory", "synthwave minimal". Build a vetted pool of 10–15 beds once and reuse (consistency is a brand asset).
4. **Suno Pro** only if you want vocal hooks or more produced tracks; its download caps and model-deprecation roadmap make it a weaker long-term dependency.

### 6. Sound effects

| Source | Licence / terms | Attribution | Agent-friendliness | Notes |
|---|---|---|---|---|
| **Freesound** | Per-clip CC0, CC BY 3.0/4.0, CC BY-NC | None for CC0; required for BY | Good: REST API with `license:"Creative Commons 0"` filter; needs free API key | Best for CC0 UI clicks, whooshes, lab hums; quality varies, normalise everything |
| **Pixabay SFX** | Pixabay Content Licence | Not required | Good: search + direct download | Polished, consistent; good whoosh/glitch/UI packs |
| **Zapsplat** | Standard (free) licence | **Required** for free users ("Sound from Zapsplat.com"); Gold from £5/mo removes it, adds WAV, unlimited downloads | Medium: 3 downloads per 15 min on free; no official API | Monetised YouTube and streams explicitly allowed with credit |
| **ElevenLabs SFX** | Plan credits; royalty-free per pricing page | None | Good: API (`eleven_text_to_sound_v2`, v3 limited access); 0.1–30 s; seamless looping option | 40 credits/second when you fix duration → a 1 s click ≈ 40 credits; great for bespoke "data chirp", "hologram materialise" sounds |
| **Programmatic synthesis (existing Python SFX synth)** | Yours | None | Best: deterministic, versionable, zero licence risk | Already in the pipeline; extend with FM blips, filtered-noise whooshes, sidechain "ducks" for captions; use ElevenLabs/Freesound only for organic textures the synth can't do |
| **Stable Audio Open** | Stability Community licence (<$1M revenue) | None | Medium | Model card says it is better at SFX/field recordings than music — a good local generator for ambience layers |

---

## Recommendation matrix

Scores 1–5 (5 best). "Agent" = how easily a Claude agent can drive it headless on Mac or Linux. "Timestamps" = native word timing.

| Candidate | Quality | Cost (25 vids/mo) | Agent | Timestamps | Licence clarity | Verdict |
|---|---|---|---|---|---|---|
| **ElevenLabs Creator — Eleven v4 / Multilingual v2** | 5 | 4 ($22/mo, plenty of headroom) | 5 (clean REST, SDKs, MCP) | 5 (char-level → words; forced-alignment API) | 5 (paid = commercial) | **Primary voice if paying is acceptable** |
| **Chatterbox Turbo (local, MIT)** | 4 | 5 (free) | 4 (pip/MLX; needs chunk+retry loop) | 2 (forced-align step) | 5 (MIT; watermark harmless) | **Best free voice**; house voice via 10 s clone |
| **Kokoro-82M (local, Apache)** | 3 | 5 | 5 (CPU, deterministic, FastAPI server) | 5 (captioned_speech) | 5 | **Best free fallback / cloud-container default**; already wired into HyperFrames |
| **Qwen3-TTS 1.7B (local, Apache)** | 4 | 5 | 3 (CUDA-first; MLX port on Mac) | 2 | 5 | Worth testing for a designed bespoke voice |
| Azure Neural HD (hosted) | 3.5 | 5 (500k free/mo) | 4 | 5 (WordBoundary) | 5 | Good free hosted option; voices read "enterprise" |
| OpenAI gpt-4o-mini-tts | 4 | 5 (~$1/mo) | 5 | 1 | 4 (disclose AI voice) | Fine voice, no timing → needs aligner |
| Google Chirp 3 HD / Gemini 3.8 Flash TTS | 3.5 / 4.5 | 5 (1M free) | 4 | 1 | 5 | Gemini TTS sounds great but no word timing |
| Edge-TTS | 3.5 | 5 | 5 | 5 | 1 | Prototyping only |
| Fish Drama 3 / Higgs v3 / Breeze / F5 / XTTS | 4–5 | 5 | 3 | 1 | 1 (non-commercial) | Excluded on licence |
| **Music: ACE-Step 1.5 (local)** | 4 | 5 | 4 (MLX on Mac, CLI) | n/a | 4 (card says commercial OK; no versioned LICENSE) | **Primary bed generator** |
| Music: Eleven Music | 4 | 4 (shares plan credits) | 5 | n/a | 5 | Use if on ElevenLabs anyway |
| Music: Pixabay / FMA CC0-BY | 3 | 5 | 4 | n/a | 4 | Build a vetted reusable pool |
| Music: Suno Pro / Udio Pro | 4.5 | 3 ($10–30/mo) | 2 (no official API; download caps) | n/a | 3 (plan-gated, shifting terms) | Optional |
| Music: MusicGen | 3 | 5 | 4 | n/a | 1 (NC) | Do not publish |
| **SFX: Python synth + Freesound CC0 + ElevenLabs SFX** | 4 | 5 | 5 | n/a | 5 | Current plan is right |

### Concrete stack suggestion

- **Mac (daily production):** ElevenLabs v4 for the voice (Creator plan), Chatterbox Turbo via `chatterbox-mlx` as the no-cost alternate and for A/B tests, Kokoro-FastAPI for scratch tracks and timing checks. ACE-Step 1.5 (MLX) for beds; Python synth + Freesound CC0 for SFX; ElevenLabs SFX for the few organic sounds.
- **Linux cloud container (agent runs, no GPU):** Kokoro CPU for scratch audio and timing, ElevenLabs API for final audio, `ctc-forced-aligner` / WhisperX-align for anything without native timing, faster-whisper `small.en` for the WER gate. Pre-generate the music pool on the Mac and commit it to the media library so the container never needs a music model.
- **Licence hygiene the agent should enforce:** record provider, model, plan and date in each video's manifest; refuse to render finals on ElevenLabs Free, Edge-TTS, MusicGen, Fish, Higgs, F5 or XTTS; keep attribution strings for any CC BY asset in a `CREDITS.md` the post-copy step reads.

---

## Test plan: TTS shoot-out

**Script.** One fixed 60 s explainer (~150 words) that includes: a punchy 1-sentence hook, two acronyms (e.g. "GPU", "RAG"), one version number ("v4.1"), one URL-ish token or product name, a parenthetical aside, a rhetorical question, and a closing CTA. Store as `tests/tts/script.txt` plus a hand-written "display" version for captions.

**Candidates (render the identical text with each, default settings, then one tuned pass):**
1. **ElevenLabs Eleven v4** (one male, one female stock narrator; stability 0.6) and **Multilingual v2** with the same voices, via `with-timestamps`.
2. **Chatterbox Turbo** (local MLX on Mac): default voice, then a clone from a 10–15 s clean studio reference; `exaggeration` 0.4–0.6, `cfg_weight` 0.3–0.5; chunk per sentence.
3. **Kokoro-82M** (`af_heart`, `am_adam`, `bm_george`) through Kokoro-FastAPI `captioned_speech` so timestamps come for free.
4. **Qwen3-TTS 1.7B VoiceDesign** with a text-designed "calm, precise tech narrator" voice, saved as a reusable clone prompt (optional 4th; drop if Mac setup takes more than an hour).

Optional hosted control: Azure Neural HD (free tier) to calibrate "what free hosted sounds like".

**What to judge (blind, randomised order, 2–3 listeners plus you; 1–5 scale each):**
- *Clarity / intelligibility* on acronyms, numbers and product names (also compute objective WER by transcribing each render with faster-whisper `medium.en` against the script).
- *Engagement*: does the hook sentence land? pacing variety, natural emphasis, absence of monotone.
- *Artefacts*: breaths, clicks, sped-up endings, hallucinated words, mispronunciations (count per render).
- *Consistency*: render the script 3 times; measure duration variance and listen for voice drift (critical for a series).
- *Timestamp quality*: for each engine, overlay captions from (a) native timestamps and (b) `ctc-forced-aligner`; measure median |Δ| vs. a manually tapped 20-word reference; anything under ~60 ms passes.
- *Ops*: wall-clock render time on the M-series Mac and in the Linux container, retries needed, lines of glue code, and licence/attribution obligations triggered.
- *Cost*: credits/characters actually consumed per 60 s, extrapolated to 25 videos.

**Decision rule.** Pick the highest "clarity × engagement" that scores ≥4 on consistency and has a commercial-OK licence. If the free winner is within ~0.5 of ElevenLabs on the listening score, ship free and keep ElevenLabs Creator for hooks only (first 3 s), where voice quality matters most for retention.

---

## Sources

ElevenLabs
- https://elevenlabs.io/pricing
- https://elevenlabs.io/pricing/api
- https://elevenlabs.io/docs/help-center/legal/can-i-publish-the-content-i-generate-on-the-platform
- https://elevenlabs.io/docs/overview/capabilities/text-to-speech
- https://elevenlabs.io/docs/api-reference/text-to-speech/convert-with-timestamps
- https://elevenlabs.io/docs/api-reference/forced-alignment/create
- https://elevenlabs.io/docs/overview/capabilities/music
- https://elevenlabs.io/docs/overview/capabilities/sound-effects
- https://openrouter.ai/elevenlabs/eleven-v4
- https://fal.ai/models/fal-ai/elevenlabs/tts/eleven-v3
- https://www.segmind.com/models/tts-elevenlabs-with-timestamps

Open-source / open-weight TTS
- https://www.cartesia.ai/learn/open-source-tts
- https://openvoxai.com/blog/best-tts-models-local-cloud-2026
- https://localaimaster.com/blog/best-local-tts-models
- https://artificialanalysis.ai/text-to-speech/leaderboard
- https://github.com/hexgrad/kokoro
- https://github.com/remsky/Kokoro-FastAPI
- https://huggingface.co/onnx-community/Kokoro-82M-v1.0-ONNX-timestamped
- https://huggingface.co/mattmireles/kokoro-coreml
- https://github.com/resemble-ai/chatterbox
- https://pypi.org/project/chatterbox-mlx/
- https://www.podonos.com/resembleai/chatterbox-turbo-vs-elevenlabs-turbo?t=o
- https://tts-comparison-4hg.pages.dev/
- https://github.com/QwenLM/Qwen3-TTS
- https://github.com/fishaudio/fish-speech
- https://github.com/nari-labs/dia
- https://github.com/index-tts/index-tts
- https://github.com/boson-ai/higgs-audio

Hosted TTS alternatives
- https://texttolab.com/blog/openai-tts-pricing
- https://developers.openai.com/api/docs/guides/text-to-speech
- https://cloud.google.com/text-to-speech/pricing/?authuser=4
- https://discuss.google.dev/t/chirp3-hd-voices-dont-support-markup-field-in-long-audio-synthesis/185977
- https://texttolab.com/blog/azure-text-to-speech-pricing
- https://learn.microsoft.com/en-us/answers/questions/2088770/are-opensource-edge-tts-free-for-commercial-use
- https://inworld.ai/resources/tts-api-pricing-comparison
- https://www.eesel.ai/blog/cartesia-sonic-3-pricing
- https://costbench.com/software/voice-apis/hume-ai/
- https://mcpservers.org/agent-skills/heygen-com/hyperframes-media

Caption timing / alignment
- https://cdn.localaimaster.com/blog/whisperx-guide
- https://huggingface.co/papers/2303.00747
- https://huggingface.co/chordai/mms-fa-aligner-coreml
- https://replicate.com/cureau/force-align-wordstamps

Music
- https://pixabay.com/service/license-summary/
- https://freemusicarchive.org/License_Guide
- https://licenseorg.com/guide/music-audio/uppbeat
- https://lickd.co/youtube-audio-library/
- https://www.digitalapplied.com/blog/social-video-music-rights-platform-comparison
- https://incompetech.com/music/royalty-free/faq.html
- https://dynamoi.com/learn/ai-music-distribution/suno-commercial-rights-explained
- https://gptprompts.ai/udio-pricing
- https://github.com/ace-step/ACE-Step-1.5
- https://github.com/ace-step/ACE-Step-1.5/discussions/1256
- https://huggingface.co/stabilityai/stable-audio-open-1.0
- https://stability.ai/news/license-update
- https://www.creativeainews.com/articles/best-open-source-ai-music-models-2026/

Sound effects
- https://licenseorg.com/guide/music-audio/freesound
- https://www.zapsplat.com/faq-category/license-and-usage/
- https://elevenlabs.io/docs/overview/capabilities/sound-effects
