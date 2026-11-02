# Topic-discovery data sources for tech_splained

Researched 2026-11-01. Purpose: feed a weekly (plus daily "hot") agent that finds new tech worth a 60-second explainer video: fast-rising GitHub repos, viral Claude Code / agent skills, new models, dev tools, clean-room reimplementations, game decompilations, etc.

Verification legend used in the tables:
- **Verified live** = I hit the endpoint from this session (via the web-fetch tool or `gh`) and saw real data.
- **Docs-verified** = read the official docs page today but did not execute a call.
- **Vendor claim** = only third-party blog/vendor sources; treat as unconfirmed.
- **From memory** = known behaviour as of mid-2026, not re-checked today.

Environment caveat: this sandbox blocks outbound `curl` to most hosts and blocks GitHub GraphQL and reddit.com entirely, so Reddit and a few others could not be live-tested. Noted per row.

---

## 1. GitHub

### 1a. GitHub REST Search API (`/search/repositories`)

| Field | Finding |
|---|---|
| Access | `GET https://api.github.com/search/repositories` (Verified live via `gh api`) |
| Auth | Optional PAT / `gh auth`. Unauthenticated = 10 req/min; authenticated = 30 req/min (search-specific bucket, separate from the 5,000/hr core limit). Docs-verified. |
| Cost | Free |
| Returns | Up to 1,000 results per query (max 100 per page), from at most ~4,000 matches. Items: `full_name`, `stargazers_count`, `created_at`, `pushed_at`, `language`, `topics`, `description`, `forks_count`, `open_issues_count`. |
| Query qualifiers | `created:>YYYY-MM-DD`, `pushed:>YYYY-MM-DD`, `stars:>N`, `topic:x`, `language:x`, plus free text. Sort: `stars`, `forks`, `help-wanted-issues`, `updated`. |
| Velocity | Not directly. Two practical patterns: (1) **"new and already big"** = `created:>7d-ago stars:>200 sort=stars` (this is what surfaces brand-new breakout repos; live test today returned 209 repos created in the last 7 days with >200 stars, top one at 8.3k). (2) **Snapshot diff** = store `stargazers_count` for a watchlist each run and compute delta week-over-week. |
| Gotchas | Search index lags a few minutes to hours. 1,000-result cap means slicing by `created:` ranges if you need more. |

Working example (verified today):

```bash
gh api -X GET search/repositories \
  -f q='created:>2026-10-25 stars:>200' -f sort=stars -f order=desc -f per_page=50 \
  --jq '.items[] | {full_name, stargazers_count, created_at, language, description}'
```

Plain curl:

```bash
curl -s -H "Authorization: Bearer $GITHUB_TOKEN" -H "Accept: application/vnd.github+json" \
  "https://api.github.com/search/repositories?q=created:%3E2026-10-25+stars:%3E200&sort=stars&order=desc&per_page=50"
```

Also useful: `pushed:>2026-10-25 stars:>5000 sort=updated` to catch *old* repos that just shipped something, and `topic:decompilation` / `topic:reverse-engineering` / `"clean room" in:readme` for the decomp niche.

### 1b. GitHub GraphQL (per-repo star velocity)

| Field | Finding |
|---|---|
| Access | `POST https://api.github.com/graphql` (From memory; GraphQL is blocked inside this Claude Code sandbox but works normally elsewhere) |
| Auth | PAT required. 5,000 points/hour; a 100-node stargazers page costs ~1 point. |
| Returns | `repository.stargazers(last:100, orderBy:{field:STARRED_AT, direction:ASC}) { edges { starredAt } }` plus `stargazerCount`. |
| Velocity | Walk backwards from the newest stargazers until `starredAt` < now-7d; count edges. 100 per page, so a repo gaining 5k stars/week costs ~50 points. Fine for a watchlist of a few hundred repos. |
| Gotchas | Stargazer connection is capped (REST caps at 40,000 stargazers = 400 pages; GraphQL has similar practical limits). For mega-repos use GH Archive instead. |

```graphql
query($owner:String!,$name:String!,$before:String){
  repository(owner:$owner,name:$name){
    stargazerCount
    stargazers(last:100, before:$before, orderBy:{field:STARRED_AT,direction:ASC}){
      pageInfo{ hasPreviousPage startCursor }
      edges{ starredAt }
    }
  }
}
```

REST equivalent (From memory): `GET /repos/{o}/{r}/stargazers?per_page=100&page=N` with header `Accept: application/vnd.github.star+json` returns `starred_at`; jump to the last page via the `Link` header and walk backwards.

### 1c. github.com/trending (HTML) and unofficial trending APIs

| Field | Finding |
|---|---|
| Access | `https://github.com/trending?since=weekly&spoken_language_code=en` is HTML only; GitHub has never shipped an official trending API. (From memory) |
| Returns (scraped) | Repo, description, language, total stars, and the "N stars this week/today" figure, which is the only first-party velocity number GitHub publishes. ~25 repos per page per language. |
| Unofficial wrappers | `github-trending/api-service` (self-hostable scraper; the GitHub page failed to load from here so maintenance status is unverified), `gh-trending-no-cors` (lissy93), npm `github-trending-scrape`, several paid Apify actors. Historic `gh-trending-api` (huchenme) is archived. All are scrapers of the same HTML and break when GitHub changes markup. |
| Auth / cost | None for direct scrape; Apify actors are paid per run. |
| Velocity | Already given ("stars this week"). Scrape daily and weekly, store `(repo, period, stars_this_period, rank)`. |
| Recommendation | Scrape the HTML yourself with a tolerant parser (`article.Box-row`), run it inside your own GitHub Action, and treat it as one signal among several rather than the backbone. |

