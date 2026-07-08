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

async function clickText(t){
  const ok = await page.evaluate((needle)=>{
    const step = document.querySelector('.step.on');
    if(!step) return false;
    const cands = Array.from(step.querySelectorAll('.opt,.chip,.btn,.yes,.no,.skip,.dev,button'));
    // deepest match wins (the label/text node's clickable ancestor)
    const hit = cands.find(el => (el.textContent||'').replace(/\s+/g,' ').trim().toLowerCase().includes(needle.toLowerCase()));
    if(!hit) return false;
    hit.click();
    return true;
  }, t);
  if(!ok) console.log('MISS:', t);
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
  await clickText('Continue'); await sleep(1100);        // -> connect
  await shot('03b-connect-a');
  await clickText('Oura Ring'); await sleep(1300);       // sync reveal
  await shot('03b-connect');
  await clickText('Continue'); await sleep(1100);        // -> symptoms
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
  await clickText('Raised blood pressure').catch(()=>{}); await sleep(320);
  await clickText('Nothing to add'); await sleep(1200);   // skip -> bloods
  await shot('11-bloods');
  await clickText('Not that I recall'); await sleep(900); // -> building
  await shot('12-building');
  await sleep(1900);                                      // building auto-advances -> report
  await shot('13-report');
  await sleep(1400);
} catch(e){ console.log('ERR', e.message); }
finally { await ctx.close(); await browser.close(); }
console.log('done');
