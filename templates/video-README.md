# <YYYY-MM-DD_Topic-Slug>

| | |
|---|---|
| Lane | evergreen / hot |
| Status | see `pipeline/queue/items/<slug>.json` |
| Duration | <s> |
| Voice | <TTS provider + voice id> |
| Music | <library id or source + licence> · window <start–end s> |
| Library assets used | <ids @ library commit> |
| Design direction | <id from 02> · accent <hex> |

## Folder

```
Assets/         custom + reused assets as reusable files (Graphics/, Audio/, Brand/, Fonts/)
Docs/           brief.md, script.md, shot-list.md, caption-pack.md, qa.md, library-candidates.md, this README
Exports/        <slug>_1080x1920.mp4 (poster baked as frame 0) + <slug>_poster.jpg
Project_Files/  comp.html, narration.json (word timestamps), render.sh, tools
Raw_Footage/    <slug>_textless_1080x1920.mp4 + untouched source media
```

## Re-render

```bash
cd Project_Files && bash render.sh
```

## Illustrative values

List any on-screen numbers that are illustrative rather than measured.
