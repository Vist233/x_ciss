import { access } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const webDir = path.dirname(fileURLToPath(import.meta.url));
const assets = [
  "data/abnormal_summary.json",
  "data/dialogue_highlights.json",
  "data/order_check_rules.json",
  "data/order_sets.json",
  "data/order_warnings.json",
  "data/orders_ranked.json",
  "data/patient.json",
  "data/pe_templates.json",
  "data/quote_pool_hpi.json",
  "data/sidebar_support.json",
  "data/similar_cases.json",
  "data/summary.json",
  "data/transcript.json",
  "data/Screenshot 2026-02-01 at 11.27.59.webp",
  "data/Screenshot 2026-02-01 at 11.28.11.webp",
  "data/Screenshot 2026-02-01 at 11.28.19.webp",
];

const missing = [];
for (const asset of assets) {
  try {
    await access(path.join(webDir, asset));
  } catch {
    missing.push(asset);
  }
}

if (missing.length) {
  console.error(`Static-site integrity check failed; missing:\n${missing.map((asset) => `- ${asset}`).join("\n")}`);
  process.exit(1);
}

console.log(`Static-site integrity check passed (${assets.length} assets).`);
