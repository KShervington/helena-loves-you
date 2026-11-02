# Caption pack — <topic>

Fill once; the publisher reads this file from `Docs/caption-pack.md` (YAML front matter is what the queue consumes).

```yaml
title: "How <X> actually works"            # YouTube title (≤ 70 chars), also TikTok title
hook_line: "<the on-screen hook>"           # first line of every caption
credit: "Built by <author/org> — <url>"     # mandatory when about a specific project
hashtags:
  instagram: ["#techexplained", "#ai", "#<topic>"]        # 3–5
  tiktok: ["#techtok", "#learnontiktok", "#<topic>"]       # 3–5
  youtube: ["#Shorts", "#<topic>"]                         # 2–3, in description
cta: "Comment the next thing you want explained."
cover_t: 2.4                                # seconds into the video for the cover/thumbnail
publish_at: null                            # set by the scheduler when approved
```

## Instagram caption (≤ 2,200 chars, first 125 visible)
<hook line>

<2–3 sentence plain-language summary — different wording from narration>

Credit: <author> — <url>
<CTA>

<hashtags>

## TikTok caption (≤ 2,200 chars, keep ≤ 150 for the visible part)
<hook line> <hashtags>

## YouTube description
<hook line>

<summary>
Source: <url>
Credit: <author>

<CTA>
<hashtags>
