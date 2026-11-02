# 04 — Script framework

Evidence base: `docs/research/hooks-and-retention.md` (platform statements, creator playbooks, studies; vendor claims are labelled there and should be treated as hypotheses until our own analytics confirm them).

## The shape of a tech_splained video

| Beat | Time | Job | Rules |
|---|---|---|---|
| **1 Hook** | 0–3 s | Open one loop, make one promise | Text on frame 0 + first spoken word within 0.5 s. 8–15 spoken words. Works muted. No logo, no intro, no "in this video". |
| **2 Proof** | 3–12 s | Prove the promise is real | First concrete fact or diagram element by 5 s. Name the searchable thing (repo / model / tool) on screen and in voice here. |
| **3 Mechanism ①** | 12–24 s | The first step of *how* | One idea. Introduce the analogy. Diagram shows scale/consequence while the voice explains mechanism (dual narrative). |
| **4 Mechanism ②** | 24–36 s | The second step | Chain with "but" / "so", never "and". |
| **5 Peak / re-hook** | ~30–42 s | The "wait, really?" moment | A surprising number, the clever trick, a dry joke from the subject itself. Explicitly re-open the loop: "but that's not the clever part." |
| **6 Resolution** | 42–52 s | Close the loop; break or pay off the analogy | Callback to the hook's key word or image. The diagram returns to a state that mirrors frame 0. |
| **7 CTA** | last 3–5 s | One ask | Spoken + on screen, inside the loop (no fade to black, music keeps going). |

Length: **default 40–50 s; cap 60 s.** Go long only when the payoff needs it. Every month, ship at least two "tight news" variants (30–40 s) against "deep" variants (50–60 s) and compare completion (see 09).

Word budget at a calm narration pace (~2.4 words/s): 45 s ≈ 110 words, 55 s ≈ 130 words. Dense script, calm voice — if it's too long, cut content, don't speed the voice.

## Writing order

1. **Ending first.** Write the payoff sentence and the callback line. If you can't, you don't have a video yet.
2. **Hooks.** Write 3–5 across at least two archetypes (below). Pick a primary and keep an alternate for A/B.
3. **Frame 0.** Hook text + one diagram element. ≤ 3 objects. Doubles as the cover.
4. **Body.** One idea per sentence. A visual change (new element, step, highlight) every 2–3 s. An explicit open loop every 10–15 s.
5. **Analogy.** One, from everyday physical life; state where it breaks.
6. **Say vs show.** Never narrate what the diagram already shows; narrate the *why*, show the *what*.
7. **Source-check table.** Every claim gets a location in the primary source.

## Hook library

Combine at most two archetypes. Rotate ≥ 4 archetypes per month so the audience doesn't learn the pattern. Use "nobody is talking about" only when literally true.

| # | Archetype | Pattern | tech_splained phrasing (examples, not reusable verbatim) |
|---|---|---|---|
| 1 | Specific number + gap | A concrete number big enough to fill the screen, then withhold the why | "This repo got 40,000 stars in six days. Nobody could explain why." |
| 2 | News one-liner | The event stated plainly; the news is the hook | "Anthropic just shipped a skill that turns your repo into a launch video." |
| 3 | Curiosity gap | Hint at a payoff with a concrete noun | "There's one thing inside this model that nobody mentions." |
| 4 | Contrarian | Challenge a belief the viewer holds; must be defensible | "You don't need a vector database for this." |
| 5 | Stakes / obsolescence | Something to gain or avoid | "If you still write Dockerfiles by hand, this changes your week." |
| 6 | Question they can't instantly answer | Exposes a knowledge gap | "Do you actually know what happens when you run `npx`?" |
| 7 | Pain callout | Names a specific frustration | "If your Claude Code bill doubled this month — this is why." |
| 8 | Bounded list | Promise with a finish line | "Three things this decompiler does that a human can't." |
| 9 | Analogy teaser | Promise an explanation via something familiar | "A transformer is basically a very fast librarian. Here's the trick." |
| 10 | Micro-story | Drop into a moment | "A solo dev shipped this on a Tuesday. By Friday, Google forked it." |
| 11 | Visual pattern interrupt | The frame does the work: a giant number, a 10,000-file tree collapsing into one | (text can be minimal; the picture is the hook) |

