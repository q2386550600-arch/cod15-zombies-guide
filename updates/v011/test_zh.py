import json,threading,time,shutil
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
P=Path('app/src/main/assets').resolve();O=Path('test-results');O.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
  super().do_GET()
s=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(P)));threading.Thread(target=s.serve_forever,daemon=True).start()
def ready(page,sel):
 end=time.monotonic()+15
 while time.monotonic()<end:
  if page.locator(sel).evaluate('e=>e.complete&&e.naturalWidth>0'):return
  time.sleep(.05)
 raise AssertionError('Image failed: '+sel)
errors=[];checks=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox']);page=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True)
 page.on('pageerror',lambda e:errors.append(str(e)));page.goto(f'http://127.0.0.1:{s.server_port}/index.html')
 page.evaluate('localStorage.setItem("cod-guide-image-language",JSON.stringify("en"))');page.reload()
 data=page.evaluate('(()=>{const missing=[];let count=0;for(const [m,s]of Object.entries(COMMUNITY_MEDIA.maps)){for(const p of COMMUNITY_MEDIA.guides[s.guide].images){const i=ZhDisplay.info(m,p);count++;if(!/[\\u4e00-\\u9fff]/.test(i.title)||!/[\\u4e00-\\u9fff]/.test(i.action)||!ZH_LOCALE.headings[p.last_heading])missing.push([m,p.index,i]);}}return {count,missing};})()')
 assert not data['missing'],data['missing'][:3];checks.append('All connected image entries have Chinese title/action and translated section headings')
 page.evaluate('GuideDebug.goMap("bo2_buried")');page.click('#galleryOverview');assert page.locator('.thumb').count()==25
 ready(page,'.thumb img >> nth=0');page.screenshot(path=str(O/'chinese-gallery.png'))
 page.locator('.thumb').nth(4).click();ready(page,'#fullImage')
 assert page.locator('#fullPlace').inner_text().startswith('卫星碟')
 assert '酒馆（Saloon）上层阳台' in page.locator('#imageWhere').inner_text()
 assert page.locator('#fullAction').inner_text().startswith('捡起')
 assert '断头台（Guillotine）' in page.locator('#fullAction').inner_text()
 assert page.locator('#viewerNext').inner_text()=='下一张 ›'
 page.screenshot(path=str(O/'chinese-viewer.png'));checks.append('Buried satellite image defaults to Chinese; proper names are English parentheses')
 page.click('#viewerNext');assert page.locator('#fullPlace').inner_text().startswith('线圈');page.click('#viewerPrev')
 page.click('#glossaryToggle');assert '（Saloon）' not in page.locator('#imageWhere').inner_text();assert page.locator('#glossaryToggle').inner_text()=='英文名称：关'
 page.click('#glossaryToggle');page.click('#zoomIn');page.click('#viewerNext');assert page.locator('#fullImage').get_attribute('style')=='width: 100%;'
 page.click('#closeModal');assert page.locator('.thumb').count()==25;page.click('#closeModal')
 checks.append('Previous/next, zoom reset, supplementary-name toggle and gallery return work')
 page.evaluate('GuideDebug.goMap("alpha")');page.click('#start');page.click('#next');page.click('#openNotes');page.locator('#freeNotes').fill('中文语言修正：保留记录');page.click('#closeModal');page.reload();page.click('#start');assert page.locator('#stepTitle').inner_text()=='修4台泄漏通风机';page.click('#openNotes');assert page.locator('#freeNotes').input_value()=='中文语言修正：保留记录';page.click('#closeModal')
 page.click('#next');assert page.locator('#tutorialBody').evaluate('e=>e.scrollTop')==0
 checks.append('Steps and notes persist; next step resets scroll')
 assert not errors,errors
 report={'passed':True,'checks':checks,'connectedImageEntries':data['count'],'pageErrors':errors};(O/'chinese-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False));b.close()
s.shutdown()
