# Shortlist — week 2026-46 (run 2026-11-11, mode: weekly)

Pulled: GitHub search (4 queries, 213 new repos ≤7 d > 200★ — ~40 of them a star-farmed "desktop installer" spam wave created 2026-11-06, dropped), HN front page + Show HN (Nov 4–11), lab feeds (OpenAI, DeepMind, Mistral, HF, Anthropic mirror, Claude Code changelog), TLDR AI/Dev, Rundown, Ben's Bites, HF trending models + daily papers, skills.sh, Anthropic plugin marketplaces. Raw pulls in `raw/2026-11-11-*`. Star counts below re-verified against the GitHub search API at 11:30 ET; everything else is as pulled.

Scoring: `docs/03` rubric (velocity .25 · timeliness .15 · novelty .15 · explainability .20 · visualizability .15 · relevance .10); shortlist ≥ 3.4; gates explainability ≥ 3, visualizability ≥ 2.

**Pilot recommendation: #3 (pinky)** — crispest mechanism, uses the one primitive the library already has, broad relevance, verifiable from the README, no legal hedging. **#1 (the recompilation wave)** is the strongest hook of the week and should be video 2.

---

### 1. The Switch recompilation wave — Hookshot / totk-pc-recomp / S2Arm — *These are not emulators. The game was rewritten.*
lane: **hot** (window ~1 week; Hookshot is 6 days old) · format: How X works · **score 4.55** (V5 T5 N4 E4 Vis5 R4)
signal: Hookshot 7,330★ in 6 d (GPL-3.0) · totk-pc-recomp 6,635★ in 13 d (MIT) · S2Arm 2,569★ in 3 d (Apache-2.0); same upstream lineage (Ryujinx, nxnative, hactool); two of three say most code was written by Claude Code
mechanism: an emulator interprets the console's instructions one by one at runtime; static recompilation translates the game's ARM64 machine code into C *once*, compiles it to a native binary, and replays the console's graphics calls (NVN) on Vulkan/Metal. The repos ship no game data — the user's own dump is recompiled on their machine (10–45 min, ~60 GB scratch for Hookshot).
visual primitive: `pipeline` (ARM64 dump → lifter → C → native binary; side branch NVN → Vulkan) with **before/after** against the emulator loop · analogy: an interpreter translating a speech sentence by sentence vs a translator rewriting the whole book once
hooks: #12 observation "This is not an emulator. The game was rewritten, line by line, by a machine." · #1 "Seven thousand stars in six days. For a Zelda port that contains no Zelda."
sources: github.com/NotRexed/Hookshot (README) · github.com/valentderah/totk-pc-recomp · github.com/jhaizhou-ops/S2Arm
risks: legal footing of recompiling a current commercial title — the video explains the technique and the no-game-data design, never links dumps or shows game footage; FPS claims unverified (don't use); credit all three authors + upstream.

### 2. craft-anything (storytold) — *It watches software and rebuilds it without reading its code.*
lane: **hot** · format: How X works · **score 4.40** (V5 T4 N4 E4 Vis5 R4)
signal: 28,053★ in 11 d, 5,685 forks (Apache-2.0/MIT); same team as FilmCraft/PhotoCraft/WordCraft (the "written from scratch in Rust" family)
mechanism: four stages — *Study* (≈320 inspection tools capture a site at three viewport widths, or a binary via decoders/Ghidra in Deep mode) → *Build* (drives the user's own Claude Code/Codex to write a fresh project) → *Check* (diffs the rebuild against the capture, feeds differences back) → *Ready*. Default "clean room" mode reads only observable behaviour, never the original's source.
visual primitive: `cycle` (study → build → check → repeat) with the capture/rebuild diff as the highlight · analogy: a tailor who measures the suit you're wearing and sews a new one — never touching your pattern
hooks: #1 "Twenty-eight thousand stars in eleven days. It rebuilds any app without reading a line of its code." · #6 "Do you know what a clean room is, in software? You will."
sources: github.com/storytold/craft-anything (README, docs/tools.md for the tool count)
risks: early alpha by its own README; no fidelity metrics (don't claim accuracy); the 320-tool count must be checked in docs/tools.md; "clean room" has a legal meaning — state it precisely. Pairs with #11 BLA (the defence) as a two-parter.

### 3. pinky (DIYgod) — *An agent can use your phone. A gate decides what it may touch.* ← **pilot**
lane: **hot** · format: How X works · **score 4.35** (V3 T5 N4 E5 Vis5 R5)
signal: 1,846★ in 5 d (Apache-2.0); author of RSSHub (credible, large following)
mechanism: a desktop app exposes a real phone to AI agents over MCP (Android via adb/scrcpy, iPhone via Apple's developer disk image). The design point is a **gateway between agent and phone** that enforces rules in code, not in the prompt: flagged actions return "approval pending" and block until the user clicks; before tapping it re-checks the target is still where it was; banking/wallet/password apps are hidden; the agent cannot type into password or OTP fields; the unlock PIN lives in the OS keychain.
visual primitive: `pipeline` (agent → gateway → phone) with the gateway highlighted, then `zoom` into the gateway's four rules · analogy: a bouncer who checks the ID at the door — the rule lives in the door, not in the guest's promise
hooks: #10 "An agent can now use your phone. I want you to see what stands between it and your bank." · #12 "The rule is not in the prompt. It is in the door."
sources: github.com/DIYgod/pinky (README)
risks: pre-alpha by its own README; latency figures are author-run (don't use); telemetry on by default (mention neutrally or skip). Clean for the pilot: one primitive we have (`pipeline`) plus one we need anyway (`zoom`).

### 4. Decision models instead of LLM calls — Amazon/Strands "decider", Hightouch, PostHog, HF — *A small model says yes or no. The large one is only called when it isn't sure.*
lane: **hot** (pattern crystallising this week) · format: How X works · **score 4.25** (V4 T5 N4 E5 Vis4 R3)
signal: Amazon/Strands post 714 pts (Nov 10) · Hightouch "Jev" 600 pts (Nov 6) · PostHog (TLDR Dev 11-10) · HF "Decision models" post (Nov 10) · Show HN Flide
mechanism: routine binary decisions (is this ticket urgent? is this record a duplicate?) go to a small, cheap scoring model; only when its confidence falls below a threshold is the frontier model called. The threshold is set by what a wrong answer costs. Four independent teams published the same pattern in one week.
visual primitive: `before-after` (every call → big model vs small model + escalation) then `graph` (confidence threshold as a gate) · analogy: triage at a clinic — the nurse decides most cases; the specialist sees the uncertain ones
hooks: #4 "You do not need the large model for most of your calls. Amazon stopped using it for theirs." · #1 "Four companies published the same idea in one week. None of them talked to each other."
sources: strandsagents.com blog (Amazon) · Hightouch post · PostHog post · HF blog (all in raw/2026-11-11-hn-feeds.md)
risks: "saves millions" is Amazon's own claim — attribute, don't assert; name the pattern, not the vendors' marketing.

### 5. OpenAI's kernel pipeline — 1,724 crashes reproduced, 948 proven exploitable, patched without a human — *Find. Prove. Fix. No one in the loop.*
lane: **hot** · format: What X is · **score 4.15** (V4 T5 N4 E4 Vis4 R4)
signal: openai.com "A thousand fewer paths to root" (Nov 4), 489 pts; same week as PHP2Shell (1,309 pts) and Anthropic's Glasswing tracker
mechanism: a three-stage pipeline — reproduce a reported kernel crash in a sandbox → attempt to prove it can be escalated to root (the proof is the filter: 1,724 → 948) → write a patch and validate it against the reproduction. Each stage is an agent with a verifier behind it.
visual primitive: `pipeline` with a `counter` narrowing 1,724 → 948 → patched · analogy: a building inspector who first proves a crack can bring the wall down before anyone is sent to fix it
hooks: #1 "Nine hundred and forty-eight ways to take over a computer. Found, proven and closed by a machine." · #12 "It did not look for bugs. It looked for proof."
sources: openai.com/index/a-thousand-fewer-paths-to-root
risks: security topic — the video explains the pipeline, never any exploit; numbers must come from OpenAI's post verbatim; neutral on vendors.

### 6. unslop (heydamir) — *Why AI-made interfaces all look the same — and the nine passes that fix it.*
lane: **hot** · format: How X works · **score 4.10** (V5 T4 N3 E4 Vis4 R4)
signal: 14,373★ in 13 d (CC BY 4.0); creator runs the "Unslopping" series on X; Claude Code / Codex skill
mechanism: three ordered phases — *Audit* lists the "slop" markers (gradients, glows, emoji labels, loud copy, uneven spacing) with locations; *Direction* proposes a visual character and one signature detail before any edit; *Passes* apply fixes in a fixed order: spacing, colour, icons, copy, type, layout, details, visuals, motion.
visual primitive: `before-after` (the same screen, slop → designed) + `pipeline` of the nine passes · analogy: an editor who first marks every cliché in a manuscript, agrees the voice with the author, then rewrites in a fixed order
hooks: #7 "Your interface looks like every other AI interface. This is the list of why." · #8 "Nine passes, in this order. The order is the point."
sources: github.com/heydamir/unslop (SKILL.md)
risks: CC BY 4.0 requires attribution (we'd credit anyway); the account's own aesthetic is a design statement — Helena explaining design is on-brand, but keep her neutral about taste.

### 7. Apple Intelligence's personal knowledge graph — *Your Mac keeps a private map of who matters to you.*
lane: **hot** · format: How X works · **score 4.10** (V4 T4 N4 E4 Vis4 R5)
signal: 863 pts on HN (Nov 7); privacy-mechanism week (Gemini annotators 723, Gemini chat-history training 737)
mechanism: on-device Apple Intelligence builds a graph of people from messages and photos and scores relationships (someone reverse-engineered the labels, including a family-member classifier). Nothing leaves the device; the interesting part is *what* is inferred and *from what signals*.
visual primitive: `graph` (you at the centre, edges weighted by signals: message frequency, photo co-occurrence, calendar) · analogy: a receptionist who never asks your name but knows who to let in
hooks: #12 "Your computer has decided who your family is." · #6 "Do you know what your phone has concluded about the people in your photos? It does."
sources: 8rank.ai write-up (HN 50403097) — **a single reverse-engineering post; verify every label against it and Apple's published docs before scripting**
risks: factual accuracy depends on one source; must not overstate ("decided" → "scores"); privacy tone stays observational — Helena's register fits this one unusually well.

### 8. A TV signal can see through walls — RF fading as a motion sensor — *Your television can tell when someone moves in the next room.*
lane: **evergreen** · format: How X works · **score 4.05** (V3 T3 N4 E5 Vis5 R5)
signal: 270 pts on HN (Nov 10; a 2025 post resurfaced — timeliness scored low, mechanism scored high)
mechanism: broadcast signals bounce around a building and arrive at the antenna by many paths; a body moving changes how those paths add up (fading), and that change alone reveals movement behind a wall — no camera, no special hardware.
visual primitive: `graph`/`tiles` (multipath rays, one body moving, the interference pattern flickering) · analogy: ripples in a pond when someone walks along the far bank
hooks: #12 "Your television can see you move. It does not need a camera." · #3 "There is a motion sensor in your living room that nobody installed."
sources: maurycyz.com/projects/fading/
risks: resurfaced content, not news — fine for evergreen; keep claims to the author's demo, no surveillance speculation.

### 9. AlphaProof Code (DeepMind) — *They did not test Signal's encryption. They proved it.*
lane: **hot** · format: What X is · **score 4.00** (V4 T5 N5 E3 Vis4 R3)
signal: deepmind.google (Nov 10), 662 pts; formal-verification week (Axiom's Stacks Project, Fable 5.2 FLT post)
mechanism: instead of running tests (which check some inputs), agents wrote ~3M lines of Lean — machine-checked mathematical proofs that Signal's core encryption does what it claims — and a tiny trusted checker verifies every step.
visual primitive: `before-after` (tests check some doors; a proof checks every door at once) + `counter` (3,000,000 lines) · analogy: checking a bridge by driving trucks over it vs proving the beams hold from the laws of physics
hooks: #12 "They did not test the code. They proved it." · #1 "Three million lines of mathematics, to confirm one app keeps a secret."
sources: deepmind.google/blog/introducing-alphaproof-code/
risks: explainability is the gate here (E3) — the script must land "test vs proof" in one analogy or the video fails; numbers from the DeepMind post only.

### 10. Llama-modchip — a 284B model on 64 GB of RAM, no GPU — *It only loads the part of the brain it is using.*
lane: **evergreen** (the mechanism is Mixture-of-Experts; the repo is the trigger) · format: How X works · **score 3.95** (V3 T4 N3 E5 Vis5 R4)
signal: 483 pts on HN (Nov 8); local-model week (Apple's local-model Mac app 426, Microsoft Foundry Local, RAM price shock)
mechanism: a mixture-of-experts model activates only a few "experts" per token; the runner keeps the active experts in RAM and streams the rest from disk on demand — fitting a 284B-parameter model on a desktop by trading speed for memory.
visual primitive: `tiles` (the experts grid; a few light up per token) + `stack` (disk → RAM → active) · analogy: a library where you only carry the books you're reading; the rest stay on the shelf
hooks: #1 "A two-hundred-and-eighty-four-billion-parameter model, on a computer with no graphics card." · #12 "It does not load the model. It loads the part it is thinking with."
sources: HN 50411961 → repo `github:synchopate/llama-modchip` — **verify the repo and numbers before scripting (not fetched this run)**
risks: repo unverified this run; MoE explanation must stay correct (experts ≠ topics).

---

## Honourable mentions (scored, not shortlisted)

| Candidate | Score | Why held |
|---|---|---|
| BLA — "Blind LLM Agents" defence against reverse-engineering agents (5,264★) | 3.70 | mechanism (poison / exhaust / hallucinate) only means something next to craft-anything — keep as part 2 of #2 |
| Anthropic "Components of Agent Memory" — consolidation while idle | 3.85 | strong evergreen; wait for a trigger with numbers |
| The OpenSSH password-length bypass (HN 2,999 pts) | 4.10 | week's biggest story, but security-bug explainers sit close to the content boundary; only as a conceptual "how a length check fails" with no reproduction — Kyle's call |
| The GitHub star-farm wave (≈40 "installer" repos born 2026-11-06 with ~1,300★ each) | 3.80 | wildcard from our own pull; very Helena ("none of them are real"); would need a careful, non-naming treatment |
| E-means — k-means in a tenth of the epochs (503 pts) | 3.55 | clean single diagram, narrow audience |
| floorplan — plain-English map of a codebase (3,565★) | 3.50 | good evergreen "how an agent maps code"; thin trigger |
| janestreet/agent_skills (5,244★) · t3dotgg/tstack (3,470★) | — | READMEs not fetched; re-score next run |
| Lichii / Eglantine Switch 2 emulators (8,430★ / 5,821★) | — | emulation legal grey + the recomp story covers the ground |
| GestaltX (6,026★ in 2 d), gpu-unlock-ada (4,870★) | — | jailbreak / firmware-unlock territory — content boundary |

## Run notes
- GitHub per-repo API is blocked from this container; `search/repositories?q=repo:a/b+repo:c/d` returns full repo objects and is the verification path. Star counts from WebFetch-rendered pages were unreliable (one fetch returned 730 for a 28k repo) — never cite a number that didn't come from the API.
- Spam detection worked by eye this run (identical star counts, created the same day, HTML "installer" repos). Next run: auto-flag clusters of ≥5 repos created within 24 h with stars within ±5 % of each other.
- HN Algolia `numericFilters` was flaky through the fetch tool; the agent fell back to the daily front-page archive. Fine for weekly; the hourly job should use the Firebase endpoint when it has a runner with network.
