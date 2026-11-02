# 00 — Cadence & operating rhythm

**Goal:** one video posted per workday (Mon–Fri) on Reels, TikTok and Shorts, without producing one video per day.

## Two lanes, one queue

| Lane | Share | What | Produced when | Lead time |
|---|---|---|---|---|
| **Evergreen** | ~3/week | "How X actually works" — mechanisms that stay true for months (how diffusion models denoise, what a KV cache is, how a decompiler reconstructs code, what a clean-room implementation is) | In batch, mid-month, for the following month | 2–6 weeks |
| **Hot** | ~2/week | Something that just happened: a repo going vertical, a model release, a skill going viral | One at a time, within 48 h of the trigger | 0–2 days |

The evergreen bank should always hold **≥ 8 approved, unpublished videos**. That's the buffer that makes a hot slot optional rather than mandatory: if nothing hot happens in a week, evergreen fills all five days.

Hot topics that miss their window don't die — if the mechanism is interesting, they become evergreen candidates with a less time-bound hook.

## Weekly rhythm (Kyle, ~2–3 h/week outside batch days)

| Day | Kyle | Agent |
|---|---|---|
| Mon | Approve this week's shortlist (10 min). Decide whether a hot slot fires. | `/ts-discover` ran over the weekend → shortlist waiting. Publisher posts the day's queued video. |
| Tue–Thu | Review any hot-lane draft (15 min each): script first, then render. | Hot lane: brief → script → produce → QA → mark `ready_for_review`. Publisher posts daily. |
| Fri | 20-min review: last week's numbers, hook winners, comment-mined topics. | `/ts-review` drafts the weekly review; proposes rubric/hook-library edits as a PR. |

## Monthly rhythm

| When | What |
|---|---|
| Week 2, day 1 | **Topic day.** Agent produces a 25-candidate evergreen shortlist (scored); Kyle picks 12–15. |
| Week 2, days 2–4 | **Script batch.** Agent writes all briefs + scripts + shot lists. Kyle reviews scripts in one sitting (scripts are cheap to fix; renders are not). |
| Week 3 | **Render batch.** Agent produces, self-QAs, and marks `ready_for_review`. Kyle watches each once, approves or kicks back with one line of notes. |
| Week 3, end | Approved videos get `publish_at` dates for next month's evergreen slots. |
| Week 4 | Slack: hot lane only, library upkeep, analytics deep-dive. |

## Status model (one video)

```
candidate → shortlisted → briefed → scripted → storyboarded → produced → qa_passed
  → ready_for_review → approved → scheduled → published → reviewed
                 ↘ changes_requested (loops back to the stage named in the note)
                 ↘ killed (with a one-line reason, kept for the record)
```

`pipeline/queue/items/*.json` is the single source of truth for status from `produced` onward; `pipeline/discover/topics.json` for everything before.

## Time budget per video (target, agent-run)

| Stage | Target | Notes |
|---|---|---|
| Brief + script | 20–30 min | includes source verification |
| Storyboard | 10 min | one primitive per beat |
| Produce | 30–60 min | TTS, composition, stills check, render |
| QA | 10 min | automated checks + a human-style watch |
| Kyle's review | 5 min | script 2 min + video 3 min |

If a video blows through 2× its budget, stop and log why in the decision log — it's usually a sign the topic is a two-parter or the visual primitive is wrong.
