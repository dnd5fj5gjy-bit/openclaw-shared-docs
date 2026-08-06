#!/usr/bin/env node
// 16:9 landscape deck -> PDF. Full bleed, no margins.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const input = path.resolve(process.argv[2]);
  const output = path.resolve(process.argv[3] || input.replace(/\.html$/i, '.pdf'));
  const browser = await chromium.launch({ headless: true });
  const page = await browser.newPage({ viewport: { width: 1600, height: 900 } });
  await page.goto(`file://${input}`, { waitUntil: 'networkidle' });
  await page.emulateMedia({ media: 'screen' });
  await page.pdf({
    path: output,
    width: '1600px',
    height: '900px',
    margin: { top: '0', bottom: '0', left: '0', right: '0' },
    printBackground: true,
    preferCSSPageSize: false,
  });
  await browser.close();
  console.log('PDF saved: ' + output);
})().catch(e => { console.error('FAILED:', e.message); process.exit(1); });
