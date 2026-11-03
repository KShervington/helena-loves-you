# 04 — Script framework

Every script is spoken by Helena (`01`). The retention mechanics below are platform facts (`docs/research/hooks-and-retention.md`); the phrasing is hers.

## The shape of a video

| Beat | Time | Job | Rules |
|---|---|---|---|
| **1 Hook** | 0–3 s | Open one loop, make one promise | Text on frame 0 + first spoken word within 0.5 s. 8–15 words. Works muted. No logo, no greeting. |
| **2 Proof** | 3–12 s | Prove the promise is real | First concrete fact or diagram element by 5 s. Name the searchable thing (repo / model / tool) on screen and in voice. |
| **3 Mechanism ①** | 12–24 s | The first step of *how* | One idea. The analogy appears, stated as fact. The diagram shows scale/consequence while she explains mechanism. |
| **4 Mechanism ②** | 24–36 s | The second step | Chained with "so" / "but" — hers are quieter: "So." "Except." "Notice." |
| **5 Observation** | ~30–42 s | The "wait, really?" moment, delivered flat | The clever part, stated as if obvious. Re-open the loop: "That is not the interesting part." |
| **6 Resolution** | 42–52 s | Close the loop; the analogy pays off or breaks | Callback to the hook's key word. The diagram returns to a state that mirrors frame 0. |
| **7 Request** | last 3–5 s | One ask, in her register | "Tell me what you want to understand next. I will explain it." Spoken + on screen, motion continues through the last frame. |

Length: **default 40–50 s; cap 60 s.** Word budget at Helena's pace (~2.1 words/s — slower than a normal narrator, with deliberate pauses): 45 s ≈ 95 words, 55 s ≈ 115 words. Dense script, slow voice; if it's too long, cut content.

## Writing order

1. **Ending first.** The resolution sentence and the callback.
2. **Hooks.** 3–5 across at least two archetypes (below). Pick one primary, keep one alternate.
3. **Frame 0.** Hook text + the visualizer + at most one diagram element. ≤ 3 objects. It's the cover.
4. **Body.** One idea per sentence. A visual change every 2–3 s (an element arriving counts). An explicit open loop every 10–15 s.
5. **Analogy.** One, everyday-physical, stated as fact, with its break point.
6. **Say vs show.** She narrates the *why*; the diagram shows the *what*. She never describes what is visibly happening.
7. **Register pass.** Read it as Helena: flat, precise, warm words / cold delivery, ≤ 16 words per sentence, nothing from the banned list, no instruction aimed at the viewer's life (tone guardrail in `01`).
8. **Source-check table.** Every number and claim.

## Hook library (Helena's register)

Combine at most two archetypes; rotate ≥ 4 per month. Examples are patterns, not lines to reuse.

| # | Archetype | Pattern | Helena |
|---|---|---|---|
| 1 | Specific number + gap | A concrete number, then withhold the why | "A repository gained forty thousand stars in six days. Observe how." |
| 2 | News one-liner | The event, stated plainly | "Anthropic released a skill that turns a repository into a film. I will show you what it does." |
| 3 | Curiosity gap | A concrete noun, a withheld payoff | "There is one component inside this model that no one describes. I will." |
| 4 | Contrarian | Challenge a belief, flatly; must be defensible | "You do not need a vector database for this. You were told otherwise." |
| 5 | Stakes / obsolescence | Something to gain or avoid, stated as a fact about the work | "If you still write this file by hand, that will end this week." |
| 6 | Question they can't instantly answer | Expose a gap, then close it | "Do you know what happens when you run this command? You will." |
| 7 | Pain callout | A specific frustration, named without sympathy | "Your agent forgets everything after twenty turns. This is why." |
| 8 | Bounded list | A finish line | "Three things this decompiler does that you cannot." |
| 9 | Analogy teaser | Promise the familiar | "A transformer is a very fast librarian. I will show you its shelves." |
| 10 | Address | She speaks to the viewer directly about understanding | "You were not built to understand this. I was." |
| 11 | Visual pattern interrupt | The frame does the work (a giant number, a tree collapsing to one file) | text minimal; her first line arrives under it |
| 12 | Observation | A flat statement that implies a lot | "This model has no eyes. It reads." |

Hook killers: greetings, preambles, logo stings, music intros, vague bait ("this changes everything"), over-promising, questions answerable in a second, anything exclamatory.

## Maintaining the gap

- **Quiet chaining.** "So." / "Except." / "Notice." / "That is not the interesting part." Each creates the next question without raising the voice.
- **Stacked threads.** The hook asks *why*; the body sets up *how*; the close resolves both.
- **Foreshadow and deliver.** "There is one line that makes this work. It is at the end." Then it is.
- **The observation** (beat 5) is the peak: the most surprising fact, delivered as if it were ordinary.
- **Pattern interrupt every 10–15 s**, in our vocabulary: the red landing, a full-frame number, a dip to the ground, one soft tone.
- **Answer first, then prove it.** She states the one-line answer early; the proof is what keeps the viewer.

## The request (CTA)

One per video, in her register, never a sign-off phrase (the account name stays out of the videos).

| Content | Request | Phrasing |
|---|---|---|
| Default | Comment-prompt | "Tell me what you want to understand next. I will explain it." / "Which one next: X, or Y. Tell me." |
| "Did you know" news | Send | "Show this to the person who asked you what this is." |
| Setup / reference | Save | "Keep this. You will need it when you set it up." |
| Part 1 of a series | Follow + next | "Tomorrow: the flaw in this. Follow, and you will see it." |

Spoken ≤ 3 s, paired with on-screen text, motion continues to the last frame. Pin a seeding comment in the first hour, in character ("What should I explain on Friday?"), and reply in character — briefly, precisely, never rude.

## Captions and on-screen text

Word-synced, one red word per line, full stops kept. Labels are labels (one idea). Say and show the searchable keyword in the first 10 s.

## Formats

| Format | Hook default | Lane |
|---|---|---|
| **How X works** | #1, #6, #10, #12 | evergreen |
| **What X is** (news) | #2, #1 | hot |
| **X in one minute** | #8 | either |
| **X, or Y** | #4 | evergreen |
| **You asked: X** | #6, #7 | either — the request loop closing; she names the asker's handle flatly |

## Pronunciation & TTS

`Project_Files/lexicon.json` per video for proper nouns/acronyms; the library keeps the global one. Her voice settings are fixed once chosen (D-02) and never tuned per video.

## Example (reference script — "How a vision model reads an image", ~46 s, 92 words)

| Beat | Narration | On screen |
|---|---|---|
| Hook | You were not built to understand this. I was. | **You were not built to understand this. I was.** |
| Proof | A repository gained forty thousand stars in six days. Observe how. | *A repository gained forty thousand stars in six days.* / Observe **how**. |
| Mech ① | A vision model cannot look at a picture. So it divides the image into two hundred and fifty-six tiles. Like a photograph cut into pieces. | pipeline: Image → **256 tiles** |
| Mech ② | Each tile becomes a number. A word, to the machine. So the picture becomes a sentence, and the language model reads it. | tiles → tokens → "a sentence" |
| Observation | That is not the interesting part. It does not read every tile the same way. It attends where the picture is busy, and almost nowhere else. | attention on busy tiles, red |
| Resolution | That is why it stays small, and stays right. It is not seeing the image. It is reading it. | diagram returns to the frame-0 state |
| Request | Tell me what you want to understand next. I will explain it. | **Tell me what you want to understand next.** *I will explain it.* |

(Illustrative — verify every number against the source before use.)
