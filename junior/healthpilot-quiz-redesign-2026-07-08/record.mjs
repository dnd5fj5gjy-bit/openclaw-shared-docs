import { createRequire } from 'module';
const require = createRequire('/opt/homebrew/lib/node_modules/');
const { chromium } = require('playwright');

const DIR = '/Users/bgvai/agents/junior/workspace/docs/healthpilot-quiz-redesign-2026-07-08';
const URL = 'file://' + DIR + '/prototype.html';
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({
  viewport: { width: 720, height: 1000 },
  deviceScaleFactor: 2,
  recordVideo: { dir: DIR + '/vid', size: { width: 720, height: 1000 } },
});
const page = await ctx.newPage();
const shot = (n) => page.screenshot({ path: `${DIR}/shots/${n}.png` });

async function clickText(t, exact=false){
  const el = page.getByText(t, exact ? { exact:true } : undefined).first();
  await el.scrollIntoViewIfNeeded().catch(()=>{});
  await el.click();
}

try{
  await page.addStyleTag({ content: '*{transition-duration:.35s!important}' }).catch(()=>{});
  await page.goto(URL, { waitUntil:'networkidle' });
  await sleep(1600); await shot('01-entry');            // dashboard + Need guidance nudge
  await clickText('Guide me'); await sleep(1300);       // -> welcome
  await shot('02-welcome');
  await clickText('The full picture'); await sleep(1300);// -> goal
  await shot('03-goal');
  await clickText('My energy'); await sleep(700);
  await clickText('Continue'); await sleep(1200);        // -> symptoms
  for (const s of ['Tired all the time','Broken sleep','No motivation','Short-tempered']){ await clickText(s); await sleep(320); }
  await shot('04-symptoms');
  await clickText('Continue'); await sleep(1300);        // -> reflect1
  await shot('05-reflect');
  await clickText('Keep going'); await sleep(1200);      // -> energy
  await page.$eval('#enRange', el=>{el.value=3;el.dispatchEvent(new Event('input',{bubbles:true}));}); await sleep(900);
  await shot('06-energy');
  await clickText('Continue'); await sleep(1200);        // -> sexual
  await clickText('Lower libido'); await sleep(320); await clickText('Fewer morning erections'); await sleep(500);
  await shot('07-sexual');
  await clickText('Continue'); await sleep(1200);        // -> tradeoff
  await shot('08-tradeoff');
  await clickText('Certainty about'); await sleep(1300); // -> lifestyle
  await clickText('5-6h'); await sleep(280); await clickText('Cardio'); await sleep(280); await clickText('Socially'); await sleep(500);
  await shot('09-lifestyle');
  await clickText('Continue'); await sleep(1100);        // -> stress
  await page.$eval('#stRange', el=>{el.value=8;el.dispatchEvent(new Event('input',{bubbles:true}));}); await sleep(900);
  await shot('10-stress');
  await clickText('Continue'); await sleep(1100);        // -> history
  await clickText('Raised blood pressure').catch(()=>{}); await sleep(280); await clickText('None', true).catch(()=>{});
  await clickText('None'); await sleep(300);
  await clickText('Continue'); await sleep(1200);        // -> bloods
  await shot('11-bloods');
  await clickText('Not that I recall'); await sleep(1400);// -> building -> auto? no, building has no auto; it's a step
  await shot('12-building');
  await clickText('').catch(()=>{});
  // building is a passive step; advance via next() by pressing the flow: there's no button, so call next
  await page.evaluate(()=>window.next && window.next()); await sleep(1600); // -> report
  await shot('13-report');
  await sleep(1200);
} catch(e){ console.log('ERR', e.message); }
finally { await ctx.close(); await browser.close(); }
console.log('done');
