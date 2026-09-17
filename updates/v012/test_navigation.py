import json,threading,time,os
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
A=Path('app/src/main/assets').resolve();OUT=Path('test-results');OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
  super().do_GET()
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory=str(A)));threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];http=[];report={'checks':[]}
def ready(page,sel='#fullImage'):
 end=time.monotonic()+15
 while time.monotonic()<end:
  if page.locator(sel).evaluate('(im)=>im.complete&&im.naturalWidth>0'):return
  time.sleep(.05)
 raise AssertionError('Image decode failed '+str(page.locator(sel).get_attribute('src')))
def swipe(page,sel,dx=-150,dy=0):
 page.locator(sel).evaluate('''(e,a)=>{const r=e.getBoundingClientRect();const x=r.x+r.width*.7,y=r.y+Math.min(r.height/2,50);const t=new Touch({identifier:1,target:e,clientX:x,clientY:y});e.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[t]}));e.dispatchEvent(new TouchEvent('touchend',{bubbles:true,changedTouches:[new Touch({identifier:1,target:e,clientX:x+a.dx,clientY:y+a.dy})]}));}''',{'dx':dx,'dy':dy})
try:
 with sync_playwright() as p:
  browser=p.chromium.launch(headless=True,args=['--no-sandbox']);page=browser.new_page(viewport={'width':390,'height':844},device_scale_factor=1,has_touch=True)
  page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:http.append(r.url) if r.status>=400 else None);page.goto(f'http://127.0.0.1:{server.server_port}/index.html')
  page.evaluate('GuideDebug.goMap("bo2_buried")');page.click('#start');page.click('#next')
  assert '位置：' in page.locator('#photoLocation').inner_text();assert '蓝色' in page.locator('#photoLocation').inner_text();assert '酒馆' in page.locator('#pointMapLinks').inner_text()
  page.locator('#photoLocation').scroll_into_view_if_needed();page.screenshot(path=str(OUT/'step-location.png'));report['checks'].append('Location and matched building/floor maps visible without enlarging photo')
  page.locator('#pointMapLinks button').filter(has_text='酒馆分层').first.click();ready(page);assert '酒馆分层' in page.locator('#fullPlace').inner_text()
  page.click('#viewerNext');ready(page);page.click('#closeModal');assert '地图与楼层' in page.locator('#modalTitle').inner_text();page.screenshot(path=str(OUT/'atlas.png'));page.click('#closeModal');assert page.locator('#modal').is_hidden();report['checks'].append('Building plan and atlas return preserve current tutorial')
  page.click('#allGallery');assert page.locator('.thumb').count()==25;assert page.locator('.thumbContext').count()==25;assert '位置：' in page.locator('.thumb').nth(4).inner_text() and '怎么找：' in page.locator('.thumb').nth(4).inner_text()
  page.screenshot(path=str(OUT/'location-gallery.png'));page.locator('.thumb').nth(4).click();ready(page)
  before=page.locator('#viewerNumber').inner_text();swipe(page,'#fullAction');assert page.locator('#viewerNumber').inner_text()!=before
  page.click('#zoomIn');before=page.locator('#viewerNumber').inner_text();swipe(page,'#fullCaption');assert page.locator('#viewerNumber').inner_text()!=before
  page.click('#zoomIn');before=page.locator('#viewerNumber').inner_text();swipe(page,'#fullImage');assert page.locator('#viewerNumber').inner_text()==before;swipe(page,'#fullAction',0,140);assert page.locator('#viewerNumber').inner_text()==before
  page.click('#zoomFit');page.locator('#fullAction').scroll_into_view_if_needed();page.screenshot(path=str(OUT/'full-page-swipe.png'));report['checks'].append('Whole-page text swipes switch photos; vertical gestures and zoomed-image panning do not')
  page.click('#closeModal');page.click('#closeModal');page.click('#sourceStep');assert page.locator('.sourceChapter').count()==19
  page.locator('.sourceChapter').filter(has_text='无限回合').first.click();assert '十二行' in page.locator('#modalBody').inner_text();assert page.locator('a.sourceLink').first.get_attribute('href').endswith('#round-infinity');report['checks'].append('All Buried headings accessible; source discrepancy and complete publisher page exposed')
  page.click('#closeModal');page.click('#closeModal');page.click('#backOverview')
  for key in page.evaluate('Object.keys(ZOMBIE_DATA)'):
   page.evaluate('(k)=>GuideDebug.goMap(k)',key);page.click('#start');assert page.locator('#stepTitle').inner_text();assert page.locator('#tutorialBody').evaluate('e=>e.scrollTop')==0
   if page.locator('#sourceStep').is_enabled():page.click('#sourceStep');assert page.locator('.sourceChapter').count()>0;page.click('#closeModal')
   page.click('#backOverview')
  report['checks'].append('All 41 map start screens and source-index navigation work')
  page.evaluate('GuideDebug.goMap("bo2_origins")');page.click('#start');assert page.locator('#stepDetails .detailJump').count()>=4
  page.click('#openNotes');page.locator('#freeNotes').fill('导航版保存测试');page.click('#closeModal');page.click('#next');page.reload();page.click('#start');page.click('#openNotes');assert page.locator('#freeNotes').input_value()=='导航版保存测试';page.click('#closeModal');report['checks'].append('Staff subchapters accessible; progress and notes persist')
  audit=json.loads((A/'navigation-audit.json').read_text());assert audit['headings']==541 and audit['sourceImageReferences']==1170 and audit['originalCommunityPlans']==134
  assert not errors,errors;assert not http,http;report.update({'passed':True,'pageErrors':errors,'httpErrors':http,'audit':audit});browser.close()
finally:
 report.setdefault('passed',False);(OUT/'navigation-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));server.shutdown();print(json.dumps(report,ensure_ascii=False,indent=2))
