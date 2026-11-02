---
name: ts-publish
description: Publish approved tech_splained videos from the queue to Instagram Reels, TikTok and YouTube Shorts with per-platform captions, then record results — or schedule them by assigning publish slots. Refuses anything not approved by Kyle. Use for "/ts-publish", "post today's video", "schedule next month", or the daily scheduled run.
---

# /ts-publish [--slot YYYY-MM-DD | --dry-run | --schedule-month YYYY-MM]

Read first: `docs/08-publishing-scheduling.md`, `pipeline/queue/README.md`, `pipeline/queue/items/*.json`.

## Hard rules

1. Only entries with `status: approved` (set by Kyle) or `scheduled` whose `publish_at` ≤ now are eligible. Anything else: skip and say so.
2. Idempotent: before posting to a platform, check `platforms.<name>.id` is empty; after posting, write the returned id and timestamp immediately. A crash mid-run must never cause a double post.
3. Native upload of the clean master to each platform; never cross-share from one app to another.
4. Dry-run by default when invoked by a human without `--slot`; the scheduled task passes `--slot today`.

## Steps (per eligible entry)

1. Resolve the export and caption pack from the project folder; validate the front matter.
2. Make the MP4 reachable at a public URL if the platform needs one (per `docs/08`), or upload directly where the API accepts bytes.
3. Instagram Reels → TikTok → YouTube Shorts, in that order, each with its own caption/title/hashtags/cover from the pack. Poll until each platform reports the post as live.
4. Pin the seeding comment where the API allows; otherwise add it to the "manual follow-ups" list in the report.
5. Update the queue entry: `status: published`, per-platform ids/URLs, `published_at`.
6. On failure: retry per the policy in `docs/08`; after the last retry mark that platform `failed` with the error, leave the others as they are, and flag it in the report. Never move on to the next day's video to "make up" a slot.

## `--schedule-month`

Assign `publish_at` to approved evergreen videos for every workday of the month that doesn't already have one, leaving the hot-lane days configured in `docs/00` open; write the plan to `pipeline/queue/calendar-YYYY-MM.md` for Kyle to glance at.

## Report

One paragraph: what was posted where (with links), what's queued for tomorrow, any failures, and the manual follow-ups (pinned comments, first-hour replies).