### 1d. GH Archive + BigQuery (ground-truth star velocity)

| Field | Finding |
|---|---|
| Access | Hourly gzipped JSON at `https://data.gharchive.org/YYYY-MM-DD-H.json.gz`; BigQuery public dataset `githubarchive` with `day.YYYYMMDD`, `month.YYYYMM`, `year.YYYY` tables, refreshed hourly. Docs-verified. |
| Auth / cost | Needs a GCP project (the `bq` CLI here lacks one). BigQuery free tier is 1 TB processed/month. A 7-day `WatchEvent` query over day tables scans roughly 10-20 GB/day of events, so a weekly job fits in the free tier if you select few columns and use `_TABLE_SUFFIX` ranges. |
| Returns | Every public event; `WatchEvent` = a star. Also `ForkEvent`, `CreateEvent` (new repo), `ReleaseEvent`. |
| Velocity | Count `WatchEvent` per `repo.name` over a window. This is the most accurate "stars gained in 7 days" available and has no per-repo cap. |

```sql
-- Stars gained per repo in the last 7 days (run with --maximum_bytes_billed)
SELECT repo.name AS repo, COUNT(*) AS stars_7d
FROM `githubarchive.day.2026*`
WHERE _TABLE_SUFFIX BETWEEN FORMAT_DATE('%m%d', DATE_SUB(CURRENT_DATE(), INTERVAL 7 DAY))
                        AND FORMAT_DATE('%m%d', CURRENT_DATE())
  AND type = 'WatchEvent'
GROUP BY repo
HAVING stars_7d >= 500
ORDER BY stars_7d DESC
LIMIT 200;
```

(SQL written from general BigQuery knowledge, not copied from gharchive.org; the dataset/table naming is docs-verified.)

### 1e. OSS Insight API (api.ossinsight.io)

| Field | Finding |
|---|---|
| Access | Base `https://api.ossinsight.io/v1`; trending endpoint `GET /trends/repos/?period=past_24_hours&language=All`. Docs-verified. Two live attempts today returned a server error, so availability is flaky or the proxy interfered. |
| Auth / cost | None during beta. 600 req/hour per IP and 1,000 req/min global, with `x-ratelimit-*` headers. Free. |
| Returns | SQL-endpoint JSON: `{type, data:{columns:[...], rows:[...]}}`; numbers come back as strings. Trending rows include repo name, stars/forks/PR/push activity in the period, a composite score and description (column names from memory of prior use; the docs page did not list them). |
| Periods | Docs example only shows `past_24_hours`; the site UI exposes Today / This Week / This Month, and the API accepts `past_week` and `past_month` (From memory). |
| Velocity | The endpoint is itself a velocity ranking (built from GH Archive events). Good as a cheap cross-check against your own BigQuery numbers. Also `GET /repos/{owner}/{repo}/stargazers/history` style endpoints for per-repo curves (listed in docs index as "stargazers history"). |

```bash
curl -s 'https://api.ossinsight.io/v1/trends/repos/?period=past_week&language=All' -H 'Accept: application/json'
```

### 1f. star-history.com

| Field | Finding |
|---|---|
| Access | Web app that calls the GitHub API from the browser with your own token; image endpoint `https://api.star-history.com/svg?repos=owner/repo&type=Date` returns an SVG chart. (From memory; blocked from this sandbox.) |
| Auth / cost | Free; the site asks for a GitHub PAT for large repos. |
| Returns | SVG only; no JSON data API. |
| Use | Visual asset for the video (star curve), not a discovery source. Generate your own chart from GH Archive data instead so you control styling. |

### 1g. Other "trending" JSON sources still alive

- **trendshift.io** – ranks repos by HN/Reddit/Twitter mentions; HTML, no public API (From memory).
- **Apify actors** (`nexgendata/github-trending-scraper`, `crawlerbros/oss-insight-scraper`) – paid, ~cents per run; useful only if you want zero maintenance.
- **GitHub "Explore" emails / `/topics/*` pages** – HTML only.

---

## 2. Hacker News

### 2a. Algolia HN Search API

| Field | Finding |
|---|---|
| Access | `https://hn.algolia.com/api/v1/search` (relevance) and `/search_by_date` (newest first). Verified live (`tags=front_page` returned 30 hits with `points`, `num_comments`, `created_at_i`, `objectID`, `_tags`). |
| Auth / cost | None; free. Rate limit 10,000 req/hour per IP (vendor-reported, matches the official API page as I remember it). |
| Returns | `hits[]` with `title`, `url`, `points`, `num_comments`, `author`, `created_at`, `created_at_i`, `objectID`, `story_text`, `_tags`; envelope `nbHits`, `nbPages`, `hitsPerPage` (max 1000). |
| Tags | `story`, `show_hn`, `ask_hn`, `front_page`, `author_<name>`, `story_<id>`. Comma = AND; parentheses = OR. |
| Numeric filters | `points>100`, `num_comments>50`, `created_at_i>UNIX` (comma = AND). |
| Velocity | Points and comments at fetch time; store per run and diff. For "did it hit the front page" use `tags=front_page` (current front page only). For weekly digest: `search_by_date?tags=(story,show_hn)&numericFilters=points>150,created_at_i>NOW-7d`. |

