const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
  });
  const page = await context.newPage();

  const urls = [];
  const responses = [];

  // Intercept all network requests
  page.on('request', request => {
    const url = request.url();
    if (url.includes('wetransfer') || url.includes('s3.amazonaws') || url.includes('download')) {
      urls.push({ url, method: request.method() });
    }
  });

  page.on('response', async response => {
    const url = response.url();
    const status = response.status();
    if (url.includes('wetransfer') && !url.includes('.js') && !url.includes('.css') && !url.includes('.ico') && !url.includes('.png')) {
      let body = '';
      try {
        body = await response.text();
        if (body.length > 2000) body = body.substring(0, 2000);
      } catch(e) {}
      responses.push({ url, status, body });
    }
  });

  console.log('Loading page...');
  await page.goto('https://collect.wetransfer.com/board/se9bv1t47ejnvz2oo20260530112532/latest', {
    waitUntil: 'networkidle',
    timeout: 30000
  });

  // Wait a bit more for JS to finish
  await page.waitForTimeout(3000);

  console.log('\n=== REQUESTS ===');
  urls.forEach(r => console.log(r.method, r.url));

  console.log('\n=== API RESPONSES ===');
  responses.forEach(r => {
    console.log(`\nURL: ${r.url}`);
    console.log(`Status: ${r.status}`);
    console.log(`Body: ${r.body}`);
  });

  // Also get page content
  const content = await page.content();
  console.log('\n=== PAGE TEXT ===');
  const text = await page.evaluate(() => document.body.innerText);
  console.log(text.substring(0, 3000));

  await browser.close();
})().catch(e => { console.error(e); process.exit(1); });
