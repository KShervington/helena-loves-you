# 03 — Topic discovery & scoring

Evidence and full API notes (endpoints, limits, working requests): `docs/research/topic-sources.md`. Machine-readable source config: `pipeline/discover/sources.json`. Data: `pipeline/discover/topics.json` (schema in `pipeline/discover/README.md`).

## What counts as a topic

A **mechanism** worth explaining, attached to a **trigger** that makes it timely. Both are required:

| Trigger (why now) | Mechanism (what we explain) |
|---|---|
| A repo gained thousands of stars this week | How it does the thing (decompilation, clean-room reimplementation, a new inference trick) |
| A model/lab release | What's new inside it (a new attention scheme, a vision tokenizer, a training recipe) |
| A skill/plugin going viral in the coding-agent world | What the skill actually automates and how |
| A viral demo | The technique underneath the demo |
| Our own comments asking for X | Whatever X is, if it has a mechanism |

A trending repo with no explainable mechanism (a list, a wrapper, a theme, a dataset dump) is a signal that a topic *near* it is hot — not a topic.

## Sources (verified Nov 2026)

| Source | What it gives | Access | Cadence |
|---|---|---|---|
| **GitHub search API** | "new and already big": `created:>7d stars:>200 sort=stars`; "old repo shipped something": `pushed:>1d stars:>5000`; niche queries (`topic:decompilation`, `"clean room" in:readme`) | PAT; 30 req/min | daily |
| **GH Archive (BigQuery)** | ground-truth `stars_7d` from `WatchEvent` | free tier | weekly |
| **GitHub snapshot diff** | star delta for a watchlist (`topics.json` entries) | PAT | daily |
| **Hacker News (Algolia)** | front page / Show HN above a points threshold, with the discussion | none | hourly (Firebase `topstories`) + daily |
| **Hugging Face Hub** | `models?sort=trendingScore`, `/api/trending`, `/api/daily_papers` (upvotes + linked repo stars) | optional token | daily |
| **arXiv RSS** (cs.CL, cs.CV, cs.LG, cs.AI) joined with HF paper upvotes | new papers that are getting attention | none | weekly |
| **Lab feeds** (OpenAI, DeepMind, Mistral, HF blog; Anthropic via community mirror + Claude Code CHANGELOG commits) | release triggers — the lead indicator | none | hourly |
| **Newsletters** (TLDR AI, The Rundown, Ben's Bites RSS) | the lag indicator: if they covered it, it's mainstream | none | daily |
| **skills.sh / Anthropic plugin marketplaces** | viral agent skills (trending/hot views; marketplace.json diffs) | scrape / GitHub | daily |
| **Reddit** (r/LocalLLaMA, r/MachineLearning, r/programming, r/ClaudeAI) | community heat + the questions people ask | OAuth app (free tier) — verify current terms before relying on it | daily |
| **Our comments** (Reels/TikTok/Shorts) | audience requests, corrections | platform APIs | weekly |
| **YouTube Data API search** | demand check for shortlisted topics (how many videos exist, their view counts) | API key | weekly |

Dead or not worth it: Papers with Code (gone), pytrends (dead), star-history (SVG only), github.com/trending (HTML; scrape only as a cross-check), Product Hunt (API forbids commercial use).

## Velocity

Each source has its own number; normalise to a 0–5 band per source and take the max across sources (`topic-sources.md` § 10). A topic seen in ≥ 3 sources gets +0.5.

## Scoring rubric

Score 0–5 per axis with one line of justification each.

| Axis | Weight | 0 | 3 | 5 |
|---|---|---|---|---|
| Velocity | 0.25 | < 100 stars / < 50 HN pts this week | 1–3k stars/wk or HN front page | > 5k stars/wk, top-5 HF trending, or #1 skills trending |
| Timeliness | 0.15 | > 30 days, no new event | 7–14 days or a major release this week | first seen < 72 h or release < 48 h |
| Novelty | 0.15 | incremental version of something covered | new approach in a known category | new category or counter-intuitive result |
| Explainability in 60 s | 0.20 | needs background most viewers lack | one analogy gets 80 % there | one-sentence "what if" premise |
| Visualizability | 0.15 | nothing to show | a diagram or terminal demo | a clear flow / before-after / something that runs |
| General-audience relevance | 0.10 | a niche of developers | most developers | non-developers would care (phones, games, money, privacy) |

`total = Σ weight × score` (max 5). **Shortlist ≥ 3.4; auto-reject < 2.0.** Hard gates regardless of velocity: explainability ≥ 3 and visualizability ≥ 2. **Hot-lane override:** velocity 5 and timeliness 5 → goes straight to Kyle with a 48-h clock.

Evergreen candidates are scored with timeliness weight set to 0 and the remaining weights renormalised; their trigger is "people keep asking" or "this is foundational to the hot topics we've covered".

## Dedupe

Canonical keys (`github:owner/repo`, `hf:ns/name`, `arxiv:id`, `url:…`); a paper + its repo + its HF model are one topic; fuzzy-match titles for URL-less items; suppress forks/mirrors; published topics stay in the file forever so a re-surfacing one needs a *new* event to come back (as a `followup`).

## The shortlist ritual

- **Weekly (Mon):** 10 candidates, ranked, each with the one-sentence explanation, lane, format, primitive, analogy, two hooks, sources and risks. Kyle picks in ≤ 10 minutes. Picks → `shortlisted` → `/helena-script`.
- **Monthly topic day:** 25 evergreen candidates; Kyle picks 12–15 for next month's batch.
- **Hot:** any time; the shortlist entry says when the window closes.
- **Comments (Fri):** audience requests, tagged `source: audience`; these get a +0.5 relevance bump because they close the CTA loop on screen ("you asked…").

## Run plan (what the agent/scheduled task does)

| Cadence | Pull |
|---|---|
| Hourly | HN Firebase top/show scores; HF `/api/trending`; lab RSS; Claude Code CHANGELOG commits |
| Daily | GitHub search queries; HF models/papers; skills.sh trending; Reddit top-of-day; newsletter feeds; snapshot-diff the watchlist |
| Weekly | GH Archive `stars_7d` top 200; arXiv ⨝ HF upvotes; YouTube demand check for the shortlist; full score + dedupe pass; write the shortlist |

All free at this volume (BigQuery inside its free tier).

## Content boundaries (from 01)

Skip: politics, creator drama, leaked assets, exploit how-tos, anything we can't verify from a primary source, anything covered in the last 90 days without a new development.
