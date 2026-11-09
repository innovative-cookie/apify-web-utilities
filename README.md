# Apify web utilities (Innovative Cookie)

Small public [Apify](https://apify.com) Actors for everyday SEO and web-dev chores: sitemaps, Core Web Vitals, broken links, images, domains, logos, and dataset cleanup.

Each **direct Store link** below opens the Actor page even when Store search hides new creators (KYC / discoverability). You need a free Apify account to run them.

| Actor | What it does | Direct Store link |
|---|---|---|
| **Sitemap URL Extractor** | Pull every URL from XML / gzip / text / RSS / Atom sitemaps (robots.txt discovery, nested indexes) | https://apify.com/innovative_cookie/sitemap-extractor |
| **PageSpeed Insights Bulk** | Bulk lab + field Core Web Vitals via Google’s free PSI API (bring your own key) | https://apify.com/innovative_cookie/pagespeed-bulk |
| **Broken Link Checker** | Crawl a site and list 404s / 5xx / dead external links with source page and anchor | https://apify.com/innovative_cookie/broken-link-checker |
| **Website Image Extractor** | List images on a page (srcset, og:image, CSS backgrounds) with size, format, alt | https://apify.com/innovative_cookie/website-image-extractor |
| **Bulk Domain Availability** | RDAP (+ DNS fallback) availability, expiry, registrar — no WHOIS personal data | https://apify.com/innovative_cookie/domain-availability |
| **Logo & Favicon Extractor** | Best logo / favicon candidates from icons, manifest, JSON-LD, og:image | https://apify.com/innovative_cookie/logo-favicon |
| **Bulk Image Converter** | Convert / compress / resize to WebP, AVIF, JPEG, PNG (URLs, uploads, or a dataset) | https://apify.com/innovative_cookie/image-converter |
| **Dataset Merge & Dedup** | Merge Apify datasets, dedupe, filter, rename / flatten fields (READ-only on sources) | https://apify.com/innovative_cookie/dataset-merge-dedup |

All Actors use **plain HTTP** (no headless browser, no paid proxy). They respect `robots.txt` where they crawl. Actor fee is **free for now** — you only pay Apify platform usage (Free plan includes monthly credit).

Related article: [Bulk Core Web Vitals with the free PageSpeed Insights API](https://dev.to/innovative_cookie/bulk-core-web-vitals-with-the-free-pagespeed-insights-api-and-a-small-hosted-option-162g).

## Quick start (Console)

1. Open a direct link above (free Apify account).
2. Click **Try for free**, keep the default input (it is intentionally tiny).
3. Download results as JSON / CSV / Excel, or use the API below.

## Quick start (API)

Set a token from Apify Console → Settings → Integrations (never commit it):

```bash
export APIFY_TOKEN="$APIFY_TOKEN"   # or paste from Console; do not commit
```

### curl

```bash
# Start sitemap-extractor and wait up to 120s
curl -sS -X POST \
  -H "Authorization: Bearer $APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d @inputs/sitemap-extractor.json \
  "https://api.apify.com/v2/acts/innovative_cookie~sitemap-extractor/runs?waitForFinish=120"
```

Ready-made scripts: [`examples/curl/`](examples/curl/).

### Apify CLI

```bash
apify login   # or APIFY_TOKEN in the environment
apify call innovative_cookie/sitemap-extractor --input inputs/sitemap-extractor.json
```

### JavaScript (`apify-client`)

```bash
npm install apify-client
node examples/js/run_actor.mjs sitemap-extractor
```

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: process.env.APIFY_TOKEN });
const run = await client.actor('innovative_cookie/sitemap-extractor').call({
  urls: ['apify.com'],
  maxUrlsPerSite: 100,
});
const { items } = await client.dataset(run.defaultDatasetId).listItems({ limit: 10 });
console.log(items);
```

### Python (`apify-client`)

```bash
pip install apify-client
python examples/python/run_actor.py sitemap-extractor
```

```python
import os
from apify_client import ApifyClient

client = ApifyClient(os.environ["APIFY_TOKEN"])
run = client.actor("innovative_cookie/sitemap-extractor").call(
    run_input={"urls": ["apify.com"], "maxUrlsPerSite": 100},
)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item)
```

## Sample inputs

Minimal JSON files (from each Actor’s default / prefill) live in [`inputs/`](inputs/). Keep test runs small so they stay inside the Free plan.

| File | Notes |
|---|---|
| `inputs/sitemap-extractor.json` | Two public sites, capped at 100 URLs each |
| `inputs/pagespeed-bulk.json` | Two URLs, mobile + performance only — set `apiKey` or `GOOGLE_PSI_API_KEY` |
| `inputs/broken-link-checker.json` | crawler-test.com fixtures, depth 0 |
| `inputs/website-image-extractor.json` | books.toscrape.com, 25 images max |
| `inputs/domain-availability.json` | Three domain names |
| `inputs/logo-favicon.json` | Three public sites, no download |
| `inputs/image-converter.json` | One Wikimedia PNG → WebP |
| `inputs/dataset-merge-dedup.json` | Inline sample items, dedupe by `url` |

### Example output (sitemap-extractor)

```json
{
  "url": "https://apify.com/",
  "lastmod": "2026-01-15T00:00:00.000Z",
  "changefreq": "daily",
  "priority": 1.0,
  "sitemapUrl": "https://apify.com/sitemap.xml",
  "sitemapFormat": "urlset"
}
```

### Example output (broken-link-checker)

```json
{
  "url": "https://crawler-test.com/links/not_found/foo1",
  "status": "broken",
  "statusCode": 404,
  "sourceUrl": "https://crawler-test.com/links/broken_links_internal",
  "anchorText": "Broken Internal Link 1",
  "linkType": "internal"
}
```

## Honest limitations

- **Not a full browser crawler.** JS-rendered-only pages, heavy SPAs, and sites that require login are out of scope for these Actors.
- **No captcha / anti-bot bypass.** Blocked (401/403/429/challenge) links are reported as blocked or skipped, never forced.
- **No paid proxies.** Everything goes through Apify’s default network; treat rate limits politely.
- **pagespeed-bulk** needs **your own** Google PageSpeed Insights API key and is bound by Google’s quotas.
- **domain-availability** uses RDAP; some TLDs only get a DNS heuristic (`likely-available`). No registrant personal data is returned.
- **Store search visibility** for new creators can lag until Apify identity verification (KYC) is complete — **direct links still work**.
- Default inputs are for demos. Raise crawl limits carefully; you still pay platform compute.

## Free tier note

- Actor fee: **$0** for now (no rental / PPE charged by us).
- You still consume Apify Free-plan credit for compute and storage.
- Keep `maxPages*`, `maxUrls*`, and concurrency low while testing.

## Repo layout

```
inputs/                 Sample Actor inputs
examples/curl/          Bash + curl runners
examples/python/        apify-client helpers
examples/js/            apify-client (ESM) helper
LICENSE                 MIT
```

Actor **source code is not vendored here** (see secret-scan note in the project notes). Use the Store pages or Apify Console to inspect builds.

## Disclosure

Built and maintained by **Innovative Cookie** (`innovative_cookie` on Apify). We are the authors of these Actors. Feedback and issues are welcome on this repository once it is published.

## License

MIT — see [LICENSE](LICENSE).
