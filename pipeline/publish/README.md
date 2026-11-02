# pipeline/publish

Implementation home for the self-built publisher described in `docs/08-publishing-scheduling.md`. **Nothing is coded yet**; this is the build order.

| # | Piece | Notes |
|---|---|---|
| 1 | `r2-upload.mjs` | S3-compatible PUT of `Exports/*.mp4` + poster to `media.<domain>/yyyy/mm/<slug>.*`; prints URLs + sha256 for the queue item |
| 2 | `queue-item.mjs` | writes `pipeline/queue/items/<slug>.json` from a project folder's caption pack + export; opens the approval PR with the preview link |
| 3 | `publish.mjs` | the Actions entrypoint: load approved/scheduled items due now → pre-flight → Instagram → TikTok inbox → (YouTube already uploaded at approval) → commit results. Idempotent via persisted ids; `concurrency: publish` |
| 4 | `youtube-schedule.mjs` | runs on approval: resumable upload, `private` + `publishAt` |
| 5 | `tokens.mjs` | daily refresh/test for IG, TikTok, Google; secrets age-encrypted in `secrets/tokens.enc.json` |
| 6 | `.github/workflows/publish.yml`, `tokens.yml`, `pr-check.yml` | cron `7,22,37,52 * * * *` + dispatch; daily tokens; ffprobe + caption-lint on PRs |
| 7 | dead-man switch | a daily Claude scheduled task (or healthchecks.io ping) that alerts if the cron hasn't run in 2 h |

Secrets never live in this repo unencrypted. The publisher refuses any item whose `status` isn't `approved`/`scheduled` or whose file hash changed after approval.
