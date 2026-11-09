# Examples

Minimal API runners for each Innovative Cookie Actor. Every script expects `APIFY_TOKEN` in the environment (see [`.env.example`](../.env.example)). Never commit tokens.

## Actors and Store links

| Script | Store page |
|---|---|
| `sitemap-extractor` | https://apify.com/innovative_cookie/sitemap-extractor |
| `pagespeed-bulk` | https://apify.com/innovative_cookie/pagespeed-bulk |
| `broken-link-checker` | https://apify.com/innovative_cookie/broken-link-checker |
| `website-image-extractor` | https://apify.com/innovative_cookie/website-image-extractor |
| `domain-availability` | https://apify.com/innovative_cookie/domain-availability |
| `logo-favicon` | https://apify.com/innovative_cookie/logo-favicon |
| `image-converter` | https://apify.com/innovative_cookie/image-converter |
| `dataset-merge-dedup` | https://apify.com/innovative_cookie/dataset-merge-dedup |

Default JSON inputs live in [`../inputs/`](../inputs/).

## Tutorials (dev.to)

- PageSpeed / Core Web Vitals (free PSI API + hosted Actor): https://dev.to/innovative_cookie/bulk-core-web-vitals-with-the-free-pagespeed-insights-api-and-a-small-hosted-option-162g  
- Sitemap URL extraction (Python, free): https://dev.to/innovative_cookie/how-to-extract-every-url-from-a-websites-sitemaps-and-check-their-status-codes-python-free-462j  

## Run

```bash
export APIFY_TOKEN=...   # from console.apify.com/settings/integrations
python examples/python/run_actor.py sitemap-extractor
./examples/curl/sitemap-extractor.sh
node examples/js/run_actor.mjs sitemap-extractor
```
