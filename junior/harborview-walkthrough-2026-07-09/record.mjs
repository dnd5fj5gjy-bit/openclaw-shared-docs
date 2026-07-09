import { chromium } from '/Users/bgvai/agents/shared/node_modules/playwright/index.mjs';
import fs from 'fs';
const FILE = 'file:///Users/bgvai/openclaw-shared-docs/junior/harborview-demo/index.html';
const OUT = '/Users/bgvai/openclaw-shared-docs/junior/harborview-walkthrough-2026-07-09/clips';
const VP = { width:1440, height:900 };

// target seconds per scene (audio + buffer); actions are paced to fill these
const TARGET = {
  '01-intro':20.2,'02-whitelabel':21.2,'03-quiz':23.2,'04-results':23.6,
  '05-bloods':11.8,'06-bloodreview':27.2,'07-portal':14.2,'08-close':32.4
};
const wait = (p,ms)=>p.waitForTimeout(ms);
async function smoothScroll(p, toY, ms){
  const steps = Math.max(6, Math.round(ms/60));
  const from = await p.evaluate(()=>window.scrollY);
  for(let i=1;i<=steps;i++){ const y = from + (toY-from)*(i/steps); await p.evaluate(y=>window.scrollTo(0,y), y); await wait(p, ms/steps); }
}

const SCENES = {
 '01-intro': async(p)=>{ await wait(p,2500); await smoothScroll(p,700,7000); await wait(p,1500); await smoothScroll(p,0,6000); await wait(p,1500); },
 '02-whitelabel': async(p)=>{
    await wait(p,1200);
    await p.evaluate(()=>toggleStudio(true)); await wait(p,2200);
    await p.evaluate(()=>loadPreset('vantage')); await wait(p,3200);
    await p.evaluate(()=>loadPreset('meridian')); await wait(p,3200);
    await p.evaluate(()=>{ setField('name','Aspire Health'); }); await wait(p,1600);
    await p.evaluate(()=>{ setColor('brand','#3b2f6b'); }); await wait(p,2200);
    await p.evaluate(()=>toggleStudio(false)); await wait(p,3000);
    await smoothScroll(p,420,2500); await wait(p,1200);
 },
 '03-quiz': async(p)=>{
    await p.evaluate(()=>startQuiz()); await wait(p,1600);
    await p.evaluate(()=>{ pickMany('reason','Low energy & fatigue'); }); await wait(p,900);
    await p.evaluate(()=>{ pickMany('reason','Poor sleep'); }); await wait(p,900);
    await p.evaluate(()=>{ pick('duration','3 to 6 months'); }); await wait(p,1100);
    await p.evaluate(()=>nextStep()); await wait(p,1200);
    await p.evaluate(()=>{ pick('energy','Running on empty'); }); await wait(p,900);
    await p.evaluate(()=>{ pick('sleep','Patchy'); }); await wait(p,1100);
    await p.evaluate(()=>nextStep()); await wait(p,1200);
    await p.evaluate(()=>{ pickMany('symptoms','Fatigue'); pickMany('symptoms','Low libido'); }); await wait(p,900);
    await p.evaluate(()=>{ pick('goal','More energy'); }); await wait(p,900);
    await p.evaluate(()=>{ pick('libido','Yes, lower than before'); }); await wait(p,1100);
    await p.evaluate(()=>nextStep()); await wait(p,1400);
 },
 '04-results': async(p)=>{
    await p.evaluate(()=>{ startQuiz(); answers.reason=['Low energy & fatigue','Poor sleep']; answers.energy='Running on empty'; answers.sleep='I wake up wrecked'; answers.libido='Yes, lower than before'; answers.stress=8; buildResults(); show('results'); });
    await wait(p,2600);
    await smoothScroll(p,360,3200); await wait(p,1400);
    await p.evaluate(()=>addFeatured()); await wait(p,2200);
    await smoothScroll(p,1000,4200); await wait(p,1600);
    await smoothScroll(p,1700,3600); await wait(p,1400);
 },
 '05-bloods': async(p)=>{
    await p.evaluate(()=>enterPortal('bloods')); await wait(p,2400);
    await smoothScroll(p,420,4200); await wait(p,2200);
 },
 '06-bloodreview': async(p)=>{
    await p.evaluate(()=>enterPortal('bloods')); await wait(p,1000);
    await p.evaluate(()=>orderBloods()); await wait(p,4200);
    await wait(p,2200);
    await smoothScroll(p,520,4200); await wait(p,1600);
    await p.evaluate(()=>addBloodStack()); await wait(p,2200);
    await smoothScroll(p,1200,4200); await wait(p,1600);
 },
 '07-portal': async(p)=>{
    await p.evaluate(()=>enterPortal('dashboard')); await wait(p,2600);
    await smoothScroll(p,360,4200); await wait(p,1600);
    await smoothScroll(p,0,2600); await wait(p,1200);
 },
 '08-close': async(p)=>{
    await p.evaluate(()=>goLanding()); await wait(p,2000);
    await smoothScroll(p,900,5000); await wait(p,1500);
    await smoothScroll(p,1900,5000); await wait(p,1500);
    await smoothScroll(p,3100,5000); await wait(p,1500);
    await smoothScroll(p,4200,5000); await wait(p,2000);
 },
};

const b = await chromium.launch();
for (const [id, fn] of Object.entries(SCENES)){
  const ctx = await b.newContext({ viewport:VP, deviceScaleFactor:1, recordVideo:{ dir:OUT, size:VP } });
  const p = await ctx.newPage();
  await p.goto(FILE); await p.waitForTimeout(500);
  const start = Date.now();
  try { await fn(p); } catch(e){ console.log('scene',id,'err',e.message); }
  const elapsed = (Date.now()-start)/1000;
  const target = TARGET[id]||18;
  if (elapsed < target) await p.waitForTimeout((target-elapsed)*1000);
  const vid = p.video();
  await ctx.close();
  const path = await vid.path();
  fs.renameSync(path, `${OUT}/${id}.webm`);
  console.log('recorded', id, 'elapsed', Math.round(elapsed)+'s -> held to', target+'s');
}
await b.close();
console.log('ALL CLIPS DONE');
