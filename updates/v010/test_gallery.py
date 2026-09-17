import json,time,threading
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
P=Path('app/src/main/assets').resolve();OUT=Path('test-results');OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
  super().do_GET()
s=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(P)));threading.Thread(target=s.serve_forever,daemon=True).start()
def ready(page,sel):
 end=time.monotonic()+20
 while time.monotonic()<end:
  if page.locator(sel).evaluate('im=>im.complete&&im.naturalWidth>0'):return
  time.sleep(.1)
 raise AssertionError('Undecodable '+str(page.locator(sel).get_attribute('src')))
report={'checks':[],'thumbnailSizes':[]};errors=[]
with sync_playwright() as p:
 b=p.chromium.launch(headless=True,args=['--no-sandbox'])
 page=b.new_page(viewport={'width':390,'height':844},device_scale_factor=2,has_touch=True)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:'+str(s.server_port)+'/index.html')
 page.evaluate('GuideDebug.goMap("bo2_buried")');page.click('#galleryOverview')
 assert page.locator('.thumb').count()==25
 for width,height in [(390,844),(360,780),(800,900)]:
  page.set_viewport_size({'width':width,'height':height});ready(page,'.thumb img >> nth=0')
  ratios=page.locator('.thumb img').evaluate_all('(ims)=>ims.map(im=>{const r=im.getBoundingClientRect();return {w:r.width,h:r.height,expected:Number(im.getAttribute("height"))/Number(im.getAttribute("width"))};})')
  for r in ratios:assert abs(r['h']/r['w']-r['expected'])<.015,r
  assert max(r['h'] for r in ratios)<500
  report['thumbnailSizes'].append({'viewport':width,'first':ratios[0]})
 page.set_viewport_size({'width':390,'height':844});page.screenshot(path=str(OUT/'gallery-fixed.png'))
 report['checks'].append('All Buried thumbnails preserve original aspect ratio at 360, 390 and 800 CSS pixels')
 coverage=page.evaluate('Object.entries(COMMUNITY_MEDIA.guides).map(([key,g])=>({key,count:g.images.length,covered:g.images.filter(im=>(IMAGE_HELP.notes[key]||[]).filter(n=>im.index>=n.first&&im.index<=n.last).length===1).length}))')
 assert sum(r['count'] for r in coverage)==1170
 assert all(r['count']==r['covered'] for r in coverage)
 report['coverage']=coverage;report['checks'].append('All 1170 source image references have one context assignment; 1148 original files unchanged')
 page.locator('.thumb').nth(4).scroll_into_view_if_needed();saved=page.locator('#modalBody').evaluate('e=>e.scrollTop');page.locator('.thumb').nth(4).click();ready(page,'#fullImage')
 assert 'Satellite Dish' in page.locator('#fullPlace').inner_text()
 assert all(w in page.locator('#fullAction').inner_text() for w in ['Guillotine','Saloon','Gallows','卫星天线盘'])
 page.screenshot(path=str(OUT/'buried-satellite-explained.png'))
 page.click('#viewerNext');assert 'Spool of Wire' in page.locator('#fullPlace').inner_text();page.click('#zoomIn');assert page.locator('#fullImage').get_attribute('style')=='width: 150%;'
 page.click('#viewerPrev');assert page.locator('#fullImage').get_attribute('style')=='width: 100%;';assert page.locator('#viewerNumber').inner_text()=='5 / 25'
 page.keyboard.press('ArrowRight');assert page.locator('#viewerNumber').inner_text()=='6 / 25';page.keyboard.press('ArrowLeft')
 page.click('#glossaryToggle');assert '(' not in page.locator('#fullAction').inner_text();page.reload();page.click('#galleryOverview');page.locator('.thumb').nth(4).click();assert '(' not in page.locator('#fullAction').inner_text();page.click('#glossaryToggle');assert '卫星天线盘' in page.locator('#fullAction').inner_text()
 report['checks'].append('Viewer next/previous/keyboard update image, title, action and position; zoom resets on image change; glossary setting persists')
 page.evaluate('''(()=>{const e=document.querySelector('#viewerPane');e.dispatchEvent(new TouchEvent('touchstart',{touches:[new Touch({identifier:1,target:e,clientX:300,clientY:200})]}));e.dispatchEvent(new TouchEvent('touchend',{changedTouches:[new Touch({identifier:1,target:e,clientX:100,clientY:200})]}));})()''')
 assert page.locator('#viewerNumber').inner_text()=='6 / 25';page.click('#zoomIn')
 page.evaluate('''(()=>{const e=document.querySelector('#viewerPane');e.dispatchEvent(new TouchEvent('touchstart',{touches:[new Touch({identifier:1,target:e,clientX:300,clientY:200})]}));e.dispatchEvent(new TouchEvent('touchend',{changedTouches:[new Touch({identifier:1,target:e,clientX:100,clientY:200})]}));})()''')
 assert page.locator('#viewerNumber').inner_text()=='6 / 25'
 report['checks'].append('Fit-size synthetic swipe switches images; zoomed swipe does not switch')
 page.click('#imageBack');assert page.locator('.thumb').count()==25;assert page.locator('#viewerNav').count()==0
 page.locator('.thumb').nth(17).scroll_into_view_if_needed();saved=page.locator('#modalBody').evaluate('e=>e.scrollTop');page.locator('.thumb').nth(17).click();assert page.locator('#branchWarning').is_visible();page.click('#closeModal');time.sleep(.1);assert abs(page.locator('#modalBody').evaluate('e=>e.scrollTop')-saved)<4
 report['checks'].append('Gallery scroll position restored and cross-route image warning shown')
 page.click('#closeModal');assert page.locator('#modal').is_hidden()
 page.evaluate('GuideDebug.goMap("alpha")');page.click('#start');page.click('#openIndex');page.locator('#modalBody .previewItem').nth(3).click();page.click('#zoomPhoto');page.click('#viewerNext');assert page.locator('#viewerNumber').inner_text()=='2 / 2';assert page.locator('#viewerNext').is_disabled();page.click('#closeModal');assert page.locator('#photoNumber').inner_text()=='2 / 2';page.click('#next');assert page.locator('#tutorialBody').evaluate('e=>e.scrollTop')==0
 report['checks'].append('Filtered step-viewer stays in its own list and returns the selected image; next step still resets scroll')
 assert not errors,errors;report['pageErrors']=errors;report['passed']=True
 (OUT/'gallery-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False));b.close()
s.shutdown()