```bash
NOW=$(date +%s); WEEK=$((NOW-7*86400))
curl -s "https://hn.algolia.com/api/v1/search_by_date?tags=show_hn&numericFilters=points%3E100,created_at_i%3E$WEEK&hitsPerPage=100"
curl -s "https://hn.algolia.com/api/v1/search?tags=story&query=github.com&numericFilters=points%3E200,created_at_i%3E$WEEK&hitsPerPage=100"
```

Tip: filter `url` for `github.com/`, `huggingface.co/`, `arxiv.org/` to join HN discussion with the other sources.

### 2b. Firebase HN API

| Field | Finding |
|---|---|
| Access | `https://hacker-news.firebaseio.com/v0/` – `topstories.json` (500 IDs), `beststories.json`, `showstories.json` (200), `newstories.json`, `item/{id}.json`, `updates.json`. Docs-verified (GitHub README). |
| Auth / cost | None; README states no rate limit. |
| Returns | Item: `title`, `url`, `score`, `descendants` (comment count), `time`, `type`, `by`. |
| Velocity | Poll `topstories` or `beststories` and `item/{id}` hourly for the daily "hot" lane; `score` delta per hour is a clean velocity measure. Requires one request per item, so use Algolia for bulk and Firebase for live tracking of a shortlist. |

```python
import requests
ids = requests.get("https://hacker-news.firebaseio.com/v0/showstories.json").json()[:50]
items = [requests.get(f"https://hacker-news.firebaseio.com/v0/item/{i}.json").json() for i in ids]
hot = [i for i in items if i and i.get("score",0) >= 100]
```

---

## 3. Hugging Face Hub

| Field | Finding |
|---|---|
| Access | `GET https://huggingface.co/api/models` (also `/api/datasets`, `/api/spaces`). Verified live: `?sort=trendingScore&direction=-1&limit=3` returned items with `id` and `trendingScore` (top was `google/embeddinggemma-2` at 968). `GET /api/trending?type=model&limit=N` also verified live; returns `recentlyTrending[]` of `{repoType, repoData{id, likes, downloads, pipeline_tag, numParameters, lastModified, availableInferenceProviders...}}` but no explicit score. |
| Auth / cost | Optional `HF_TOKEN`. Rate limits per 5-minute window: anonymous 500 API calls, free account 1,000, PRO 2,500 (docs-verified). Headers follow the IETF `RateLimit` draft; `huggingface_hub>=1.2` auto-waits on 429. Free. |
| Params | `sort` (`trendingScore`, `likes`, `downloads`, `createdAt`, `lastModified`), `direction=-1`, `limit` (max 100), `filter=<tag>` (e.g. `text-generation`, `arxiv:2610.xxxxx`), `author=`, `search=`, `expand[]=likes&expand[]=downloads&expand[]=createdAt&expand[]=trendingScore`. Cursor pagination via the `Link` header. Note: in today's live call with `expand[]` the summarized response showed only `trendingScore`; confirm the exact `expand` spelling in the OpenAPI spec (`/.well-known/openapi.json`). |
| Daily papers | `GET https://huggingface.co/api/daily_papers?limit=50` verified live. Items: `title`, `summary`, `publishedAt`, `numComments`, `submittedBy`, `organization`, `thumbnail`, and nested `paper{id, authors, upvotes, publishedAt, submittedOnDailyAt, discussionId, githubRepo?, githubStars?, projectPage?}`. `?date=YYYY-MM-DD` is widely used by community scrapers for a specific day (From memory). `GET /api/papers/{arxiv_id}` returns `upvotes`, `publishedAt`, `title` for one paper (verified via the hysts Space source). |
| Velocity | `trendingScore` is HF's own recency-weighted popularity (likes/downloads over roughly the last week). Store `likes`, `downloads`, `trendingScore` per repo per run and diff; a new model entering the top 20 by `trendingScore` within 7 days of `createdAt` is your "new model" trigger. For papers, `paper.upvotes` plus `githubStars` of the linked repo. |
| Webhooks | Hub webhooks exist for repos you already know; not useful for discovery. |

```bash
curl -s -H "Authorization: Bearer $HF_TOKEN" \
 'https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=50&expand[]=likes&expand[]=downloads&expand[]=createdAt&expand[]=pipeline_tag'
curl -s 'https://huggingface.co/api/daily_papers?limit=50' | jq '.[] | {id:.paper.id, title, up:.paper.upvotes, repo:.paper.githubRepo, stars:.paper.githubStars}'
```

Python: `from huggingface_hub import HfApi; HfApi().list_models(sort="trendingScore", direction=-1, limit=50, expand=["likes","downloads","createdAt"])`.

---

## 4. arXiv and paper-trend services

### 4a. arXiv API and RSS

