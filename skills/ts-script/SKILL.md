---
name: ts-script
description: Turn an approved tech_splained topic into a verified brief, a timed script (hook, gap, analogy, CTA) and a shot list mapped to diagram primitives, inside a new dated project folder. Use for "/ts-script <topic>", "write the script for…", or after Kyle approves a shortlist.
---

# /ts-script <topic or topics.json id>

Creates `YYYY-MM-DD_Topic-Slug/` with `Docs/brief.md`, `Docs/script.md`, `Docs/shot-list.md`, `Docs/caption-pack.md`, `Project_Files/script.txt`, `Project_Files/lexicon.json`, and sets the topic to `scripted` (then `storyboarded`) in `topics.json`.

Read first: `docs/01-brand-audience-voice.md`, `docs/04-script-framework.md`, `docs/05-visual-storytelling.md`, and `templates/`.

## Steps

1. **Research the primary source.** Read the repo README/code, paper, or release notes directly. Extract the 3–5 mechanism bullets and cite their location. Note author/org for credit. If the source contradicts the shortlist's claim, stop and say so.
2. **Brief** (`templates/topic-brief.md`): one-sentence explanation, mechanism bullets, the gap, candidate analogy with its break point, the visual primitive and its highlighted element, 3 hooks across ≥ 2 archetypes, risks.
3. **Write the ending first**: payoff sentence + callback line.
4. **Script** (`templates/script.md`): fill all seven beats; narration 100–135 words; "but/so" chaining; a re-hook in beat 5; one CTA from the table in `docs/04`; on-screen text ≤ 8 words/line. Fill the **source-check table** — every number and claim.
5. **Voice pass.** Read it aloud in your head at ~2.4 words/s. Cut filler, split any sentence over ~18 words, remove banned words (`docs/01`). Make sure the searchable keyword is spoken and shown in the first 10 s.
6. **Shot list** (`templates/shot-list.md`): per beat — primitive id, reveal order, the narration word that triggers each reveal, the highlighted element, transition in, caption lines with accent words, what persists into the next beat. Choose the poster moment.
7. **Caption pack** (`templates/caption-pack.md`): title, per-platform captions, credit line, hashtags per the limits in `docs/08`, `cover_t`.
8. **`Project_Files/script.txt`**: narration only, beats separated by blank lines with `# beat-id` markers (this is the TTS input). **`lexicon.json`**: pronunciations for proper nouns/acronyms.
9. Run `python3 <library>/assets/tools/narration/stub-narration.py Project_Files/script.txt Project_Files/narration.json` to get estimated timings; sanity-check that the total is 40–60 s. If not, cut (don't speed up).
10. Report: the hook, the one-sentence explanation, estimated length, and the two things you were least sure about. Hot lane: say what the 48-h deadline is.

## Rules

- Do not invent numbers to make a hook punchier. If the real number is unimpressive, change the hook archetype.
- One analogy per video, and it must be stated where it breaks.
- Never narrate what the diagram will visibly show; narrate the why.
- If the topic turns out to be two ideas, write a two-parter and say so; don't cram.
