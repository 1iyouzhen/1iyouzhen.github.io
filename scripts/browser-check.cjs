const { chromium } = require('../.tools/browser/node_modules/playwright-core');
const path = require('path');
const assert = require('assert/strict');
(async () => {
 const browser = await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const context = await browser.newContext({viewport:{width:1440,height:1100},colorScheme:'light'});
 const page = await context.newPage();
 const errors=[]; page.on('pageerror',e=>errors.push(e.message));
 page.on('response',r=>{if(r.status()>=400 && r.url().startsWith('http://127.0.0.1:8765')) errors.push(r.status()+' '+r.url())});
 const base=process.env.BLOG_URL || 'http://127.0.0.1:8765';
 await page.goto(base+'/',{waitUntil:'networkidle'});
 await page.locator('.home-info').waitFor();
 assert.equal(await page.locator('.post-entry').count(),2);
 assert.equal(await page.locator('#menu a').count(),6);
 await page.screenshot({path:path.resolve('.tools/home-desktop.png'),fullPage:true});
 await page.locator('#theme-toggle').click();
 assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
 const dark = await page.evaluate(()=>getComputedStyle(document.documentElement).getPropertyValue('--theme').trim());
 assert.equal(dark,'#171c26');
 await page.reload({waitUntil:'networkidle'});
 assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
 await page.screenshot({path:path.resolve('.tools/home-dark.png'),fullPage:true});
 await page.locator('#theme-toggle').click();
 await page.goto(base+'/search/',{waitUntil:'networkidle'});
 await page.locator('#searchInput').waitFor({state:'visible'});
 await page.waitForFunction(()=>!document.querySelector('#searchInput').disabled);
 await page.locator('#searchInput').fill('LLM');
 await page.waitForFunction(()=>document.querySelectorAll('#searchResults li').length>0);
 const results=await page.locator('#searchResults li').count();
 await page.screenshot({path:path.resolve('.tools/search.png'),fullPage:true});
 await page.goto(base+'/posts/hello-world/',{waitUntil:'networkidle'});
 assert.ok(await page.locator('.toc').count());
 assert.ok(await page.locator('.post-content').innerText());
 await page.screenshot({path:path.resolve('.tools/article.png'),fullPage:true});
 for(const route of ['/archives/','/tags/','/projects/','/about/']) {
  const response=await page.goto(base+route,{waitUntil:'networkidle'}); assert.equal(response.status(),200);
  assert.ok(await page.locator('h1').innerText());
 }
 await page.setViewportSize({width:390,height:844});
 for(const route of ['/','/posts/hello-world/','/projects/','/search/']) {
  await page.goto(base+route,{waitUntil:'networkidle'});
  const overflow=await page.evaluate(()=>({width:document.documentElement.scrollWidth,viewport:innerWidth}));
  assert.ok(overflow.width<=overflow.viewport+1,route+' overflows: '+JSON.stringify(overflow));
  if(route==='/') await page.screenshot({path:path.resolve('.tools/home-mobile.png'),fullPage:true});
 }
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({status:'PASS',searchResults:results,pages:8,mobileWidths:390,darkThemePersistence:true,consoleErrors:errors,screenshots:['.tools/home-desktop.png','.tools/home-dark.png','.tools/home-mobile.png','.tools/search.png','.tools/article.png']}));
 await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
