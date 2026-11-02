# 09 — Analytics & iteration

The point of measuring is to change three things: which topics we pick (03), how we hook and structure (04), and how long/what look we ship (02/04). Everything else is vanity.

## What to pull (per video, per platform)

| Metric | Instagram Reels | TikTok | YouTube Shorts | Why |
|---|---|---|---|---|
| Plays / views, reach | insights API | video analytics | Analytics API | denominator |
| **3-s hold / "viewed vs swiped away"** | retention curve (where available) | 3-s retention | VVSA (target ≥ 75 %) | the hook |
| Average watch %, completion | ✓ | ✓ | ✓ | the body |
| Retention curve → **steepest-drop timestamp** | ✓ (where exposed) | ✓ | ✓ | which 5 s to fix |
| Replays | plays/reach > 1.3 | rewatch rate | replays count as views | loop quality |
| **Sends / shares per reach** | primary non-follower signal (≥ 1 % strong) | shares | shares | distribution |
| Saves | ✓ | ✓ | – | reference value |
| Comments (count + text) | ✓ | ✓ | ✓ | CTA loop + corrections |
| Follows gained from the video | ✓ | ✓ | ✓ (subs) | compounding |

Raw pulls go to `pipeline/analytics/<YYYY-WW>.json`; a flat `pipeline/analytics/videos.csv` (one row per video × platform × snapshot at 24 h / 7 d / 28 d) is what the review reads.

## Derived views (the weekly table)

Group by each of: **hook archetype**, **length bucket** (30–40 / 40–50 / 50–60), **format**, **lane**, **direction** (while the aesthetic test runs), **CTA type**, **posting slot**. Report median 3-s hold, completion, sends/reach, comments/reach. Don't conclude anything from < 5 videos per bucket — write "n/a (n=3)".

## The weekly review (Fri, `/ts-review`)

1. The table.
2. Per video: the steepest-drop timestamp and a one-line hypothesis (hook over-promised? body stalled at the second mechanism? caption too dense?). Fix the five seconds before the drop in the next similar video.
3. Three things that worked, three that didn't.
4. Comment mining: topic requests → `topics.json` (`source: audience`); corrections → `Docs/errata.md` and, if material, a pinned correction.
5. Experiments in flight and their current read (A/B hooks, tight vs deep length, aesthetic directions).
6. Proposed changes as a PR touching only 00/03/04/10.

## Standing experiments (first 90 days)

| Experiment | Design | Decision metric | Decide after |
|---|---|---|---|
| Hook archetypes | rotate ≥ 4 archetypes/month; paired topics get different archetypes | 3-s hold, completion | 20 videos |
| Length | 2 tight (30–40 s) vs 2 deep (50–60 s) per week on comparable topics | completion × reach | 16 videos |
| Aesthetic direction | 2 videos per finalist direction (02 § test) | 3-s hold, completion, sends | 6 videos |
| CTA | comment-prompt vs send-to-a-person on Reels | comments/reach vs sends/reach | 12 videos |
| Posting slot | 11:00–13:00 ET vs 18:00–20:00 ET | 24-h reach | 4 weeks |
| Caption style | phrase lines vs word-by-word in the hook | 3-s hold | 12 videos |

## Platform-level health (monthly)

Follower growth per platform, share of reach from non-followers, which formats/series get follows, total minutes watched. If one platform is clearly carrying the account, adapt the native versions there first (title/caption/cover), not the video.

## Feedback into the system

- Hook library (`04`): annotate each archetype with its running median 3-s hold; retire ones that trail for two months.
- Rubric (`03`): if "visualizability 2" topics consistently under-perform, raise the gate to 3. If audience-requested topics over-perform, raise their bump.
- Cadence (`00`): if hot-lane videos outperform by > 1.5× on reach, shift to 3 hot / 2 evergreen.
- Design (`02`): the aesthetic test ends with a decision in `10`.
