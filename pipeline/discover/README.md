# pipeline/discover

| File | What |
|---|---|
| `sources.json` | Every source `/helena-discover` pulls from: request, auth env var, how its number maps to the velocity band, cadence, enabled flag |
| `topics.json` | The topic store (schema below). Status before a video exists lives here; from `produced` onward, `../queue/items/<slug>.json` is the source of truth |
| `topics-archive.jsonl` | `published` / `killed` topics older than 90 days, one per line |
| `raw/` | Raw pulls per run (`<date>-<source>.json`), gitignored |
| `shortlist-YYYY-WW.md`, `shortlist-hot-YYYY-MM-DD.md`, `shortlist-monthly-YYYY-MM.md` | What Kyle approves from |

## `topics.json` schema

```jsonc
{
  "version": 1,
  "generated_at": "2026-11-01T12:00:00Z",
  "topics": [{
    "id": "github:owner/repo",                 // canonical key: github:owner/repo | hf:ns/name | arxiv:id | url:host/path | request:text
    "aliases": ["url:github.com/owner/repo", "hn:46012345"],
    "title": "repo",
    "one_liner": "What it is in one plain sentence.",
    "category": "dev-tool | model | paper | skill | decomp | clean-room | infra | other",
    "tags": ["cli", "llm"],
    "first_seen_at": "…", "last_updated_at": "…",
    "status": "candidate | shortlisted | briefed | scripted | storyboarded | killed | stale",   // later statuses live in queue/items/
    "lane": "evergreen | hot",
    "signals": [ { "source": "github_search_new", "observed_at": "…", "metrics": { "stars": 4957 }, "url": "…" } ],   // append-only
    "velocity": { "stars_7d": 4950, "hn_points": 412, "hf_trending_rank": null, "skills_installs_7d": null, "sources_count": 2 },
    "scores": { "velocity": 5, "timeliness": 5, "novelty": 3, "explainability": 4, "visualizability": 3, "relevance": 3,
                "total": 3.95, "scored_at": "…", "justification": { "explainability": "one analogy (a spell-checker for tone) gets 80% there", "…": "…" } },
    "credit": { "author": "owner", "url": "https://github.com/owner/repo" },
    "shortlist": "shortlist-2026-45.md",
    "project_folder": null,                      // set by /helena-script
    "notes": "hook idea…",
    "history": [ { "at": "…", "event": "created | scored | shortlisted | approved | killed", "by": "helena-discover | kyle" } ]
  }]
}
```

Rules: `signals[]` is append-only (prune > 30 days for non-published); `velocity`/`scores` are overwritten each run; keep under ~500 live topics; published topics keep their aliases forever so re-surfacing needs a new event.

## Status

No pull code is written yet — `sources.json` + the skill are the spec. First implementation step: a small Node or Python runner (`discover.mjs`) that executes each enabled source, writes `raw/`, dedupes into `topics.json`, and leaves scoring to the agent (scores need judgement, pulls don't).
