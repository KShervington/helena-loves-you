import { chromium } from "playwright";
import path from "node:path"; import fs from "node:fs"; import { fileURLToPath } from "node:url";
const here = path.dirname(fileURLToPath(import.meta.url)); const out = path.join(here, "out"); fs.mkdirSync(out, { recursive: true });
const jobs = [["eurostile","hook"],["eurostile","diagram"],["eurostile","viz"]];   // add ["geometric",…]/["grotesk",…] to re-render the archived alternatives
const browser = await chromium.launch(); const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
for (const [t, f] of jobs) { await page.goto("file://" + path.join(here, "helena.html") + `?type=${t}&frame=${f}`); await page.evaluate(() => document.fonts.ready); await page.waitForTimeout(80);
  await page.screenshot({ path: path.join(out, `${t}-${f}.jpg`), type: "jpeg", quality: 92 }); }
await browser.close();
