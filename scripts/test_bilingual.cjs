const {chromium}=require('../.tools/browser/node_modules/playwright-core');
const assert=require('node:assert/strict');
(async()=>{
 const browser=await chromium.launch({executablePath:'C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe',headless:true});
 const page=await browser.newPage({viewport:{width:1440,height:1000}});
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const base=process.env.BLOG_URL || 'http://127.0.0.1:8877';
 const pairs=[['/','/en/'],['/about/','/en/about/'],['/projects/','/en/projects/'],['/archives/','/en/archives/'],['/search/','/en/search/'],['/tags/','/en/tags/'],['/posts/hello-world/','/en/posts/hello-world/'],['/posts/my-first-post/','/en/posts/my-first-post/'],['/posts/learning-map/','/en/posts/learning-map/']];
 for(const [zh,en] of pairs){
  await page.goto(base+zh,{waitUntil:'networkidle'});
  assert.equal(await page.locator('html').getAttribute('lang'),'zh-CN');
  assert.equal(await page.locator('.language-switcher a[data-language=en]').getAttribute('href'),en);
  await page.locator('.language-switcher a[data-language=en]').click();
  await page.waitForLoadState('networkidle');
  assert.equal(new URL(page.url()).pathname,en);
  assert.equal(await page.locator('html').getAttribute('lang'),'en-US');
  assert.equal(await page.locator('.language-switcher a[data-language=zh]').getAttribute('href'),zh);
  assert.equal(await page.locator('#check-site-update').innerText(),'Check for updates');
  const text=(await page.locator('main').innerText()).replaceAll('简体中文','');
  assert.ok(!/[\u4e00-\u9fff]/.test(text),'Chinese text leaked into English page: '+en);
 }
 await page.goto(base+'/en/',{waitUntil:'networkidle'});
 assert.deepEqual(await page.locator('#menu a span').allTextContents(),['Posts','Archive','Search','Tags','Projects','About']);
 assert.ok((await page.locator('.home-links .social-icons a[title=Rss]').getAttribute('href')).endsWith('/en/index.xml'));
 await page.locator('#theme-toggle').click();
 await page.locator('.language-switcher a[data-language=zh]').click();
 await page.waitForLoadState('networkidle');
 assert.equal(await page.locator('html').getAttribute('data-theme'),'dark');
 await page.locator('#theme-toggle').click();
 await page.goto(base+'/en/search/',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>!document.querySelector('#searchInput').disabled);
 await page.locator('#searchInput').fill('My First Article');
 await page.waitForFunction(()=>document.querySelector('#searchResults').textContent.includes('My First Article'));
 const results=await page.locator('#searchResults a').evaluateAll(links=>links.map(link=>new URL(link.href).pathname));
 assert.ok(results.every(x=>x.startsWith('/en/')));
 await page.goto(base+'/search/',{waitUntil:'networkidle'});
 await page.waitForFunction(()=>!document.querySelector('#searchInput').disabled);
 await page.locator('#searchInput').fill('我的第一篇文章');
 await page.waitForFunction(()=>document.querySelector('#searchResults').textContent.includes('我的第一篇文章'));
 const chineseResults=await page.locator('#searchResults a').evaluateAll(links=>links.map(link=>new URL(link.href).pathname));
 assert.ok(chineseResults.every(x=>!x.startsWith('/en/')));
 for(const width of [390,320]){
  await page.setViewportSize({width,height:844});
  for(const route of ['/','/en/','/en/posts/hello-world/']){
   await page.goto(base+route,{waitUntil:'networkidle'});
   assert.ok(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth+1),'Mobile overflow: '+route+' at '+width);
  }
 }
 await page.setViewportSize({width:1440,height:1000});
 await page.goto(base+'/en/',{waitUntil:'networkidle'});
 await page.screenshot({path:'.tools/home-english.png',fullPage:true});
 await page.setViewportSize({width:390,height:844});
 await page.screenshot({path:'.tools/home-english-mobile.png',fullPage:true});
 assert.deepEqual(errors,[]);
 console.log(JSON.stringify({status:'PASS',translationPairs:pairs.length,englishContent:true,languageSpecificSearch:true,themePersists:true,mobileWidths:[390,320],consoleErrors:errors}));
 await browser.close();
})().catch(error=>{console.error(error);process.exit(1)});
