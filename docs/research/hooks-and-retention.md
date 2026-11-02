# Hooks, Retention, CTAs and Format Conventions for Short-Form Tech Explainers (2025–2026)

Research compiled 2026-11-01 for the tech_splained account: faceless 45–60s explainers (AI models, viral GitHub repos, dev tools) with clean diagram visuals and AI voiceover, posted to Instagram Reels, TikTok and YouTube Shorts, 5 days/week.

**How to read the confidence labels used below**

| Label | Meaning |
|---|---|
| OFFICIAL | Platform documentation or a named platform executive (Mosseri, YouTube Help, TikTok Newsroom / Community Guidelines) |
| STUDY | A named dataset with a stated sample size (Metricool, Sprout, Buffer, Paddy Galloway) |
| PRACTITIONER | A working creator describing their own method (Jenny Hoyos, Cleo Abram) |
| VENDOR | Tool-company blog with no cited methodology; useful as a heuristic, not as a fact |

Most of the "2026 algorithm" content online is VENDOR-grade. Where numbers below are vendor-sourced they are marked as such and should be treated as starting hypotheses to validate against your own analytics.

---

## 1. Hook patterns (first 1–3 seconds)

### 1.1 Why the hook dominates

- YouTube Shorts shows every new Short to a feed test audience and reads early behavior; the key metric in Studio is "Viewed vs. Swiped Away" (VVSA). Paddy Galloway's analysis of 3.3B Shorts views found 70–90% VVSA on the top performers; under 60% means distribution gets pulled; under 50% means the hook is broken. Aim for 75%+ (STUDY via VENDOR summary).
- Vendor-reported scroll decision time: roughly 1.4s on Reels, 1.7s on TikTok, 2.3s on Shorts (VENDOR, uncited). Treat as "you have under 2 seconds."
- Mosseri: roughly half of Reels impressions play with sound off, so the first frame must be a visual hook and the hook must work muted (OFFICIAL, Colin & Samir interview, June 2024). Other vendor estimates put sound-off at 54% (Reels) to 68% (TikTok) (VENDOR).
- Shorts with an immediate hook in the first 2 seconds retain about 19% more viewers (Zebracat 2025, VENDOR).

### 1.2 Hook taxonomy with example phrasings for tech explainers

Each hook should open ONE loop that the video closes. Combine at most two types (e.g., number + curiosity gap). Keep the spoken hook to 8–15 words, landing within 3 seconds, first word spoken within ~0.5s of frame one.