| Field | Finding |
|---|---|
| Access | `http://export.arxiv.org/api/query?search_query=cat:cs.CL&sortBy=submittedDate&sortOrder=descending&max_results=200`. Docs-verified. Atom 1.0 output. |
| Auth / cost | None; free. Etiquette: one request every 3 seconds; max 2,000 results per call, 30,000 per query. |
| Query syntax | Prefixes `cat:`, `ti:`, `abs:`, `all:`; Boolean `AND`/`OR`/`ANDNOT`; `submittedDate:[202610250000+TO+202611010000]`. Combine categories: `cat:cs.CL OR cat:cs.CV OR cat:cs.LG OR cat:cs.AI`. |
| RSS | `https://rss.arxiv.org/rss/cs.CL` (or `/atom/`), multi-category `cs.CL+cs.CV+cs.LG+cs.AI`, updated nightly at midnight US Eastern, 2,000-item cap. Docs-verified. |
| Velocity | arXiv has no popularity signal. Join on arXiv ID with HF daily-paper upvotes, HN points (search `arxiv.org/abs/<id>`), and GitHub repos tagged `arxiv:<id>` on HF or found via GitHub search `"<arxiv id>" in:readme`. |

### 4b. Trending-paper services

| Service | Status (2026-11) |
|---|---|
| **Papers with Code** | Shut down by Meta in late July 2025; `paperswithcode.com/api/v1` is not maintained. Visitors were steered to Hugging Face Papers. Historical JSON dumps exist on GitHub. Do not build on it. (Vendor-confirmed; consistent with memory.) |
| **HF Daily Papers** | The de-facto replacement; see 3 above. Curated submissions with upvotes, comments, linked repos. |
| **alphaXiv** | Trending/"Hot" feed on alphaxiv.org (views, votes, comments); no public REST API documented. Offers an MCP server at `https://api.alphaxiv.org/mcp/v1` (Streamable HTTP; OAuth 2.1 or API key from Settings > API Keys) with tools `get_hot_feed` (30-day hot feed), `discover_papers`, `get_paper_content`. Quotas undocumented. Docs-verified. Good fit for an agentic pipeline since Claude Code can call it directly. |
| **Semantic Scholar API** | Not researched in depth; useful for citation velocity but too slow for weekly video topics. (From memory) |

---

## 5. Product Hunt API (GraphQL)

| Field | Finding |
|---|---|
| Access | `POST https://api.producthunt.com/v2/api/graphql`; register an app at `producthunt.com/v2/oauth/applications`. Docs-verified. |
| Auth | OAuth2 client-credentials token for public read, or a non-expiring **developer token** from the app dashboard for personal scripts (docs-verified). |
| Cost / limits | Free. Complexity budget 6,250 points per 15 minutes on GraphQL; 450 requests per 15 minutes on other v2 routes; `X-Rate-Limit-Limit/Remaining/Reset` headers; 429 when exceeded. |
| Terms | The docs state the API must not be used commercially; business use requires emailing Product Hunt. A monetized video channel is a gray area; keep usage low-volume and attribute, or ask. |
| Returns | `posts(order: RANKING|VOTES|NEWEST, postedAfter:, postedBefore:, topic:)` with `name`, `tagline`, `votesCount`, `commentsCount`, `featuredAt`, `topics`, `website`, `url`. (Field list from memory; the overview page only links to the schema reference.) |
| Velocity | `votesCount` within 24-72h of `featuredAt`; snapshot daily. Filter topics `artificial-intelligence`, `developer-tools`, `open-source`, `github`. |

```bash
curl -s https://api.producthunt.com/v2/api/graphql -H "Authorization: Bearer $PH_TOKEN" -H 'Content-Type: application/json' \
 -d '{"query":"{ posts(order: VOTES, postedAfter: \"2026-10-25T00:00:00Z\", first: 50, topic: \"developer-tools\") { edges { node { name tagline votesCount commentsCount featuredAt website url topics { edges { node { slug } } } } } } }"}'
```

Fallback: `https://www.producthunt.com/feed` (RSS of featured posts, no vote counts; From memory).

---

## 6. Reddit (r/LocalLLaMA, r/MachineLearning, r/programming, r/ClaudeAI)

| Field | Finding |
|---|---|
| Access | OAuth Data API `https://oauth.reddit.com/r/{sub}/top?t=week&limit=100` after obtaining a token from `https://www.reddit.com/api/v1/access_token` with a "script" app's client id/secret. reddit.com is blocked from this sandbox, so nothing here is live-verified. |
| Auth / limits | Official wiki (Docs-verified, last substantive update references July 2023): 100 QPM per OAuth client id, averaged over 10 minutes; 10 QPM without OAuth; descriptive `User-Agent` of the form `platform:appid:version (by /u/name)` required; limits exposed in `X-Ratelimit-*` headers. |
| Cost | Free tier for non-commercial use within 100 QPM. The $0.24 per 1,000 calls commercial figure dates from 2023 and no current self-serve price page exists; commercial access is by application and vendors report 2-4 week review queues (Vendor claim). A weekly read of four subreddits is a few dozen calls, far inside free. |
| 2026 changes | One vendor (KeyAPI, Aug 2026) claims unauthenticated `.json` URLs started returning 403 in late May 2026 and a "Responsible Builder" review applies to business OAuth apps; the article is internally inconsistent, so **verify directly** before relying on `.json`. |
| RSS fallback | `https://www.reddit.com/r/LocalLLaMA/top/.rss?t=week` and `/new/.rss` historically work without auth and return Atom with title/link/author/updated but **no score**. Could not be tested from here (blocked). If `.json` is truly gone, expect `.rss` to be rate-limited or require a browser-like UA. |
| Returns | `data.children[].data`: `title`, `score`, `ups`, `upvote_ratio`, `num_comments`, `created_utc`, `url`, `permalink`, `link_flair_text`, `selftext`. |
| Velocity | `score` and `num_comments` on `top?t=day` vs `t=week`; store and diff. Extract outbound `github.com`/`huggingface.co` links to join with other sources. |