Hook killers: greetings, preambles, logo stings, music intros, vague bait with no concrete noun ("this changes everything"), over-promising, questions answerable in a second.

## Maintaining the gap (beats 3–6)

- **But/so chaining.** Each beat ends in a "but" or a "so" that creates the next question. Conflict → resolution → new conflict.
- **Stacked threads.** The hook asks *why*; the body sets up *how*; the close resolves both.
- **Foreshadow and deliver.** "The one-line fix is at the end" — then actually show it.
- **Peak in the middle.** The most surprising fact or the one dry joke sits around 55–70 % of runtime.
- **Pattern interrupt every 10–15 s.** In our style: the accent colour appearing in a monochrome frame, a full-screen number, a zoom-in, a sound cue.
- **Answer first, then prove it.** For explainers, giving the one-line answer early lowers swipe-away; viewers stay for the proof.

## CTA

One CTA per video, matched to the content:

| Content | CTA | Phrasing |
|---|---|---|
| Default (explainer) | Comment-prompt | "Comment the repo or model you want explained next." / "Which should I explain next: X or Y?" |
| "Did you know" news | Send | "Send this to the dev on your team who still does X." |
| Setup/how-to | Save | "Save this for when you set it up." |
| Part 1 of a series | Follow + next episode | "Follow — tomorrow: the security hole in this." |

Spoken CTA ≤ 3 s, paired with on-screen text, inside the final loop. Never single-word bait ("comment YES"). Pin a seeding comment within the first hour ("What should I explain Friday?") and reply to early comments.

## Captions and on-screen text

- Burned-in, word-synced (or 3–5 words at a time), one accent colour on the key term, brand font.
- Labels are labels: one idea each; two lines means it's a sentence — move it to narration.
- Say and show the exact keyword people would search ("MCP server", "KV cache", the repo name) in the first 10 s.

## Formats (recurring series)

| Format | Hook default | Typical lane |
|---|---|---|
| **How X actually works** | #1, #6, #9 | evergreen |
| **Why everyone's talking about X** | #2, #1 | hot |
| **X in 60 seconds** | #8 | either |
| **X vs Y** | #4 | evergreen |
| **You asked: X** (answers a comment) | #6, #7 | either — this is the CTA loop closing |

## Pronunciation & TTS notes

Keep `Project_Files/lexicon.json` per video for proper nouns and acronyms (e.g. "nginx" → "engine-x", "GGUF" → "G-G-U-F"). The TTS step reads it; the library keeps a global one that grows over time.

## Example (reference script — "How a vision model reads an image", 48 s)

| Beat | Narration | On screen |
|---|---|---|
| Hook | This repo got forty thousand stars in six days — and nobody could explain why. | **This repo got 40,000 stars in six days.** |
| Proof | It's called Moondream, and it's a vision model small enough to run on your laptop. | Moondream · 1.9B params · runs on a laptop |
| Mech ① | A vision model can't look at a picture. So it chops the image into two hundred and fifty-six tiny tiles — like cutting a photo into puzzle pieces. | pipeline: Image → **256 tiles** |
| Mech ② | Each tile gets turned into a number — a kind of word. So the picture becomes a sentence the language model can read. | tiles → tokens → "a sentence" |
| Peak | But here's the clever part: this one doesn't read every tile the same way. It spends more attention where the picture is busy. | heatmap on the tiles; accent on busy tiles |
| Resolution | That's why it's tiny and still accurate. It's not seeing the image — it's reading it, puzzle piece by puzzle piece. | diagram returns to frame-0 state |
| CTA | Comment the model you want explained next. | **Comment the next one ↓** |

(Illustrative — verify every number against the actual source before using any of this.)
