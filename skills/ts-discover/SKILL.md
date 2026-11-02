---
name: ts-discover
description: Find and score new-technology topics for tech_splained videos — pull candidates from the configured sources (GitHub velocity, HN, Hugging Face, arXiv, release feeds, skill marketplaces, our own comments), dedupe, score with the rubric, and write a shortlist for Kyle to approve. Use for "/ts-discover", "find topics", "what should we explain this week", or the weekly/monthly topic run.
---

# /ts-discover

Produces `pipeline/discover/shortlist-<YYYY-WW>.md` (or `-hot-<date>.md`) and updates `pipeline/discover/topics.json`. It never creates videos.

Read first: `docs/03-topic-discovery.md`, `pipeline/discover/sources.json`, the current `topics.json` (to avoid re-proposing anything `killed`, `published`, or already `shortlisted`).

## Modes

| Mode | When | Output |
|---|---|---|
| `weekly` (default) | Sunday night / Monday morning | 10 candidates, mixed lanes |
| `monthly` | Week 2 topic day | 25 evergreen candidates |
| `hot` | Any time something is moving fast | 1–3 candidates with a 48-h clock |
| `comments` | Friday | topics mined from our own comments, tagged `source: audience` |

## Steps

1. **Pull.** For each enabled source in `sources.json`, fetch the signal it defines (e.g. GitHub: repos created or pushed recently sorted by stars, star delta over 7 days; HN: front page + Show HN above the score threshold; HF: trending models/papers; feeds: new posts since last run). Record raw hits in `pipeline/discover/raw/<date>-<source>.json`.
2. **Dedupe.** Same repo/paper/model across sources = one candidate; keep every source as evidence (more sources → higher timeliness).
3. **Pre-filter.** Drop anything that fails a content boundary in `docs/01` (politics, drama, leaked assets, exploit how-tos) and anything we've published in the last 90 days unless it's a genuinely new development.
4. **Score** each candidate 1–5 on the six rubric axes in `docs/03`; compute the weighted total. Write one line of justification per axis — no bare numbers.
5. **Draft the one-sentence explanation** for every candidate scoring ≥ the shortlist threshold. If you can't write it, cap explainability at 2 and say why.
6. **Write the shortlist** (template below), ranked, with lane, format suggestion, and the two best hook archetypes from `docs/04`.
7. **Update `topics.json`**: new candidates with `status: candidate`; shortlisted ones with `status: shortlisted`, `shortlist: <file>`.
8. Tell Kyle in one paragraph: how many pulled, how many shortlisted, the top 3, anything hot with its deadline.

## Shortlist entry format

```
### 3. <Name> — <one-sentence explanation>
lane: hot (window closes ~Wed) · format: Why everyone's talking about X · score 24/30
signal: 38.9k stars in 7 days (GitHub), HN #1 for 9 h, HF trending #4
mechanism worth explaining: <2 lines>
visual primitive: pipeline (highlight: the tiling step) · analogy: puzzle pieces
hooks: #1 number+gap "…", #2 news one-liner "…"
sources: <urls>   risks: <unverified claim / licence / staleness>
```

## Rules

- Primary sources only for facts (the repo README, the paper, the release notes). Aggregators are signals, not sources.
- Never score a topic high on relevance because *you* find it interesting; the test is whether a curious non-specialist would stop scrolling.
- A trending repo with no explainable mechanism (a list, a wrapper, a UI theme) is not a topic. Say so and move on.
- Unattended runs write the shortlist and stop. Kyle picks; you don't promote anything to `briefed`.