| # | Pattern | Mechanism | Example phrasing (tech explainer) | Fit for tech_splained |
|---|---|---|---|---|
| 1 | **Curiosity gap** | Hint at a payoff, withhold it | "This 400-line repo does what a $20/month tool does." / "There's one thing nobody mentions about MCP servers." | Most consistent performer across platforms (VENDOR: ~68% 3s retention). Default choice. |
| 2 | **Contrarian / bold claim** | Challenge a belief the viewer holds | "RAG is mostly dead, and this is what replaced it." / "You don't need a vector database for this." | Strong for dev audiences who like to argue; drives comments. Must be defensible or drop-off follows. |
| 3 | **Stakes / obsolescence** | Something to gain or avoid | "If you still write Dockerfiles by hand, watch this." / "This model just made half your prompt engineering useless." | Very good for "new model/tool" news. Pair with a specific. |
| 4 | **Specific number** | Concreteness signals real information | "47,000 GitHub stars in 9 days." / "3 lines of config. Zero servers." | Ideal first-frame text. Numbers big enough to fill the screen act as a visual pattern interrupt. |
| 5 | **"Nobody is talking about"** | Scarcity of information | "Everyone's covering the new model. Nobody's covering the thing inside it." | Works, but overused in 2026; only use when literally true. |
| 6 | **Direct question the viewer cannot instantly answer** | Exposes a knowledge gap | "Do you actually know what happens when you run `npx`?" / "Why does your agent forget everything after 20 turns?" | Good for fundamentals. Avoid questions answerable in one second (kills tension). |
| 7 | **Direct callout / pain point** | Names the viewer's frustration | "If your Claude Code bill doubled this month, this is why." | High watch-time lift when the pain is specific (VENDOR: ~34% lift vs generic openers). |
| 8 | **Listicle promise** | Bounded payoff with a finish line | "3 things this repo does that your IDE can't." | Gives a built-in retention structure (viewer waits for #3). |
| 9 | **News one-liner** | Newsworthy event stated plainly | "NASA just regained contact with its most distant spacecraft." (Cleo Abram's style) → "OpenAI just open-sourced something it said it never would." | Best for day-of releases. No clickbait needed; the news is the hook. |
| 10 | **Analogy teaser** | Promise an explanation through something familiar | "A transformer is basically a very fast librarian. Here's the trick." | Fits the 3Blue1Brown-style analogy brand. |
| 11 | **Visual pattern interrupt** | Break feed rhythm visually | A single giant number, a before/after diagram already on screen, a "wait, what?" visual (e.g., a 10,000-file tree collapsing into 1 file). | Mandatory for faceless accounts: no face means the frame must do the work. |
| 12 | **Story cold open / micro-story** | Drop into a moment | "A solo dev shipped this on a Tuesday. By Friday, Google forked it." | Good variety hook; use sparingly. |

### 1.3 Text-on-screen vs spoken hook

- Use both, always. Text overlay mirrors (but does not have to duplicate verbatim) the spoken hook. Text appears on frame one, not after a delay.
- First frame rules (Jenny Hoyos, PRACTITIONER): readable on mute, centered composition, no more than three objects in frame, strong enough to serve as a thumbnail.
- Platform nuance (VENDOR): TikTok weights the first spoken words heavily alongside on-screen text; Instagram leans visual, so the frame must work silently; Shorts tolerates slightly more setup.
- Faceless accounts specifically: no personality recognition, so rely on text overlay + a visually distinctive first frame + a sound cue. Vendor data: 40% of underperforming videos had hooks that failed on mute; fixing that improved them ~2x (VENDOR, uncited).

### 1.4 Hook mistakes that kill distribution

- "In this video I'll show you..." or any greeting/preamble.
- Logo sting, music intro or slow zoom on a static frame before speech.
- Vague curiosity bait with no concrete noun ("this changes everything").
- Over-promising: unrealistic hooks spike early retention and then crater at the payoff.
- A question the viewer can answer instantly.

### 1.5 Hook testing loop

- Write 3–5 hooks per script; pick one primary, keep one alternate.
- Publish two similar videos in the same week with different hook types; compare VVSA (Shorts), 3-second retention (TikTok analytics), and plays/reach (Reels).
- Rotate at least four hook archetypes across a month to avoid "hook decay" (audience learns the pattern).
- Replicate the winner for the next 3–5 videos, then test again.

---

## 2. Retention structure

### 2.1 Timestamp blueprint for a 45–60s explainer

| Segment | Time | Job | Notes |
|---|---|---|---|
| Hook | 0–3s | Open one loop, make one promise | Text + voice + distinctive frame. Full "hook arc" may run to 5–6s. |
| Investment window | 3–15s | Prove the promise is real | First concrete fact or visual within 5s. No channel intro, no "before we start." TikTok sub-30s completion below 40% almost always means a leak here (VENDOR). |
| Payoff zone | 15s–~80% | Deliver in steps; one idea per sentence | Place the strongest insight inside the first 30% of the body. Re-hook every 10–15s. |
| Peak | around the middle | A surprising fact, a joke, a "wait, really?" visual | Hoyos cites peak-end theory: a mid-video peak lifts remembered quality. |
| Close | last 10–15% | Resolve the loop, callback to the hook, CTA | No "thanks for watching," no fade to black. |

### 2.2 Re-hooks and open loops (how to "maintain the gap")

- Insert a small open loop every 10–15 seconds: "but that's not the clever part," "and this is where it gets weird," "the second thing is what actually matters."
- Stack two or three unresolved threads that converge at the end (e.g., hook asks WHY, body sets up HOW, close resolves both).
- Chain beats with "but" / "so" instead of "and" (Hoyos). Conflict → resolution → new conflict. Every "but" creates a new question.
- Foreshadow the payoff explicitly ("I'll show you the one-line fix at the end") and then actually deliver it. Hoyos calls foreshadowing the most underrated hook element.
- Dual narrative (Hoyos): voiceover carries one thread while visuals carry context, so nothing is stated that could be shown. For a diagram-driven account this is the core craft: narration explains the mechanism while the diagram shows the scale/consequence.
- Answer-first structure (TikTok practitioners): give the one-line answer, then prove it. Explainer audiences stay for the proof, and the early answer lowers swipe-away.

### 2.3 Pacing and density

- Visual change every 2–3 seconds (cut, zoom, new label appearing, diagram step). For a diagram style, "change" can be a new element animating in rather than a hard cut.
- At least one deliberate pattern interrupt every 10–15s in anything over 30s (B-roll cutaway, color accent appearing in an otherwise monochrome frame, full-screen number, sound effect).
- Viewers start scrolling after ~12–15s of a static frame (VENDOR heuristic).
- Remove pauses over ~0.3s and filler; if too long, cut content rather than speed up the voice. Hoyos: do not talk fast; deliver dense context then let it breathe.
- Captions: word-synced or 3–5 words on screen at a time, burned in, consistent brand font, key terms highlighted with the one accent color. Correct the auto-captions manually in the hook.
- Text density: one idea per on-screen label. If a label needs two lines, it is a sentence, not a label.

### 2.4 Length (where retention and distribution meet)

- Platform caps relevant to recommendation: Reels up to 3 minutes eligible for non-follower recommendation since Feb 2025 (earlier limit was 90s); Shorts up to 3 minutes since Oct 2024; TikTok distributes 1–3 minute videos when completion holds (OFFICIAL/VENDOR mix).
- Completion benchmarks (VENDOR, Zebracat and others): 21–30s videos hit the highest completion (~64%); under-30s averages ~72% vs ~54% for 30–60s. Top-performing Shorts average ~34s (Hoyos).
- For tech_splained: 45–60s is defensible because explainers need setup, but every video should earn its length. Default to 35–50s; go to 60s only when the payoff requires it. A tighter 30–40s "news" variant is worth testing against the 55s "deep" variant.
- TikTok Creator Rewards pays only on videos over 60s (PRACTITIONER note). If monetization matters there, a 61–75s version may be worth the retention trade.

### 2.5 Endings that avoid pre-CTA drop-off

- Callback: end with the hook's key word or image, so the final line recontextualizes the opening (narrative loop). This also raises replays, which Shorts counts as views since March 31, 2025 (OFFICIAL).
- Visual mirror: match the final frame to the first (same background, same diagram state) so the loop is seamless.
- Keep motion and audio running through the last frame; no musical resolution, no hard stop to black.
- Do not over-explain the ending. A goodbye sequence signals "the end" and viewers leave before the CTA.
- Loop endings suit explainers less than they suit entertainment; for tutorials the recommended close is "complete the arc, then one short question that points at the next video."
- Benchmarks to watch (VENDOR): a retention cliff before 70% means the close starts too early or the payoff runs long. Fix the five seconds before the steepest drop first.

---

## 3. CTAs and platform ranking signals

### 3.1 What each platform says it rewards

| Signal | Instagram Reels | TikTok | YouTube Shorts |
|---|---|---|---|
| Top stated signals | Watch time, likes per reach, sends per reach (Mosseri, Jan 2025, OFFICIAL). In June 2024 Mosseri said watch time matters "a lot less" than sends for reaching non-followers. For followers (connected reach), likes matter more; for non-followers (unconnected reach), sends matter more. | User interactions (completion, rewatch, shares, comments, saves), then video info (captions, sounds, hashtags), then device/account settings (TikTok Newsroom, OFFICIAL). First 3 seconds "critical" (TikTok Creator Academy). | Viewed vs swiped away, completion, retention curve, engaged views; early engagement in first 24–48h; consistency (YouTube Help, OFFICIAL). Weights unpublished. |
| Shares | Strongest for non-follower reach. Vendor rule of thumb: <0.5% sends/reach weak, 0.5–1% solid, 1–2% strong, >2% breakout (VENDOR). | Important; TikTok averages ~1.8x more shares per view than Reels (VENDOR). | Counted, but swipe/retention dominates feed distribution. |
| Saves | Counted; vendor ordering puts saves above comments, below shares. | Counted in early-hour signals. | Minor. |
| Comments | Meaningful comments and threaded replies matter; generic single-word bait is risky (see 3.3). | Threaded replies and first-hour conversation count. | Counted. Pinned comment helps conversation. |
| Rewatches | Plays/reach above ~1.3 signals replay behavior (VENDOR). | Rewatch/loop rate is a priority signal; 20–30% rewatch on short clips is strong (VENDOR). | Replays count as views (since Mar 2025); retention over 100% possible on segments. |
| Follower count | Not a ranking input; recommendations over follows since 2024. | Not a direct ranking factor (OFFICIAL). | Not a direct input. |

### 3.2 CTA types and when to use them

| CTA | Best platform | Phrasing pattern | Notes |
|---|---|---|---|
| **Comment-prompt (topic request)** | TikTok, Reels | "Comment the repo or model you want broken down next." / "Which one should I explain: X or Y?" | Fits the brand goal. Ask an open question with a specific noun class, not "comment yes." Binary choice ("X or Y?") lowers friction and produces debatable threads. |
| **Send/share** | Reels (primary), TikTok | "Send this to the dev on your team who still does X." / "Share this with whoever asked you what MCP is." | Mosseri: make content people would send to a friend. Name the recipient type so the viewer pictures a person. |
| **Save** | Reels, TikTok | "Save this for when you set it up." | Natural for tutorials/reference explainers; weaker for news. |
| **Follow (series)** | All | "Follow; tomorrow is part 2: the security hole in this." | Follow CTAs work when tied to a concrete next episode, not "follow for more." |
| **Caption CTA (no spoken CTA)** | Shorts | CTA lives in title/description/pinned comment | A 3s spoken CTA on a 20s Short is 15% of runtime; on a 55s explainer it is ~5%, so a short spoken CTA is acceptable but keep it under 3s. |

Rules:
- One CTA per video. Match it to the content: save for how-to, send for "did you know," comment for debates/requests.
- Pair spoken CTA with on-screen text; keep the CTA inside the final 3–5 seconds and inside the loop (do not break visual continuity).
- Pin a comment within the first hour that seeds the conversation ("What should I explain Friday?") and reply to early comments in the first hour; first-hour engagement velocity is treated as a growth signal on all three platforms (VENDOR consensus; Mosseri noted rapid first-hour sharing as a sign a Reel is taking off).

### 3.3 Engagement-bait boundary (Instagram, OFFICIAL)

- Instagram (May–June 2024) said asking for a specific word/number/emoji solely to game ranking can limit reach. It clarified that genuine conversation and keyword-triggered DM tools are not the target; intent matters.
- Safe pattern: open-ended, content-specific requests ("comment what to explain next," "tell me what I got wrong"). Risky pattern: "comment YES if you agree," "like if you're watching in 2026."

### 3.4 TikTok STEM feed

- TikTok's STEM feed opened to all users in the US, UK and Ireland on Oct 23, 2024, and expanded regionally through 2025 (OFFICIAL via Social Media Today / TikTok Newsroom). Content is vetted by partner reviewers for educational quality. Clean, accurate tech explainers are the kind of content eligible for it; clear on-screen text and keyword-rich captions help classification.

---

## 4. Format conventions

### 4.1 Length and aspect

- 9:16, 1080x1920, export clean (no watermark, no third-party logo).
- Vertical performs better than square on Shorts (Google guidance via VENDOR summary); square/vertical under 3 minutes is classified as a Short, 16:9 is not.
- Reels: up to 3 minutes eligible for non-follower recommendation (Feb 2025); longer Reels (creation limit 20 min since Dec 2025) mostly reach existing followers.

### 4.2 Captions and on-screen text

- Burned-in (open) captions on every video: platform CC toggles may not render in muted autoplay; captions correlate with higher completion in every study found (VENDOR numbers range from +31% retention to +80% completion likelihood; magnitude unverified, direction consistent).
- 3–5 words on screen at a time or word-synced; high contrast; key term highlighted with one accent color; consistent brand font.
- Instagram reads on-screen text and audio to classify topic; TikTok search indexes captions and on-screen text. Say and show the exact keyword the target viewer would search ("MCP server," "Claude Code hooks," repo name).
- Since Aug 2025 Instagram auto-applies AI caption/audio translation to Reels; clean source captions help that.

### 4.3 Safe zones (1080x1920 working margins, cross-platform conservative)

| Edge | Keep clear | Why |
|---|---|---|
| Top | ~250–290 px | Status bar, "Following/For You" tabs, Shorts title area |
| Bottom | ~480–670 px (conservative: lowest third) | Username, caption, audio, comment box; Reels caption and TikTok description stack here |
| Right | ~110–160 px | Like/comment/share/save column |
| Left | ~60–110 px | Mostly safe; avoid aligning text to the edge |

- Fully protected center is roughly 760 x 960 px. Put captions in the center-to-upper-center band, never in the bottom quarter. Hook text sits in the upper-middle third.
- Platform-specific: Reels covers the most bottom area; TikTok's right column is tallest; Shorts puts the title at the bottom and controls on the right.
- Diagrams: keep the critical node/label inside the center band; decorative lines can bleed to the edges.

### 4.4 Cover frame and title text

- Treat the cover as a separate asset, not a random frame. On Reels the cover is cropped to 4:5 in feed and 1:1 on the profile grid, so center the title.
- Shorts: thumbnail frame can be picked in the mobile app before/after upload; desktop uploads get an auto frame. Title shows below the Short in feed, in search, and on shelves. YouTube recommends concise, accurate titles with important words first. Lead with the problem or outcome ("Why Claude Code forgets your context").
- TikTok: cover text is the on-screen title; choose a frame with the hook text visible.
- Cover and first frame can be the same design: giant hook text + one diagram element.

### 4.5 Hashtags (2025–2026 reality)

| Platform | Current rule | Evidence |
|---|---|---|
| Instagram | Max 5 hashtags per post/Reel (rolling out from Dec 2025). Mosseri said in Feb and May 2025 that hashtags do not increase reach; they help describe content. Metricool 2026 (24M posts) found posts with hashtags got ~32% fewer views (correlation). | OFFICIAL + STUDY |
| TikTok | Max 5 hashtags since Aug 2025. Metricool 2026 (2.3M posts) found videos with at least one hashtag got ~5% more views and ~9% more interactions (correlation). TikTok lists hashtags as a video-info signal below viewer behavior. | OFFICIAL + STUDY |
| YouTube Shorts | Hashtags/title/description should match the topic; no stuffing. No evidence #shorts matters. Treat as light SEO. | OFFICIAL |

Recommendation: 0–2 descriptive hashtags on Instagram (or none), 3–5 on TikTok (1–2 niche community, 1–2 topic, 1 series tag like #techsplained), 2–3 in the Shorts description. Spend the effort on keyword-rich captions and spoken keywords instead.

### 4.6 Posting times

- Two large 2026 studies disagree: Sprout (2B engagements, all platforms) favors Tue–Thu 1–6 pm local; Buffer (7.1M TikTok posts) favors evenings 6–11 pm and weekends, peaking Sat 5 pm and Sun 9 am. Only overlap: Thursday ~1 pm. Hootsuite: Thursday morning / Saturday midday. (STUDY, conflicting)
- Every platform says the first hours drive distribution, so post when your audience is awake and you can reply to comments for the first hour.
- Practical for a 5-day workday cadence targeting US/EU developers: start with weekday 11 am–1 pm ET (catches US lunch and EU late afternoon) and test a 6–8 pm ET slot. Re-check your own Insights after 30 days; audience-specific data beats any study.
- Shorts get their strongest push right after publishing; Reels and TikTok also reward first-hour velocity, so stagger platforms by a few minutes rather than hours if you want to reply on all three.

### 4.7 Cross-posting the same video (watermarks, native upload)

- Instagram: since 2021, Reels with another app's logo/watermark are excluded from Explore and Reels recommendations (still shown to followers). Your own logo is fine (Mosseri, Oct 2024). Originality rules (Apr 2024, extended Apr 2026): no visible watermarks, only the original of duplicate posts is recommended, aggregator accounts lose recommendation eligibility. (OFFICIAL)
- TikTok: content showing someone else's watermark or logo is ineligible for the For You feed; your own clean export is fine. (OFFICIAL, Community Guidelines)
- YouTube: Oct 2026 update prioritizes original content and reduces Shorts distribution for channels that mostly re-upload others' videos. Your own video on all three platforms is not penalized. (OFFICIAL)
- No platform has published a penalty for posting your own clean video to all three on the same day. Native upload of a clean master is the rule; never share from one app to another.
- Adapt per platform, not just re-upload: Shorts title with keywords up front and link in description/pinned comment; Reels caption keyword-rich with the send CTA; TikTok caption with the comment CTA and 3–5 hashtags. Riley Brown is cited as differentiating content per platform rather than straight cross-posting.
- Keep a TikTok-native master (most forgiving on length, most generous on shares) and derive Reels/Shorts versions with the end card and CTA wording changed.

---

## 5. Example accounts and what they do structurally

Described, not copied. Mix of tech, science, and structural masters whose methods transfer to a diagram-led faceless format.

| Creator | Platform focus | What they do structurally | Transferable lesson |
|---|---|---|---|
| **Cleo Abram (Huge If True)** | YouTube long-form + ~30s TikToks/Reels/Shorts | Opens with a single plain-language news line (no clickbait), frames topics as an everyday question, alternates talking segments with animation/graphs/on-screen text, consistent visual identity across long and short. Scripts are built around the opening line. | The news-one-liner hook; script backwards from the opener; same look everywhere. |
| **Jenny Hoyos** | YouTube Shorts (not tech; ~10M avg views/video) | Hook under 3s, readable on mute, max three objects in frame; "but/so" beat chaining; dual narrative (voice tells one story, visuals another); peak in the middle, quick end; top performers average ~34s; retention graph shape over percentage. | The most actionable retention playbook found. Apply "but/so" and dual narrative to diagram explainers. |
| **Fireship** | YouTube (100-second explainers, Shorts cuts) | Information density and meme density both very high; speed comes from script density, not post-production speed-up; deadpan programmer humor; entertainment is the delivery vehicle for the information. | Script tight enough that a 60s video feels like 90s of content; one dry joke per 15s as a re-hook. |
| **Hank Green** | TikTok (science) | Each video answers one submitted viewer question; light, self-deprecating tone; admits uncertainty; 60s cap forces one idea per video. Top videos are responses to comments. | Build the "comment what to explain next" loop into the content: answer-a-comment videos as a recurring format. |
| **AsapScience** | TikTok/YouTube | Whiteboard-style illustration carried from long-form into shorts, plus casual commentary variants. | Signature illustration style is the brand recognizer for a faceless account. |
| **Riley Brown** | TikTok (636K), YouTube, Instagram | Builds apps with AI on screen; content differs by platform rather than cross-posted; ties tutorials to his own products. | Platform-native versions; show the thing working, not slides about it. |
| **Matt Wolfe** | YouTube (~1M), newsletter, podcast | Weekly AI news roundups; news-cycle cadence; cross-channel funnel (FutureTools, newsletter). | News timing: publish within the cycle; roundup format as a reliable weekly slot. |
| **Faceless AI-visual accounts (e.g., @magsimich case)** | TikTok | AI-generated single visual + caption hook, repeated format, viral hits (5.8M, 5.1M) from caption-led hooks with no voice. | Proof that a caption-led first frame alone can carry distribution; the first frame is the hook. |

Pattern across the winners: one idea per video, a hook that is a plain concrete statement, a recognizable visual signature, a mid-video peak, and a short clean end. None of them open with a logo or an intro.

---

## 6. Script-writing SOP checklist (distilled)

1. Pick ONE idea and the single promise the hook makes. Write the ending (payoff + callback line) first.
2. Write 3–5 hooks across at least two archetypes (default: specific number + curiosity gap, or news one-liner). 8–15 words. Text version fits in two lines in the upper-center band.
3. First frame: hook text + one diagram element; readable muted; three objects max; doubles as cover.
4. 3–15s: first concrete proof or visual within 5s. No intro, no context dump.
5. Body: one idea per sentence; "but/so" chaining; an explicit open loop every 10–15s; one peak (surprise or dry joke) near the middle; a visual change every 2–3s (diagram step counts).
6. Dual narrative: narration explains mechanism, diagram shows scale or consequence. Never say what the diagram already shows.
7. Say and show the searchable keyword (model/repo/tool name) at least once in the first 10s.
8. Close: resolve the loop, callback to the hook word/image, mirror the first frame, keep motion going. CTA under 3s: "Comment the repo or model you want explained next." On Reels versions, alternate with a send CTA naming a recipient type.
9. Export clean 1080x1920, burned-in captions in the center band, no watermark. Separate cover asset.
10. Per platform: Shorts title keyword-first; Reels caption keyword-rich, 0–2 hashtags; TikTok 3–5 hashtags incl. a series tag. Pin a seeding comment and reply for the first hour.
11. Measure: VVSA/3s retention (hook), steepest mid drop (fix the 5s before it), completion, sends/reach (Reels), rewatch rate (TikTok/Shorts). Rotate hook archetypes monthly.

---

## Sources

### Hooks and retention
- https://virvid.ai/blog/first-3-seconds-hook-faceless-shorts-2026
- https://virvid.ai/blog/looping-structure-shorts-retention-2026
- https://kineclip.com/blog/how-to-write-viral-hooks-short-form-2026/
- https://postlinkapp.com/blog/hook-examples-for-social-media-videos
- https://dev.to/bulkdl/hook-engineering-the-science-of-the-first-3-seconds-in-short-form-video-2026-2jp9
- https://gpt.social/blog/how-to-script-short-form-videos-2026
- https://shortzly.com/blog/short-form-video-retention-strategies
- https://www.bytecap.io/research/youtube-shorts-retention-benchmarks
- https://www.bytecap.io/blog/science-of-silent-viewing-short-form-video-retention
- https://www.zebracat.ai/post/social-media-video-statistics
- https://rosetta.to/u/vidiq/how-jenny-hoyos-actually-makes-viral-shorts

### Algorithms, CTAs and platform statements
- https://rosetta.to/u/colinandsamir/an-honest-conversation-with-the-ceo-of-instagram
- https://dev.to/stklen/instagram-reels-algorithm-2026-the-3-official-ranking-factors-mme
- https://www.socialpilot.co/blog/instagram-reels-algorithm
- https://www.socialync.io/blog/adam-mosseri-shares-instagram-algorithm-2026
- https://www.socialmediatoday.com/news/instagram-clarifies-advice-single-word-ctas-longer-reels/718151/
- https://www.socialmediatoday.com/news/instagram-clarifies-that-including-your-own-logo-on-a-reel-is-ok/730852/
- https://www.socialmediatoday.com/news/instagram-implements-new-limits-on-hashtag-use/808309/
- https://blog.hootsuite.com/tiktok-algorithm/
- https://www.darkroomagency.com/observatory/how-tiktok%E2%80%99s-algorithm-works-in-2026-and-15-tactics-to-go-viral
- https://frameos.studio/blog/tiktok-hashtags
- https://gyre.pro/blog/understanding-the-youtube-shorts-algorithm-a--guide
- https://subscribr.ai/youtube-strategy/youtube-shorts-titles-thumbnails-matter
- https://www.socialmediatoday.com/news/tiktok-expands-stem-feed-users-us-and-uk/730850/
- https://www.post-bridge.com/blog/does-cross-posting-hurt-engagement

### Format, timing, cross-posting
- https://reap.video/blog/short-form-video-safe-zones
- https://influencermarketinghub.com/cross-posting-matrix
- https://iqfluence.io/public/blog/best-time-to-post-on-tiktok
- https://metricool.com/social-media-short-video-report-2025/

### Creators
- https://async.com/blog/why-cleo-abram-goes-viral/
- https://skills.sh/jarmen423/skills/fireship-video-style
- https://www.yalescientific.org/2021/04/into-the-newsroom-teaching-through-tiktoks
- https://ryandoser.com/ai-content-creators-to-follow/
- https://weekly.joebuildsai.com/p/an-ai-account-with-no-camera-just-hit-5-8-million-views
- https://www.indiehackers.com/post/i-run-a-faceless-ai-tools-tiktok-just-shipped-the-playbook-with-the-actual-2026-monetization-stack-3-sourced-case-studies-6fe30c2f50
