#!/usr/bin/env node
/**
 * Run any Innovative Cookie Actor via apify-client.
 *
 *   export APIFY_TOKEN=...
 *   npm install apify-client
 *   node examples/js/run_actor.mjs sitemap-extractor
 */
import { readFile } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { ApifyClient } from 'apify-client';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '../..');

const ACTORS = {
  'sitemap-extractor': 'innovative_cookie/sitemap-extractor',
  'pagespeed-bulk': 'innovative_cookie/pagespeed-bulk',
  'broken-link-checker': 'innovative_cookie/broken-link-checker',
  'website-image-extractor': 'innovative_cookie/website-image-extractor',
  'domain-availability': 'innovative_cookie/domain-availability',
  'logo-favicon': 'innovative_cookie/logo-favicon',
  'image-converter': 'innovative_cookie/image-converter',
  'dataset-merge-dedup': 'innovative_cookie/dataset-merge-dedup',
};

const actor = process.argv[2];
if (!actor || !ACTORS[actor]) {
  console.error(`Usage: node run_actor.mjs <${Object.keys(ACTORS).join('|')}>`);
  process.exit(1);
}

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set APIFY_TOKEN (see .env.example).');
  process.exit(1);
}

const inputPath = process.argv[3] || resolve(ROOT, 'inputs', `${actor}.json`);
const runInput = JSON.parse(await readFile(inputPath, 'utf8'));

if (actor === 'pagespeed-bulk') {
  if (process.env.GOOGLE_PSI_API_KEY) {
    runInput.apiKey = process.env.GOOGLE_PSI_API_KEY;
  } else if (String(runInput.apiKey || '').startsWith('YOUR_')) {
    console.error('Set GOOGLE_PSI_API_KEY or edit the input JSON.');
    process.exit(1);
  }
}

const client = new ApifyClient({ token });
const actorId = ACTORS[actor];
console.error(`Calling ${actorId} with ${inputPath} …`);
const run = await client.actor(actorId).call(runInput);
const { items } = await client.dataset(run.defaultDatasetId).listItems({ limit: 3 });
console.log(JSON.stringify({ runId: run.id, status: run.status, sample: items }, null, 2));