```python
import requests, requests.auth
auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
tok = requests.post("https://www.reddit.com/api/v1/access_token",
    auth=auth, data={"grant_type":"client_credentials"},
    headers={"User-Agent":"linux:techsplained-topics:0.1 (by /u/YOURNAME)"}).json()["access_token"]
r = requests.get("https://oauth.reddit.com/r/LocalLLaMA/top", params={"t":"week","limit":100},
    headers={"Authorization":f"bearer {tok}","User-Agent":"linux:techsplained-topics:0.1 (by /u/YOURNAME)"})
posts = [c["data"] for c in r.json()["data"]["children"]]
```

Alternatives if Reddit becomes hostile: Hyper MCP `reddit_scrape` (already available in this workspace's skills), or paid providers (SocialCrawl, Apify) at cents per 1k posts.

---

## 7. Skill / plugin marketplaces for coding agents

### 7a. skills.sh (Vercel) and `npx skills`

| Field | Finding |
|---|---|
| What it is | The largest open registry of agent skills (`SKILL.md` in a public GitHub repo). Install via `npx skills add owner/repo [--skill name]`. Leaderboard at skills.sh with views **All Time**, **Trending (24h)**, **Hot**, plus an "8W Activity" sparkline and total installs (e.g. top entry ~4.1M). Docs-verified. |
| API | `https://skills.sh/api/v1/skills?view=trending|hot|all-time&per_page=100&page=0`, `/api/v1/skills/search?q=`, `/api/v1/skills/curated`, `/api/v1/skills/{owner}/{repo}/{skill}` (returns `installs`, content `hash`, `files[]`), `/api/v1/skills/audit/{source}/{skill}` (Socket/Snyk/etc. results). Docs-verified. |
| Auth | **Vercel OIDC token** (`Authorization: Bearer $VERCEL_OIDC_TOKEN`), i.e. the caller must be a Vercel project (or `vercel env pull` locally). 600 req/min per team/project; 429 with `Retry-After`. This is the main friction: you need a (free) Vercel project to get a token. |
| Returns | Skill object: `id`, `slug`, `name`, `source`, `installs`, `sourceType`, `installUrl`, `url`, `isDuplicate`. Hot view adds `installsYesterday` and `change` (same-hour-yesterday delta). No weekly-installs field. |
| Velocity | Snapshot `installs` for the top ~500 daily and compute 1d/7d deltas yourself; the `hot` view's `change` is the only built-in delta. Also watch `trending` rank movement and newly created skills with high first-week installs (new `id` appearing in top 100). Install counts include CI/bot installs, so treat as relative. |
| No-auth fallback | Scrape `https://skills.sh/` leaderboard HTML (toggle is client-side; the page is server-rendered for All Time), or consume the daily JSON snapshots published by the community dashboard `vishalsachdev/skills-sh` (GitHub Actions scraper, `snapshots/` directory). |

```bash
curl -s "https://skills.sh/api/v1/skills?view=trending&per_page=50" -H "Authorization: Bearer $VERCEL_OIDC_TOKEN"
```

### 7b. Anthropic marketplaces and directory

| Field | Finding |
|---|---|
| Catalogs | `anthropics/claude-plugins-official` (marketplace `claude-plugins-official`, auto-added), `anthropics/claude-plugins-community` (`claude-community`), `anthropics/claude-code` demo (`claude-code-plugins`), plus topic repos `anthropics/skills`, `anthropics/knowledge-work-plugins`. Each is a `.claude-plugin/marketplace.json`. Docs-verified. |
| Web | `https://claude.com/marketplace/plugins` lists ~530 plugins with "Anthropic verified" badges. The docs say it shows install counts; the page I fetched today showed none, so the counts may be client-rendered or recently removed. No API or RSS. |
| Velocity | Watch commits to `marketplace.json` in the official and community repos (`GET /repos/anthropics/claude-plugins-official/commits?path=.claude-plugin/marketplace.json`) for new entries; then measure the plugin's source repo via GitHub stars/GH Archive. |

### 7c. Awesome lists and aggregators

- `hesreallyhim/awesome-claude-code`, `travis-vl/awesome-claude-skills` and similar: diff README commits weekly for new entries (From memory for repo names; verify).
- Third-party indexes: skillselion.com (claims thousands of ranked skills, offers an MCP), claudemarketplaces.com, orangebot.ai (daily scraper publishing `skills_index.json`), agentskillsfinder.com. None documents a stable public API; all are scrapes of skills.sh plus GitHub.
- Signal fusion for "a skill is going viral": skills.sh trending rank up AND source repo gained >500 stars/week (GH Archive) AND at least one HN or r/ClaudeAI post with >50 points. Any two of three is a strong candidate.

---

## 8. Release / news feeds

| Publisher | Feed | Status |
|---|---|---|
| Anthropic | No official RSS (`anthropic.com/news/rss.xml` 404s). Community mirror `https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml` verified live today (~185 items, latest 2026-10-28). Also the Claude Code changelog `https://github.com/anthropics/claude-code/blob/main/CHANGELOG.md` (poll via GitHub commits API) and `https://status.claude.com/history.rss` (outages only). | Verified live (mirror) |
| OpenAI | `https://openai.com/news/rss.xml` | Listed by feeder.co; not fetched today |
| Google DeepMind | `https://deepmind.google/blog/rss.xml` | Listed by feeder.co; not fetched today |
| Meta AI | No working RSS found; `ai.meta.com/blog/rss/` failed today. Use a generated feed (feeder/rss.app) or scrape `ai.meta.com/blog/`. | Unverified / likely none |
| Mistral | `https://mistral.ai/news/rss` | Listed by feeder.co; not fetched today |
| Hugging Face blog | `https://huggingface.co/blog/feed.xml` | Listed by feeder.co; not fetched today |
| TLDR AI | `https://tldr.tech/api/rss/ai` – RSS 2.0, 20 items, title/link/category/pubDate, **no description**. Other verticals: `/api/rss/tech`, `/api/rss/dev`. | Verified live |
| The Rundown AI | `https://www.therundown.ai/feed` – RSS 2.0, 50 items with description. | Verified live |
| Ben's Bites | `https://www.bensbites.com/feed` – RSS 2.0 with `content:encoded` full text, enclosure thumbnails. | Verified live |
| GitHub Releases | `https://github.com/{owner}/{repo}/releases.atom` per repo for watchlist tools (From memory). | |

Use newsletters as a *lag indicator* (if TLDR covered it, it is already mainstream) and lab feeds as a *lead indicator* for model launches.

---

## 9. Demand check: Google Trends and YouTube

| Field | Finding |
|---|---|
| pytrends | Archived April 2025; scrapes internal endpoints that Google keeps changing, so it fails unpredictably. Do not depend on it. (Vendor claim, consistent with memory.) |
| Official Google Trends API | Announced 24 July 2025 as a limited alpha via Search Central: consistently scaled interest (comparable across calls), rolling ~1,800-day window, daily/weekly/monthly aggregation, ISO 3166-2 regions, no five-term cap. Access is by application with stated use case; no pricing or GA date as of today. Worth applying as a journalist/creator use case. (Docs-verified via ppc.land summary of the announcement.) |
| Paid alternatives | SerpApi, Apify actors (~half a cent per term), Glimpse, TrendsMCP. Only needed if the alpha application is rejected. |
| YouTube Data API v3 | `search.list?q=<topic>&type=video&publishedAfter=<7d ago>&order=viewCount` costs 100 quota units; default quota 10,000 units/day, free with a GCP project (From memory). Use `videos.list` (1 unit) on the result IDs for `statistics.viewCount`. A topic with zero recent explainer videos above 50k views is a gap; one with ten is saturated. |
| Cheaper proxies | Count of HN + Reddit posts mentioning the term (already collected); Wikipedia pageviews API (`wikimedia.org/api/rest_v1/metrics/pageviews`) for concepts that have an article; Google autocomplete scrape for "what is X". |

---

## 10. Scoring rubric for candidates

Score each candidate 0-5 on six axes; weights reflect a short-form explainer channel for a general tech audience.

| Axis | Weight | 0 | 3 | 5 | How to compute / judge |
|---|---|---|---|---|---|
| **Velocity** | 0.25 | <100 stars or <50 HN points this week | 1k-3k stars/wk or HN front page | >5k stars/wk, or top-5 HF trending, or #1 skills.sh trending | Normalize per source: `log10(stars_7d)`, HN points, HF trendingScore rank, skills.sh install delta. Take max across sources. |
| **Timeliness** | 0.15 | Older than 30 days with no new event | 7-14 days old or major release this week | First seen <72h, or launch/release in last 48h | `now - first_seen_at`; reset on a new `ReleaseEvent` or lab announcement. |
| **Novelty** | 0.15 | Incremental version of something covered | New approach in a known category | New category or counterintuitive result | LLM judge with the last 90 days of covered topics as context; penalize near-duplicates (see 11). |
| **Explainability in 60s** | 0.20 | Needs background most viewers lack | One analogy gets you 80% there | One-sentence "what if" premise | LLM judge asked to write the one-sentence hook; fail if it cannot without jargon. |
| **Visualizability** | 0.15 | Pure backend/infra, nothing to show | Terminal demo or diagram | Has a GIF, demo video, before/after, or runs in a browser | Check README for images/GIFs, HF Space, demo URL, game footage (decomps score high). |
| **General-audience relevance** | 0.10 | Only a niche of developers cares | Most developers care | Non-developers would care (phones, games, money, privacy) | LLM judge plus keyword heuristics; r/programming vs r/technology crossover is a good proxy. |

`total = sum(weight * score)`; shortlist `>= 3.4`, auto-reject `< 2.0`, and hard-gate: explainability `>= 3` and visualizability `>= 2` regardless of velocity. Add a **daily hot-lane override**: any candidate with velocity 5 and timeliness 5 skips the weekly queue.

## 11. Dedupe strategy

1. **Canonical key**: resolve every signal to one of `github:owner/repo`, `hf:namespace/name`, `arxiv:id`, `url:<normalized domain+path>`. Extract GitHub/HF/arXiv URLs from HN `url`/`story_text`, Reddit `url`/`selftext`, PH `website`, HF `githubRepo`, skills.sh `source`. Lower-case, strip `www.`, trailing slashes, `.git`, query strings, and follow GitHub renames via `GET /repos/{o}/{r}` (returns the new `full_name`).
2. **Entity merge**: a paper + its repo + its HF model are one topic. Link via HF `arxiv:` tags, README arXiv IDs, and the `paper.githubRepo` field. Store all keys in `aliases[]`.
3. **Fuzzy title match**: for items with no URL (newsletter blurbs, Reddit text posts), embed `title + first 300 chars` and merge at cosine `>= 0.86` against the last 60 days of topics; confirm with an LLM yes/no when between 0.78 and 0.86.
4. **Fork/mirror suppression**: use skills.sh `isDuplicate`, GitHub `fork: true`, and name-similarity against higher-starred repos.
5. **Covered-topic memory**: keep `status: published` topics forever with their aliases; a re-surfacing topic needs a new `ReleaseEvent`/announcement to re-enter as a `followup` type instead of being dropped.
6. **Source-count bonus**: dedupe is also the velocity multiplier; `sources_count >= 3` adds +0.5 to the total score.

## 12. Minimal data model: `topics.json`

```json
{
  "version": 1,
  "generated_at": "2026-11-01T12:00:00Z",
  "topics": [
    {
      "id": "github:heydamir/unslop",
      "aliases": ["url:github.com/heydamir/unslop", "hn:46012345"],
      "title": "unslop",
      "one_liner": "A linter that strips AI-sounding filler from your prose.",
      "category": "dev-tool",
      "tags": ["cli", "writing", "llm"],
      "first_seen_at": "2026-10-29T15:41:21Z",
      "last_updated_at": "2026-11-01T11:58:02Z",
      "status": "candidate",
      "lane": "weekly",
      "signals": [
        {"source": "github_search", "observed_at": "2026-11-01T11:50:00Z", "metrics": {"stars": 4957, "forks": 120, "created_at": "2026-10-29T15:41:21Z"}, "url": "https://github.com/heydamir/unslop"},
        {"source": "gharchive", "observed_at": "2026-11-01T11:55:00Z", "metrics": {"stars_7d": 4950, "stars_24h": 1800}},
        {"source": "hn_algolia", "observed_at": "2026-11-01T11:56:00Z", "metrics": {"points": 412, "comments": 190, "front_page": true}, "url": "https://news.ycombinator.com/item?id=46012345"}
      ],
      "velocity": {"stars_7d": 4950, "hn_points": 412, "hf_trending_rank": null, "skills_installs_7d": null, "sources_count": 2},
      "scores": {"velocity": 5, "timeliness": 5, "novelty": 3, "explainability": 4, "visualizability": 3, "relevance": 3, "total": 3.95, "scored_at": "2026-11-01T12:00:00Z", "scorer": "claude-sonnet-4.5"},
      "assets": {"readme_url": "https://raw.githubusercontent.com/heydamir/unslop/main/README.md", "demo_media": [], "star_history_svg": null},
      "notes": "Hook: your writing has an AI accent and this tool hears it.",
      "history": [{"at": "2026-11-01T12:00:00Z", "event": "created", "by": "topic-discovery"}]
    }
  ]
}
```

Field rules:
- `id` is the canonical key from section 11; `aliases` holds every other key ever merged in.
- `status` enum: `candidate` → `shortlisted` → `scripted` → `published` | `rejected` | `stale`. `lane`: `weekly` | `hot`.
- `signals[]` is append-only raw observations (one per source per run); `velocity` and `scores` are derived and overwritten each run so the file stays small. Prune `signals` older than 30 days for non-published topics.
- Keep `topics.json` under ~500 live topics; archive `published`/`rejected` to `topics-archive.jsonl`.

## 13. Suggested run plan

- **Hourly (hot lane, cheap)**: HN Firebase `topstories` + `showstories` scores; HF `/api/trending`; lab RSS feeds; Claude Code CHANGELOG commits.
- **Daily**: GitHub search `created:>7d stars:>200` and `pushed:>1d stars:>5000`; github.com/trending daily scrape; HF models/papers; skills.sh trending; Reddit `top?t=day` for the four subs; TLDR/Rundown/Ben's Bites feeds.
- **Weekly**: GH Archive BigQuery `stars_7d` top 200; OSS Insight `past_week` cross-check; arXiv RSS joined with HF upvotes; Product Hunt `postedAfter` 7d; YouTube Data API demand check for the shortlist; scoring + dedupe pass.

Total API cost at this cadence: $0 for everything except BigQuery (inside free tier) and optional paid Reddit/Trends fallbacks.

---

## Sources

GitHub
- https://docs.github.com/en/rest/search/search?apiVersion=2022-11-28
- https://docs.github.com/en/graphql/reference/objects#stargazerconnection
- https://www.gharchive.org/
- https://ossinsight.io/docs/api
- https://ossinsight.io/docs/api/list-trending-repos
- https://ossinsight.io/blog/introducing-trending-page
- https://github.com/github-trending/api-service
- https://github.com/lissy93/gh-trending-no-cors
- https://npmjs.com/package/github-trending-scrape
- https://apify.com/nexgendata/github-trending-scraper
- https://apify.com/crawlerbros/oss-insight-scraper.md
- https://dev.to/devil_scrapes/github-trending-api-scrape-todays-hottest-repos-for-2001k-5b2b
- https://dev.to/agenthustler/free-github-scraping-api-in-2026-no-signup-required-4ihb
- https://jsr.io/@hk/ossinsight-client
- https://x-cmd.com/mod/ossinsight

Hacker News
- https://hn.algolia.com/api
- https://hn.algolia.com/api/v1/search?tags=front_page&hitsPerPage=3
- https://github.com/HackerNews/API
- https://dev.to/odeeb/the-hacker-news-search-api-free-no-key-and-surprisingly-powerful-5e8l
- https://dev.to/odeeb/hacker-news-firebase-api-vs-algolia-which-one-to-use-3g2n
- https://dev.to/agenthustler/scraping-hacker-news-in-2026-complete-guide-algolia-api-date-filters-3iep

Hugging Face
- https://huggingface.co/docs/hub/api
- https://huggingface.co/docs/hub/rate-limits
- https://huggingface.co/.well-known/openapi.md
- https://huggingface.co/api/daily_papers?limit=3
- https://huggingface.co/api/trending?type=model&limit=3
- https://huggingface.co/api/models?sort=trendingScore&direction=-1&limit=3&expand[]=trendingScore&expand[]=likes&expand[]=downloads&expand[]=createdAt&expand[]=pipeline_tag
- https://huggingface.co/spaces/hysts/daily-papers/blob/24eae416fa7098a12d68ca550a171b9047c68b59/papers.py
- https://dev.to/scrapemint/the-hugging-face-hub-is-a-free-json-api-rank-trending-ai-models-without-a-key-39cb

arXiv and papers
- https://info.arxiv.org/help/api/basics.html
- https://info.arxiv.org/help/api/user-manual.html
- https://info.arxiv.org/help/rss.html
- https://www.alphaxiv.org/
- https://www.alphaxiv.org/docs/mcp
- https://www.codesota.com/papers-with-code/shutdown
- https://www.codesota.com/papers-with-code/api
- https://hyper.ai/en/news/42900

Product Hunt
- https://www.producthunt.com/v2/docs
- https://www.producthunt.com/v2/docs/rate_limits/headers
- https://apify.com/mattdef/producthunt-scraper
- https://rollout.com/integration-guides/product-hunt/api-essentials

Reddit
- https://support.reddithelp.com/hc/en-us/articles/16160319875092-Reddit-Data-API-Wiki
- https://www.socialcrawl.dev/blog/reddit-api-key-limits-alternatives-2026
- https://www.socialcrawl.dev/blog/reddit-data-api-2026.md
- https://www.keyapi.ai/blog/reddit-data-api-overhaul-major-changes-and-migration-guide/
- https://dev.to/agenthustler/reddit-data-api-2026-after-the-pricing-change-heres-what-developers-actually-use-4o2h
- https://www.xpoz.ai/blog/guides/reddit-api-pricing-tiers-and-alternatives/
- https://apiserpent.com/blog/best-reddit-api-providers-2026

Skills and plugins
- https://skills.sh/
- https://skills.sh/docs/api
- https://vishalsachdev.github.io/skills-sh/about.html
- https://dev.to/shenhuang/how-i-indexed-2000-claude-code-skills-and-what-the-install-data-says-about-ai-coding-in-2026-3k80
- https://dev.to/skillselion/everything-claude-code-has-285000-github-stars-its-most-installed-skill-has-18189-installs-58e0
- https://skillselion.com/skills
- https://claudemarketplaces.com/skills/geekjourneyx/mind-skills/trending-skills
- https://code.claude.com/docs/en/plugins/anthropic-marketplaces.md
- https://code.claude.com/docs/en/discover-plugins
- https://claude.com/marketplace/plugins
- https://github.com/anthropics/claude-plugins-official
- https://github.com/anthropics/claude-plugins-community

News feeds
- https://feeder.co/knowledge-base/rss-content/ai-news-rss-feeds/
- https://raw.githubusercontent.com/Olshansk/rss-feeds/main/feeds/feed_anthropic_news.xml
- https://openai.com/news/rss.xml
- https://deepmind.google/blog/rss.xml
- https://mistral.ai/news/rss
- https://huggingface.co/blog/feed.xml
- https://ai.meta.com/blog/rss/
- https://tldr.tech/api/rss/ai
- https://www.therundown.ai/feed
- https://www.bensbites.com/feed
- https://www.readless.app/pt-BR/blog/best-ai-news-rss-feeds-2026

Google Trends / demand
- https://developers.google.cn/search/blog/2025/07/trends-api
- https://ppc.land/google-opens-alpha-testing-for-new-trends-api-targeting-developers-and-journalists/
- https://dev.to/esteban_ortega/pytrends-is-dead-heres-how-to-get-google-trends-data-in-2026-1a18
- https://apiserpent.com/blog/pytrends-dead-google-trends-data-2026
- https://scrapebadger.com/blog/does-google-trends-have-an-api-what-to-use-in-2026
- https://scrapegraphai.com/blog/google-trends-api
- https://trendsmcp.ai/trendsmcp-vs-google-trends-api
- https://meetglimpse.com/google-trends/api/
