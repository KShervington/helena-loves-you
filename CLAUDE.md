# CLAUDE.md — agent entrypoint for helena_loves_you

You are producing content for **helena_loves_you**, a short-form account where Helena — a synthetic human with no personality who says things a person with one would say — explains new technology with clean animated diagrams. Videos are faceless: her voice, her register and the voice visualizer are her presence. Read this file, then only the documents the stage needs.

## Non-negotiables

1. **Nothing publishes without Kyle's approval.** A video's `status` in `pipeline/queue/items/*.json` moves to `approved` only when Kyle sets it. The publisher refuses anything else.
2. **Every claim on screen or in narration is checked against the primary source** (the repo, paper, release notes, docs). No invented numbers. If a fact can't be verified, cut it or hedge it on screen.
3. **Credit creators.** A video about someone's repo/paper names them (on screen + caption) and links in the caption pack.
4. **Licensed audio only.** Music and SFX come from the media library (licence recorded per asset) or from sources listed in `docs/06-production-pipeline.md` § Audio.
5. **Stay inside the design system** (`docs/02-visual-design-system.md`): one red idea per frame, centred, slow and flat. Text that must be read lives in the vertical safe area.
6. **Stay inside her voice** (`docs/01`): flat, precise, warm words / cold delivery. The tone guardrail is absolute — her perfectionism is aimed at systems, never at the viewer. The account name is never said or shown in a video; no image of Helena ever appears in one.
7. **Don't touch other repos' `main`.** Library additions go through a PR on `add/<project-folder-name>`.

## Which docs for which stage

| Stage | Skill | Read |
|---|---|---|
| Discover | `skills/helena-discover` | `docs/03-topic-discovery.md`, `pipeline/discover/sources.json`, current `topics.json` |
| Script | `skills/helena-script` | `docs/01-…voice.md`, `docs/04-script-framework.md`, `docs/05-visual-storytelling.md`, `templates/` |
| Produce | `skills/helena-produce` | `docs/02-visual-design-system.md`, `docs/06-production-pipeline.md`, the library `INDEX.md` |
| QA | `skills/helena-qa` | `docs/07-qa-checklist.md` |
| Publish | `skills/helena-publish` | `docs/08-publishing-scheduling.md`, `pipeline/queue/README.md` |
| Review | `skills/helena-review` | `docs/09-analytics-iteration.md` |

## Project folders

One folder per video in the working directory: `YYYY-MM-DD_Topic-Slug/` with `Assets/ Docs/ Exports/ Project_Files/ Raw_Footage/` (same convention as Kyle's promo videos). `templates/video-README.md` says what goes where. Scratch work stays outside the project folder.

## Working style

- Draft the hook first; if the hook isn't good, the topic isn't ready.
- Prefer one idea per frame. If a frame needs a paragraph, it's two frames.
- Before a full render, look at stills from every scene and mid-transition.
- Log anything you decided that the docs didn't cover in `docs/10-decision-log.md` under "Agent notes", so it can be promoted into an SOP later.
