import json, threading
from pathlib import Path
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from functools import partial
from playwright.sync_api import sync_playwright
P=Path('app/src/main/assets').resolve();OUT=Path('test-results');OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*args):pass
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
  super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(P)));threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];bad=[];checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,args=['--no-sandbox'])
 page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.on('response',lambda r:bad.append(r.url) if r.status>=400 else None)
 page.goto(f'http://127.0.0.1:{server.server_port}/index.html');page.screenshot(path=str(OUT/'overview.png'))
 assert page.locator('#overview').is_visible() and not page.locator('#tutorial').is_visible()
 page.click('#start');assert page.locator('#tutorial').is_visible() and not page.locator('#overview').is_visible()
 page.click('#next');assert page.locator('#stepTitle').inner_text()=='修4台泄漏通风机'
 page.wait_for_function('document.querySelector("#stepPhoto").complete && document.querySelector("#stepPhoto").naturalWidth>0')
 page.screenshot(path=str(OUT/'tutorial.png'));checks.append('Overview hidden after start; source image loads')
 page.eval_on_selector('#tutorialBody','e=>e.scrollTop=e.scrollHeight');page.click('#next');assert page.eval_on_selector('#tutorialBody','e=>e.scrollTop')==0
 checks.append('Next-step content scroll resets to zero; footer remains visible')
 page.click('#openNotes');page.locator('#freeNotes').fill('恢复测试：本局密码 0245');page.click('#closeModal')
 page.reload();page.click('#start');assert page.locator('#stepTitle').inner_text()=='启动 Rushmore'
 page.click('#openNotes');assert page.locator('#freeNotes').input_value()=='恢复测试：本局密码 0245';page.click('#closeModal');checks.append('Progress and notes persist after reload')
 for game,keys in page.evaluate('Object.entries(window.ZOMBIE_GAMES).map(([k,v])=>[k,v.maps])'):
  page.click('#backOverview') if page.locator('#tutorial').is_visible() else None
  page.locator('#games button').filter(has_text={'bo1':'COD7','bo2':'COD9','bo3':'COD12','bo4':'COD15'}[game]).click()
  for key in keys:
   page.select_option('#maps',key);page.click('#start');assert page.locator('#stepTitle').inner_text()
   assert page.eval_on_selector('#tutorialBody','e=>e.scrollTop')==0
   assert page.locator('#next').bounding_box()['y']<844
   a=page.evaluate('window.GuideDebug.currentPhotos().length')
   if a:page.wait_for_function('document.querySelector("#stepPhoto").complete && document.querySelector("#stepPhoto").naturalWidth>0')
   page.click('#backOverview')
 checks.append('All 41 map overview/start/first-step navigation works')
 page.evaluate('window.GuideDebug.goMap("bo2_tranzit")');page.select_option('#branch','Maxis');page.click('#start');page.click('#next');assert '[Maxis]' in page.locator('#stepTitle').inner_text();page.click('#backOverview');checks.append('BO2 branch filtering works')
 page.evaluate('window.GuideDebug.goMap("alpha")');page.click('#galleryOverview');assert page.locator('.thumb').count()==50;page.locator('.thumb').nth(2).click();page.click('#zoomIn');assert page.locator('#fullImage').get_attribute('style')=='width: 150%;';page.click('#imageBack');assert page.locator('.thumb').count()==50;checks.append('All 50 Alpha images available; zoom and gallery return work')
 page.click('#closeModal');page.click('#start');page.click('#openIndex');page.locator('#modalBody .previewItem').nth(3).click();page.wait_for_function('document.querySelector("#stepPhoto").complete');page.screenshot(path=str(OUT/'tv-step.png'))
 assert not page.locator('#overview').is_visible();assert page.locator('#photoCount').inner_text()=='2 张'
 assert not errors,errors;assert not bad,bad
 data={'checks':checks,'pageErrors':errors,'httpErrors':bad,'imageReferences':page.evaluate('COMMUNITY_MEDIA.references'),'uniqueImages':page.evaluate('COMMUNITY_MEDIA.uniqueImages'),'mapCount':page.evaluate('Object.keys(ZOMBIE_DATA).length')};(OUT/'ui-tests.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));print(json.dumps(data,ensure_ascii=False,indent=2));browser.close()
server.shutdown()
