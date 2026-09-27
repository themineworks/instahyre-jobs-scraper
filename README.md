# Instahyre Jobs Scraper: India Tech Job Search Feed

Scrape Instahyre's public India tech job-search feed: title, company tagline, founding year, employee count, company description, normalised locations, and a skills array. Salary and full descriptions sit behind Instahyre's own account wall and are not returned. No login required.

**Run it on Apify:** [apify.com/themineworks/instahyre-jobs-scraper](https://apify.com/themineworks/instahyre-jobs-scraper)
**Docs, FAQ and pricing:** [themineworks.com/actors/instahyre-jobs-scraper](https://themineworks.com/actors/instahyre-jobs-scraper/)

**Price:** $2.00 per 1,000 jobs on Apify's free plan, down to $1.20 on higher plans, plus a $0.005 start fee per run. Failed and empty results are never charged.

## What it returns

* Company firmographics on every row: founded year, headcount, tagline
* Skills returned as a structured array
* Free, non-billed market-snapshot record with top companies/locations
* Monitor mode bills only for genuinely new postings
* Reads Instahyre's public JSON feed. No HTML parsing to break

## Quick start

You need a free [Apify account](https://console.apify.com/sign-up) and its API token (Settings, API & Integrations).

### Python

```bash
pip install apify-client
```

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")
run = client.actor("themineworks/instahyre-jobs-scraper").call(run_input={
    "jobFunctionSlugs": [
        "backend-development"
    ],
    "maxJobs": 10
})

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

### Node.js

```bash
npm install apify-client
```

```javascript
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });
const run = await client.actor('themineworks/instahyre-jobs-scraper').call({
    "jobFunctionSlugs": [
        "backend-development"
    ],
    "maxJobs": 10
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### cURL

One request that runs the actor and returns the results in the response (for runs under 5 minutes):

```bash
curl -X POST "https://api.apify.com/v2/acts/themineworks~instahyre-jobs-scraper/run-sync-get-dataset-items?token=YOUR_APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"jobFunctionSlugs": ["backend-development"], "maxJobs": 10}'
```

### Command line

This repo includes ready-made clients that save results to JSON and CSV:

```bash
python3 instahyre_jobs_scraper.py --token YOUR_APIFY_TOKEN --job-function-slugs "backend-development" --max-jobs "10"
node instahyre_jobs_scraper.mjs --token YOUR_APIFY_TOKEN --job-function-slugs "backend-development" --max-jobs "10"
```

## Input

| Field | Type | Default | Description |
|---|---|---|---|
| `jobFunctionSlugs` | array |  | Instahyre job-function slugs to filter by, for example 'backend-development', 'full-stack-development'… |
| `jobType` | string | `"any"` | Filter by employment type |
| `companySize` | string | `"any"` | Filter by hiring company's size band |
| `maxJobs` | integer | `100` | Maximum jobs to return across all pages/functions |
| `monitorMode` | boolean | `false` | When enabled, this and every subsequent scheduled run delivers ONLY jobs not seen in a prior run of this… |

## Output

One row per result, as JSON, CSV, Excel or through the API.

| Field | Type | Description |
|---|---|---|
| `job_id` | integer |  |
| `title` | string |  |
| `candidate_title` | string |  |
| `company_name` | string |  |
| `company_tagline` | string |  |
| `company_founded` | integer |  |
| `employee_count` | integer |  |
| `company_about` | string |  |
| `locations` | array |  |
| `locations_raw` | string |  |
| `skills` | array |  |
| `accept_outstation` | boolean |  |
| `public_url` | string |  |
| `resource_uri` | string |  |
| `scraped_at` | string |  |

## Use it from an AI agent

The actor works as a tool in Claude, Cursor or any MCP client through Apify's MCP server:

```
https://mcp.apify.com/?tools=themineworks/instahyre-jobs-scraper
```

## FAQ

### Is this scraping HTML?

No. It reads Instahyre's public JSON job-search feed directly.

### Why is there no salary or full job description?

Instahyre requires an account for both. This actor only scrapes the public search feed, so neither is returned. Stated up front rather than discovered after paying.

### Can I search by keyword or city?

Not on the public feed. It is organised by job function slug; filter by location downstream using the locations field.

### How do I find valid jobFunctionSlugs values?

They are the slugs Instahyre uses in its own job-search URLs, for example backend-development. Run once with the market-snapshot record to see which functions carry inventory.

### What does it cost?

Pay per job delivered. The market-snapshot record is never billed.

### Can I export the results to CSV or Excel?

Yes. Every run saves to an Apify dataset you can download as JSON, CSV, Excel or XML, or read through the API. The Python and Node clients in this repo also write the results to local files.

### Can I run it on a schedule?

Yes. Save your input as a task on Apify and attach a schedule, or call the API from your own cron job. Scheduled runs are billed the same way as manual ones.

## Related scrapers

* [Foundit Jobs Scraper](https://themineworks.com/actors/foundit-jobs-scraper/): Foundit.in (Monster India): 20 fields, monitor mode
* [Hirist Jobs Scraper](https://themineworks.com/actors/hirist-jobs-scraper/): India IT jobs across 147 locations, 19 fields
* [Naukri Jobs Scraper](https://themineworks.com/actors/naukri-jobs/): India's largest job board structured as clean JSON

Part of [The Mine Works](https://themineworks.com/): 151 pay-per-result scrapers with no login and no browser setup on your side.

## License

MIT © The Mine Works
