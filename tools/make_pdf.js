// Print an HTML file to an A4 PDF with headless Chromium (Playwright).
// Usage: node tools/make_pdf.js guide/guide.html out.pdf
// Set CHROMIUM_PATH to use a specific Chromium binary.
const path = require("path");

let playwright;
try {
  playwright = require("playwright");
} catch {
  const { execSync } = require("child_process");
  const globalRoot = execSync("npm root -g").toString().trim();
  playwright = require(path.join(globalRoot, "playwright"));
}

(async () => {
  const [input, output] = process.argv.slice(2);
  const browser = await playwright.chromium.launch({
    executablePath: process.env.CHROMIUM_PATH || undefined,
  });
  const page = await browser.newPage();
  await page.goto("file://" + path.resolve(input), { waitUntil: "load" });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: output,
    format: "A4",
    printBackground: true,
    preferCSSPageSize: true,
  });
  await browser.close();
})().catch((err) => {
  console.error(err);
  process.exit(1);
});
