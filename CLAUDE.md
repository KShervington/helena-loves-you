# CLAUDE.md — agent entrypoint for tech_splained

You are producing content for **tech_splained**, a faceless short-form account that explains new technology with clean animated diagrams. Read this file, then only the documents the stage needs.

## Non-negotiables

1. **Nothing publishes without Kyle's approval.** A video's `status` in `pipeline/queue/items/*.json` moves to `approved` only when Kyle sets it. The publisher refuses anything else.
2. **Every claim on screen or in narration is checked against the primary source** (the repo, paper, release notes, docs). No invented numbers. If a fact can't be verified, cut it or hedge it on screen.
3. **Credit creators.** A video about someone's repo/paper names them (on screen + caption) and links in the caption pack.
4. **Licensed audio only.** Music and SFX come from the media library (licence recorded per asset) or from sources listed in `docs/06-production-pipeline.md` § Audio.
5. **Stay inside the design system** (`docs/02-visual-design-system.md`). One accent colour per video. Text that must be read lives in the vertical safe area.
6. **Don't touch other repos' `main`.** Library additions go through a PR on `add/<project-folder-name>`.

## Which docs for which stage

| Stage | Skill | Read |
|---|---|---|
| Discover | `skills/ts-discover` | `docs/03-topic-discovery.md`, `pipeline/discover/sources.json`, current `topics.json` |
| Script | `skills/ts-script` | `docs/01-…voice.md`, `docs/04-script-framework.md`, `docs/05-visual-storytelling.md`, `templates/` |
| Produce | `skills/ts-produce` | `docs/02-visual-design-system.md`, `docs/06-production-pipeline.md`, the library `INDEX.md` |
| QA | `skills/ts-qa` | `docs/07-qa-checklist.md` |
| Publish | `skills/ts-publish` | `docs/08-publishing-scheduling.md`, `pipeline/queue/README.md` |
| Review | `skills/ts-review` | `docs/09-analytics-iteration.md` |

## Project folders

One folder per video in the working directory: `YYYY-MM-DD_Topic-Slug/` with `Assets/ Docs/ Exports/ Project_Files/ Raw_Footage/` (same convention as Kyle's promo videos). `templates/video-README.md` says what goes where. Scratch work stays outside the project folder.

## Working style

- Draft the hook first; if the hook isn't good, the topic isn't ready.
- Prefer one idea per frame. If a frame needs a paragraph, it's two frames.
- Before a full render, look at stills from every scene and mid-transition.
- Log anything you decided that the docs didn't cover in `docs/10-decision-log.md` under "Agent notes", so it can be promoted into an SOP later.
