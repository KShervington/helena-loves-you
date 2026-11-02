// Render every theme × frame of explore.html to 1080×1920 JPEGs, then a contact sheet.
import { chromium } from "playwright";
import { fileURLToPath } from "node:url";
import path from "node:path";
import fs from "node:fs";

const here = path.dirname(fileURLToPath(import.meta.url));
const out = path.join(here, "out");
fs.mkdirSync(out, { recursive: true });
const themes = ["blueprint", "instrument", "midnight", "clinical", "signal"];
const frames = ["hook", "diagram"];

const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
for (const t of themes) for (const f of frames) {
  const url = "file://" + path.join(here, "explore.html") + `?theme=${t}&frame=${f}`;
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(100);
  await page.screenshot({ path: path.join(out, `${t}-${f}.jpg`), type: "jpeg", quality: 92 });
  console.log("rendered", t, f);
}
await browser.close();
