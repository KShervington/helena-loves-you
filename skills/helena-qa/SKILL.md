---
name: helena-qa
description: Run the helena_loves_you QA gate on a produced video folder — automated file/audio checks plus a frame-by-frame readability, accuracy and design-system review — and write Docs/qa.md with pass/fail per rule. Use for "/helena-qa <folder>", "check this video", or automatically at the end of /helena-produce.
---

# /helena-qa <project folder>

Read `docs/07-qa-checklist.md` and apply every line. Output `Docs/qa.md`:

```
# QA — <slug> — <date>
Result: PASS | FAIL (n blocking)
| Section | Rule | Result | Note |
...
Weakest second: <t> — <why>
```

## Steps

1. **Automated** (section G): ffprobe the export (codec, size, fps, duration), loudnorm analysis (LUFS, true peak), file presence per section F, caption-pack front matter parses, `narration.json` is not a stub.
2. **Stills**: capture frame 0, every scene boundary, mid-transitions, and the three busiest frames. Check safe area, fonts, contrast (compute it for caption text vs the sampled background), one-accent rule, element counts.
3. **Sync**: pick three narration words (start/middle/end) and compare the audio onset (from `narration.json` against the wav) to the frame in which the caption word turns accent; drift ≤ 100 ms.
4. **Accuracy**: open `Docs/script.md`'s source-check table; spot-verify every number that appears on screen against its cited source location.
5. **Human-style watch**: describe the video from stills alone (muted test); then with the narration. Name the weakest second.
6. Set the queue status: `qa_passed` → `ready_for_review`, or `changes_requested` with the failing lines quoted.

Never soften a blocking fail into a note. If unsure whether something blocks, it blocks.
