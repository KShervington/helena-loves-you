---
name: helena-review
description: Weekly helena_loves_you performance review — pull per-video metrics from the three platforms, compare hook archetypes, lengths and directions, mine comments for topic requests, and propose edits to the hook library, scoring rubric and cadence as a PR. Use for "/helena-review", "how did this week do", or the Friday scheduled run.
---

# /helena-review [--week YYYY-WW]

Read first: `docs/09-analytics-iteration.md`, `pipeline/queue/items/*.json`, last week's `docs/reviews/`.

## Steps

1. **Pull metrics** for every video published in the window (and update the trailing 28-day numbers for older ones): per platform — views/plays, reach, 3-s retention or VVSA, average watch %, completion, replays, likes, comments, shares/sends, saves, follows gained. Store raw in `pipeline/analytics/<YYYY-WW>.json`; the review reads from there.
2. **Compute the derived metrics** in `docs/09` (sends/reach, hook hold, mid-drop time, completion by length bucket, by hook archetype, by direction, by lane).
3. **Comments**: collect, classify (topic request / correction / question / noise). Corrections go to the video's `Docs/errata.md` and, if material, a pinned correction comment is proposed. Topic requests go to `topics.json` as `source: audience`.
4. **Write `docs/reviews/<YYYY-WW>.md`**: the table, three bullets of what worked, three of what didn't, the steepest-drop timestamp for each video with a hypothesis, and the experiments running (A/B hooks, lengths, directions) with their current read.
5. **Propose changes** as a branch `review/<YYYY-WW>` touching only `docs/04` (hook library notes), `docs/03` (rubric weights), `docs/00` (cadence) and `docs/10` (decision log). Kyle merges.
6. Report: the three numbers that matter this week, the one change you'd make, and what the comments are asking for.

Don't draw conclusions from fewer than ~5 videos per bucket; say "not enough data" instead.
