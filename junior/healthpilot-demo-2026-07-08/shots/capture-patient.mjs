import { createRequire } from 'module';
const require = createRequire('/opt/homebrew/lib/node_modules/');
const { chromium } = require('playwright');

const OUT = '/Users/bgvai/agents/junior/workspace/docs/healthpilot-demo-2026-07-08/shots';
const BASE = 'http://localhost:4301';
const EMAIL = 'oliver-tanner@demo.tedshealth.example';
const PASS = 'DemoPass123!';

const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 2 });
const page = await ctx.newPage();

async function dismissCookies() {
  for (const t of ['Accept', 'Accept all', 'Got it', 'I agree', 'Allow all']) {
    const b = page.getByRole('button', { name: new RegExp(t, 'i') });
    if (await b.count().catch(() => 0)) { await b.first().click().catch(() => {}); await sleep(300); break; }
  }
}

try {
  await page.goto(`${BASE}/login`, { waitUntil: 'networkidle' });
  await sleep(1200);
  await dismissCookies();

  // Fill login form (Firebase emulator behind it)
  const email = page.locator('input[type="email"], input[name="email"], input[placeholder*="mail" i]').first();
  const pass = page.locator('input[type="password"], input[name="password"]').first();
  await email.fill(EMAIL);
  await pass.fill(PASS);
  await page.getByRole('button', { name: /sign in|log ?in|continue/i }).first().click().catch(async () => {
    await pass.press('Enter');
  });

  // Wait for dashboard
  await page.waitForURL(/dashboard/i, { timeout: 20000 }).catch(() => {});
  await sleep(3000);
  await dismissCookies();
  await page.screenshot({ path: `${OUT}/08-patient-dashboard.png`, fullPage: false });
  console.log('WROTE 08-patient-dashboard.png  url=' + page.url());

  // Try to open the health report / result to show summary + recommended actions
  const link = page.getByRole('link', { name: /report|result|assessment|view/i }).first();
  if (await link.count().catch(() => 0)) {
    await link.click().catch(() => {});
    await sleep(2500);
    await page.screenshot({ path: `${OUT}/03-summary-cta.png`, fullPage: false });
    console.log('WROTE 03-summary-cta.png  url=' + page.url());
  } else {
    console.log('no report link found; 08 only');
  }
} catch (e) {
  console.log('ERROR ' + (e?.message || e));
} finally {
  await browser.close();
}
