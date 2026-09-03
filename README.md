# 💼 LinkedIn Job Search API: a no-login LinkedIn job scraper for listings, results counts, and autocomplete

> The LinkedIn job scraper that needs no login, no cookies, and no account. Search job listings, read LinkedIn's own results count, hydrate full job details, and resolve company ids and geoIds, all as clean JSON.

**Actor page:** [apify.com/johnvc/linkedin-job-search-scraper](https://apify.com/johnvc/linkedin-job-search-scraper?fpr=9n7kx3)
**Input schema:** [apify.com/johnvc/linkedin-job-search-scraper/input-schema](https://apify.com/johnvc/linkedin-job-search-scraper/input-schema?fpr=9n7kx3)

The LinkedIn Job Search API is a no-login LinkedIn job scraper delivered as a clean JSON API. Point it at a keyword plus a location and it returns job listings (title, company, location, posted date, and the canonical job URL), plus a free results-count row carrying LinkedIn's own total for that query. Hand it a job URL and it returns the full record: description, seniority, employment type, salary when published, industries, and the applicant count. Three typeahead modes return job-title suggestions, company ids for the company filter, and geoIds for precise location targeting. There is no login, no cookies, and no account: it reads LinkedIn's public guest pages, so scraping LinkedIn jobs without an account is the default here, not a workaround.

## Video Walkthrough

[![Watch the walkthrough](https://img.youtube.com/vi/jREWahDGhJM/maxresdefault.jpg)](https://www.youtube.com/watch?v=jREWahDGhJM)

### Text walkthrough

This repo is a runnable quick start for the LinkedIn job scraper on Apify, wrapped as the LinkedIn Job Search API. The one required input is `search_mode`; in `search` mode you add `keywords` and a `location`, and you can narrow with `datePosted`, `companyIds`, `easyApplyOnly`, and `under10Applicants`, every filter applied at the source before anything is billed. Each search row carries `jobTitle`, `companyName`, `location`, `postedDate`, and `jobUrl`, and every search also emits a free `searchMeta` row with `resultsCountCaption` and `resultsCountParsed`, which is LinkedIn's own total for that query. Switch `search_mode` to `job` and pass `jobUrls` to pull full records with `descriptionText`, `seniorityLevel`, `employmentType`, `salaryText`, and `numApplicants`. The `companySuggestions` mode turns a company name into the numeric LinkedIn company id the filter needs, and `locationSuggestions` returns the geoId for any city or country. A common use case, mirrored by a published task, is finding LinkedIn jobs with under 10 applicants: set `under10Applicants` to true with a recent `datePosted` window and you surface fresh, low-competition postings before the crowd. The Python example keeps its first run cheap so you can try each mode for pennies.

## Quick Start

### Prerequisites
- Python 3.11 or higher
- An Apify account and API key ([get a free key here](https://apify.com?fpr=9n7kx3))

1. **Clone the repository**
   ```bash
   git clone https://github.com/johnisanerd/Apify-LinkedIn-Job-Search-API.git
   cd Apify-LinkedIn-Job-Search-API
   ```

2. **Install dependencies with UV**
   ```bash
   # Install UV if you do not have it:
   curl -LsSf https://astral.sh/uv/install.sh | sh

   # Install project dependencies:
   uv sync
   ```

3. **Configure your API key**
   ```bash
   cp .env.example .env
   # Edit .env and add your Apify API key
   # Get your free API key at: https://apify.com?fpr=9n7kx3
   ```

4. **Run the example**
   ```bash
   # Default run is a near-zero-cost autocomplete call:
   uv run python linkedin-job-search-api-example.py

   # Task-aligned recipes (see the Recipes section):
   uv run python linkedin-job-search-api-example.py --example search-without-account
   uv run python linkedin-job-search-api-example.py --example company-id-lookup
   uv run python linkedin-job-search-api-example.py --example under-10-applicants
   ```

### Alternative: set the API key directly
```bash
export APIFY_API_TOKEN="your_api_key_here"
uv run python linkedin-job-search-api-example.py
```

## Why Use This LinkedIn Job Search API?

**No login, no cookies, no account.** The Actor reads LinkedIn's public guest pages, so you can search LinkedIn jobs without an account and never touch a session cookie. There is no cookie input at all, and any cookie a response tries to set is discarded.

**A free results count on every search.** Each `search` run pushes a free `searchMeta` row with LinkedIn's own caption, for example `7,000+ Semiconductor Engineering Jobs in United States`, returned verbatim, parsed to a number, and flagged when LinkedIn caps it. Track that number over time to watch hiring demand by keyword and location without paying for a single listing.

**Honest filters that run at the source.** Date posted, company ids, Easy Apply, and the under-10-applicants filter are all forwarded to LinkedIn and applied before billing, so you only pay for rows that already match. Filtered and duplicate jobs are never billed.

**Company ids and geoIds built in.** Two typeahead modes resolve the exact codes precise filtering needs: `companySuggestions` is a LinkedIn company id finder that maps a name to its numeric id, and `locationSuggestions` returns the live geoId for any city or country instead of a stale static list.

**Full job records on demand.** Feed job URLs or bare ids to the `job` mode and get the complete description (text and HTML), seniority level, employment type, job function, industries, applicant count, and salary when the posting publishes one.

**Structured JSON you can call anywhere.** Every mode returns clean rows you can read over the Apify API from Python, export to CSV or Excel, or wire into an AI agent over MCP.

## Features

### Core Capabilities
- Five modes from one input field: `search`, `job`, `autocomplete`, `companySuggestions`, `locationSuggestions`
- Keyword plus location job search with `datePosted`, `companyIds`, `easyApplyOnly`, and `under10Applicants` filters
- Free `searchMeta` results-count row on every search
- Full job detail scrape from any `linkedin.com/jobs/view/` URL or bare job id
- Job-title, company id, and geoId typeahead lookups

### Data Quality
- One row per unique job, deduped by `jobId`; duplicate URLs collapse into a single billed row
- Canonical `jobUrl` and `companyLinkedinUrl` with tracking parameters stripped
- Free in-band `error` rows (never billed) when a URL is dead or a page changes
- Pay per delivered row, no start fee and no monthly minimum

## Recipes

Each recipe below is a published, ready-to-run configuration on Apify Store. The top three also ship as Python helpers in `linkedin-job-search-api-example.py`.

### Search LinkedIn Jobs Without an Account or Login

[Run this on Apify](https://apify.com/johnvc/linkedin-job-search-scraper/examples/search-linkedin-jobs-without-an-account?fpr=9n7kx3): `search` mode with `keywords` plus `location`, returning job title, company, location, posted date, and job URL as JSON, CSV, or Excel, with no login and no cookies.

Local: `uv run python linkedin-job-search-api-example.py --example search-without-account`

### Look Up LinkedIn Company IDs for Job Filters

[Run this on Apify](https://apify.com/johnvc/linkedin-job-search-scraper/examples/look-up-linkedin-company-ids-for-job-filters?fpr=9n7kx3): the `companySuggestions` mode as a LinkedIn company id finder; type a company name and get back `suggestionId` and `displayName`, the numeric ids the company job filter needs.

Local: `uv run python linkedin-job-search-api-example.py --example company-id-lookup`

### Find LinkedIn Jobs With Under 10 Applicants

[Run this on Apify](https://apify.com/johnvc/linkedin-job-search-scraper/examples/find-linkedin-jobs-with-under-10-applicants?fpr=9n7kx3): a `search` with `under10Applicants` set to true, surfacing only the postings with fewer than 10 applicants so far, filtered at the source.

Local: `uv run python linkedin-job-search-api-example.py --example under-10-applicants`

### Get LinkedIn GeoIDs for Any City or Country

[Run this on Apify](https://apify.com/johnvc/linkedin-job-search-scraper/examples/get-linkedin-geoids-for-any-city-or-country?fpr=9n7kx3): the `locationSuggestions` mode returns live LinkedIn geoId codes by name, so you can target a search precisely with the `geoId` field instead of relying on a stale static list.

### Track LinkedIn Job Counts by Keyword and Location

[Run this on Apify](https://apify.com/johnvc/linkedin-job-search-scraper/examples/track-linkedin-job-counts-by-keyword-and-location?fpr=9n7kx3): read `resultsCountCaption`, `resultsCountParsed`, and `resultsCountIsCapped` from the free `searchMeta` row to follow LinkedIn's own job count for any keyword and location over time.

Two Simplified-Chinese task pages cover the same Actor: [免登录搜索领英职位](https://apify.com/johnvc/linkedin-job-search-scraper/examples/mian-denglu-sousuo-lingying-zhiwei?fpr=9n7kx3) and [提取领英职位详情](https://apify.com/johnvc/linkedin-job-search-scraper/examples/tiqu-lingying-zhiwei-xiangqing?fpr=9n7kx3).

**Schedule tip:** Save any of these inputs as an Apify Task and [schedule it](https://apify.com/johnvc/linkedin-job-search-scraper?fpr=9n7kx3) to run daily or weekly. A scheduled `search` run is a practical stand-in for a LinkedIn jobs RSS feed: your dataset stays fresh, and the free results-count row keeps a running record of demand without any manual runs.

## Usage Examples

### Basic Example
```json
{
  "search_mode": "search",
  "keywords": "software engineer",
  "location": "United States",
  "maxItems": 10
}
```

### Advanced Example
```json
{
  "search_mode": "search",
  "keywords": "data engineer",
  "location": "Austin, TX",
  "datePosted": "pastWeek",
  "under10Applicants": true,
  "companyIds": ["1441"],
  "maxItems": 10
}
```

## Input Parameters

Built from the Actor's real [input schema](https://apify.com/johnvc/linkedin-job-search-scraper/input-schema?fpr=9n7kx3).

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `search_mode` | `str` | YES | `search` | One of `search`, `job`, `autocomplete`, `companySuggestions`, `locationSuggestions`. |
| `keywords` | `str` | search mode | - | What to search for: a job title, skill, or phrase, for example `semiconductor engineer`. |
| `location` | `str` | search mode | - | Free-text place, for example `United States` or `Philadelphia, PA`. Resolved server-side. |
| `geoId` | `str` | no | - | LinkedIn geo id from the `locationSuggestions` mode; use together with `location`. |
| `datePosted` | `str` | no | `any` | One of `any`, `past24h`, `pastWeek`, `pastMonth`. |
| `companyIds` | `array` | no | `[]` | Numeric company ids from the `companySuggestions` mode; multiple ids combine as OR. |
| `easyApplyOnly` | `bool` | no | `false` | Only jobs with LinkedIn Easy Apply. |
| `under10Applicants` | `bool` | no | `false` | Only jobs with fewer than 10 applicants so far. |
| `jobUrls` | `array` | job mode | - | `linkedin.com/jobs/view/` URLs or bare numeric ids; duplicates collapse into one billed row. |
| `query` | `str` | suggestion modes | - | The text to complete, for example `semic` for titles or `appl` for companies. |
| `maxItems` | `int` | no | `100` | Cap on billable rows (1 to 1000). Free `searchMeta` and `error` rows never count. |

## Output Format

Real rows from the Actor's dataset. A `jobListing` row from the `search` mode:

```json
{
  "resultType": "jobListing",
  "jobId": "4451264908",
  "jobTitle": "Silicon Design Engineer",
  "companyName": "AMD",
  "companyLinkedinUrl": "https://www.linkedin.com/company/amd",
  "location": "Austin, TX",
  "jobUrl": "https://www.linkedin.com/jobs/view/silicon-design-engineer-at-amd-4451264908",
  "postedDate": "2026-08-24",
  "postedText": "3 days ago",
  "position": 1,
  "searchKeywords": "semiconductor engineering",
  "searchLocation": "United States",
  "viaResidentialProxy": false,
  "fetchedAt": "2026-08-27T23:04:11Z"
}
```

The free `searchMeta` row that precedes every search (never billed):

```json
{
  "resultType": "searchMeta",
  "searchKeywords": "semiconductor engineering",
  "searchLocation": "United States",
  "datePosted": "pastWeek",
  "resultsCountCaption": "7,000+ Semiconductor Engineering Jobs in United States",
  "resultsCountParsed": 7000,
  "resultsCountIsCapped": true,
  "searchUrl": "https://www.linkedin.com/jobs/search?keywords=semiconductor+engineering&location=United+States&f_TPR=r604800"
}
```

A `job` row from the `job` mode adds the full description (`descriptionText` and `descriptionHtml`), `seniorityLevel`, `employmentType`, `jobFunction`, `industries`, `numApplicants`, parsed salary fields (`salaryText`, `salaryMin`, `salaryMax`, `salaryCurrency`), `similarJobs`, and `peopleAlsoViewed`. A `suggestion` row from the typeahead modes carries `suggestionType` (`TITLE`, `COMPANY`, or `GEO`), `suggestionId`, and `displayName`.

## People also search for

### Is this a LinkedIn job scraper or an API?

Both. This repo teaches the **LinkedIn Job Search API** on Apify. People often search for a "linkedin job scraper" or ways to "scrape linkedin jobs"; the same Actor covers that need and returns structured JSON you can call from Python or MCP, with no login and no cookies.

### How do I scrape LinkedIn jobs without login or an account?

Run the Actor in `search` mode with `keywords` and a `location`. It reads LinkedIn's public guest pages, so no login, cookie, or account is involved. See the Quick Start and the "Search LinkedIn Jobs Without an Account or Login" recipe above.

### How do I use the LinkedIn job scraper from Python?

Clone this repo, set `APIFY_API_TOKEN`, run `uv sync`, then `uv run python linkedin-job-search-api-example.py`. The default run is a cheap autocomplete call; the `--example` recipes mirror the published Store tasks.

### How do I find a LinkedIn company id?

Use the `companySuggestions` mode as a LinkedIn company id finder: pass a company name as `query` and read `suggestionId` from each row. Feed those ids into the `companyIds` filter to restrict a search to specific employers.

### How do I filter LinkedIn jobs by number of applicants?

Set `under10Applicants` to true in `search` mode to return only postings with fewer than 10 applicants so far. Full job records from the `job` mode also expose `numApplicantsText` and a parsed `numApplicants` count.

### How do I find LinkedIn jobs posted in the last 24 hours?

Set `datePosted` to `past24h` (or `pastWeek` / `pastMonth`) in `search` mode. The filter runs at the source, so only fresh postings come back and only matching rows are billed.

### What is a LinkedIn geoId and how do I get one?

A geoId is LinkedIn's numeric location code. Run the `locationSuggestions` mode with a place name as `query` to get live geoIds, then pass one in the `geoId` field alongside `location` for precise targeting.

### Can I use the LinkedIn job scraper with MCP or Claude?

Yes. Use the install sections below to add the Actor as an MCP tool in [Claude Code](https://claude.ai/referral/uIlpa7nPLg) (free trial), [Claude Cowork](https://claude.ai/referral/uIlpa7nPLg) (free trial), Claude.ai, Cursor, or ChatGPT.

---

## Install as an MCP tool

Add the LinkedIn Job Search API to any MCP client through the hosted Apify MCP server. The server URL is built from the `actors` and `docs` helper tools plus this one Actor, which keeps the tool list small:

```
https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-job-search-scraper
```

Auth is either OAuth in the browser when offered, or your Apify API token (the same `APIFY_API_TOKEN` secret used by the Python example). Get a token at https://console.apify.com/settings/integrations and a free Apify account at https://apify.com?fpr=9n7kx3 .

## Install in Claude Cowork Desktop

![Install in Claude Cowork Desktop](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_desktop.png)

Cowork is the desktop app's automation mode. To give it the LinkedIn Job Search API as a tool, add the Apify MCP server as a connector.

1. Open the Claude desktop app and go to **Settings → Connectors** (or **Settings → Developer → Edit Config** to edit `claude_desktop_config.json` directly).
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`
2. Add the Apify MCP server, preloaded with only this Actor:

```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": [
        "-y",
        "mcp-remote",
        "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-job-search-scraper"
      ]
    }
  }
}
```

3. Restart the app. When Cowork first calls the tool, complete the OAuth prompt in your browser, or add your Apify API token in the connector settings to skip OAuth.
4. In a Cowork chat, confirm the tool is available and ask it to run the LinkedIn Job Search API.

Download the desktop app and start a free trial: https://claude.ai/referral/uIlpa7nPLg
More help: https://docs.apify.com/platform/integrations/claude-desktop

## Install in Claude Code

![Install in Claude Code](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_code.png)

Claude Code is the command-line tool. Add the Actor's MCP server with one command:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-job-search-scraper"
```

To use a token instead of browser OAuth:

```bash
claude mcp add --transport http apify \
  "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-job-search-scraper" \
  --header "Authorization: Bearer YOUR_APIFY_API_TOKEN"
```

Then verify with `claude mcp list`, or run `/mcp` inside a session. Ask Claude Code to call the LinkedIn Job Search API.

Try Claude Code free: https://claude.ai/referral/uIlpa7nPLg
Claude Code MCP docs: https://code.claude.com/docs/en/mcp

## Install in Claude (website)

![Install in Claude (website)](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_claude_ai.png)

On claude.ai you add Apify as a connector, then enable just this Actor's tool.

1. Go to **Settings → Connectors → Browse connectors** and search for **Apify MCP server**. Install it (enable or update if prompted).
2. When connecting, authenticate with your Apify API token, and enable the tool `johnvc/linkedin-job-search-scraper`.
3. In any chat, open **+ → Connectors** and turn on **Apify**.
4. Alternatively, choose **Add custom connector** and paste the full MCP URL `https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-job-search-scraper`, using OAuth when prompted.
5. Ask Claude to run the LinkedIn Job Search API.

Open Claude on the web: https://claude.ai

## Install in Cursor

![Install in Cursor](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_cursor.png)

Cursor reads MCP servers from a project file at `.cursor/mcp.json`.

1. In your project, create `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-job-search-scraper"
    }
  }
}
```

2. If you prefer token auth over browser OAuth, add a header:

```json
{
  "mcpServers": {
    "apify": {
      "url": "https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-job-search-scraper",
      "headers": { "Authorization": "Bearer YOUR_APIFY_API_TOKEN" }
    }
  }
}
```

3. Open **Cursor → Settings → MCP** and confirm the **apify** server is connected (green dot).
4. In Composer or Chat, ask Cursor to call the LinkedIn Job Search API.

New to Cursor? Get it here: https://cursor.com/referral?code=XQP4VBLI3NNX

## Install in ChatGPT

![Install in ChatGPT](https://raw.githubusercontent.com/johnisanerd/ApifyPublicData/main/assets/guides/install_mcp_into_ChatGPT.png)

ChatGPT connects to the Apify MCP server through Developer mode (available on ChatGPT Pro, Plus, Business, Enterprise, and Education plans).

1. Click your profile icon, then go to **Settings > Apps**. If you do not see a **Create app** button, open **Advanced settings** and enable **Developer mode**.
2. Click **Create app** and fill out the form:
   - **Name:** Apify
   - **MCP Server URL:** `https://mcp.apify.com/?tools=actors,docs,johnvc/linkedin-job-search-scraper`
   - **Authentication:** OAuth
3. Click **Create** and authorize the connection with Apify.
4. To use the app in a conversation, click **+** in the chat, choose **Developer mode**, and select **Apify**.

More help: https://docs.apify.com/platform/integrations/mcp

---

[**Made with care**](https://apify.com/johnvc?fpr=9n7kx3)

*Use the LinkedIn Job Search API to power your data workflows with reliable, structured results.*

Last Updated: 2026.09.02
