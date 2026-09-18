import json,os,time,threading
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
OUT=Path('test-results');OUT.mkdir(exist_ok=True)
class Quiet(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
server=ThreadingHTTPServer(('127.0.0.1',0),partial(Quiet,directory='app/src/main/assets'));threading.Thread(target=server.serve_forever,daemon=True).start()
errors=[];checks=[]
with sync_playwright() as p:
 browser=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'),args=['--no-sandbox']);page=browser.new_page(viewport={'width':390,'height':844},has_touch=True)
 page.on('pageerror',lambda e:errors.append(str(e)))
 page.goto('http://127.0.0.1:'+str(server.server_port)+'/index.html');page.evaluate('GuideDebug.goMap("bo2_buried")');page.click('#galleryOverview');page.locator('.thumb').nth(4).click();assert page.evaluate('guideGestureBackend')=='pointer'
 def swipe(sel,dx=-190,dy=8):
  page.locator(sel).scroll_into_view_if_needed();r=page.locator(sel).bounding_box();y=max(0,min(780,r['y']+min(r['height']/2,45)))
  page.mouse.move(290 if dx<0 else 95,y);page.mouse.down();page.mouse.move((290 if dx<0 else 95)+dx,y+dy,steps=12);page.mouse.up();time.sleep(.45)
 for zoom in (1,1.5,2.5):
  page.click('#zoomFit')
  for n in range(round((zoom-1)*2)):page.click('#zoomIn')
  before=page.evaluate('GuideDebug.viewer().index');swipe('#viewerPane');assert page.evaluate('GuideDebug.viewer().index')==before+1
  page.click('#zoomIn');before=page.evaluate('GuideDebug.viewer().index');swipe('#fullAction',dx=190);assert page.evaluate('GuideDebug.viewer().index')==before-1
 checks.append('Image and text drags page exactly once at 100%, 150%, 250% zoom')
 page.click('#zoomIn');page.click('#viewerTouchMode');assert 'imagePanMode' in page.locator('#modal').get_attribute('class')
 before=page.evaluate('GuideDebug.viewer().index');swipe('#viewerPane');assert page.evaluate('GuideDebug.viewer().index')==before
 page.click('#viewerTouchMode');page.click('#viewerNext');assert page.evaluate('GuideDebug.viewer().index')==before+1
 checks.append('Explicit pan mode disables paging; next button and mode restoration work');page.screenshot(path=str(OUT/'viewer.png'))
 page.click('#closeModal');page.click('#closeModal');page.evaluate('GuideDebug.goMap("bo2_origins")');page.click('#start');page.click('#next');pos=page.evaluate('GuideDebug.detailPos()');page.reload();page.click('#start');assert page.evaluate('GuideDebug.detailPos()')==pos
 checks.append('Tutorial micro-position survives reload');assert not errors,errors
 (OUT/'browser-gestures.json').write_text(json.dumps({'passed':True,'checks':checks,'errors':errors},ensure_ascii=False,indent=2));print(json.dumps({'passed':True,'checks':checks}));browser.close()
server.shutdown()
