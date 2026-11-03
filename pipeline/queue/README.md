# pipeline/queue

One JSON file per video in `items/<slug>.json` (so approval PRs never conflict) is the source of truth for every video from `produced` onward; `_example.json` shows the shape. `/helena-produce` appends, `/helena-qa` and Kyle change status, `/helena-publish` reads and records results. Publishing logic and the approval gate are described in `docs/08-publishing-scheduling.md`.

## Entry schema

```jsonc
{
    "slug": "2026-11-12_Moondream-Tiles",
    "topic_id": "github:vikhyat/moondream",
    "lane": "evergreen",
    "format": "How X actually works",
    "status": "produced | qa_passed | ready_for_review | changes_requested | approved | scheduled | published | failed | killed",
    "status_by": "helena-produce | helena-qa | kyle | helena-publish",
    "status_at": "2026-11-12T18:02:00Z",
    "review_note": "",                                   // Kyle's one-liner on changes_requested
    "files": {
      "video": "2026-11-12_Moondream-Tiles/Exports/2026-11-12_Moondream-Tiles_1080x1920.mp4",
      "poster": "…/Exports/2026-11-12_Moondream-Tiles_poster.jpg",
      "textless": "…/Raw_Footage/…_textless_1080x1920.mp4",
      "caption_pack": "…/Docs/caption-pack.md",
      "sha256": "…"                                      // of the mp4; the publisher refuses a file whose hash changed after approval
    },
    "meta": { "duration_s": 48.2, "direction": "instrument", "voice": "elevenlabs/eleven_v4/<voice>", "music": "music-lab-bed-01", "hook_archetype": "number+gap", "length_bucket": "45-50" },
    "publish_at": "2026-12-03T16:30:00Z",               // UTC; null until scheduled
    "public_url": null,                                  // where the mp4 is hosted for pull-based platforms, set by the publisher
    "platforms": {
      "instagram": { "id": null, "url": null, "posted_at": null, "attempts": 0, "error": null },
      "tiktok":    { "id": null, "url": null, "posted_at": null, "attempts": 0, "error": null },
      "youtube":   { "id": null, "url": null, "posted_at": null, "attempts": 0, "error": null }
    },
    "followups": { "pinned_comment": false, "first_hour_replies": false },
    "history": [ { "at": "…", "event": "produced", "by": "helena-produce" }, { "at": "…", "event": "approved", "by": "kyle" } ]
}
```

## Status rules

- `status` also has `publishing`, `partial` (some platforms done) — set by the publisher.
- Only **Kyle** sets `approved` (and `changes_requested` / `killed`). Agents set everything else.
- `approved` requires `qa_passed` in history and a `sha256`. Any later change to the file resets the entry to `produced`.
- `scheduled` = `approved` + `publish_at`. `/helena-publish --schedule-month` assigns slots; Kyle can edit dates by hand.
- The publisher processes an entry when `status ∈ {approved, scheduled}` and `publish_at ≤ now` (or `--slot` names it). It writes each platform's `id` the moment the platform returns one — idempotency depends on this.
- `failed` is per platform; the entry stays `published` if ≥ 1 platform succeeded, with the failed platform flagged for retry/manual action.

## Approval UX (no new tooling)

Kyle approves by merging the PR that sets `status: approved` in the item file (the review-week default: one PR per batch, the diff *is* the approval record), or by replying "approve <slug>" / "changes <slug>: <note>" in the chat where the agent reports — the agent then edits the file and records `status_by: kyle`. Either way the commit history is the audit trail.
