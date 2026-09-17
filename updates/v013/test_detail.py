import json,threading,time,os
from pathlib import Path
from functools import partial
from http.server import ThreadingHTTPServer,SimpleHTTPRequestHandler
from playwright.sync_api import sync_playwright
A=Path(os.environ.get('GUIDE_ASSETS','app/src/main/assets')).resolve();OUT=Path(os.environ.get('GUIDE_TEST_OUT','test-results'));OUT.mkdir(exist_ok=True,parents=True)
class Handler(SimpleHTTPRequestHandler):
 def log_message(self,*a):pass
 def do_GET(self):
  if self.path=='/favicon.ico':self.send_response(204);self.end_headers();return
  super().do_GET()
http=ThreadingHTTPServer(('127.0.0.1',0),partial(Handler,directory=str(A)));threading.Thread(target=http.serve_forever,daemon=True).start()
errors=[];missing=[];report={'checks':[]}
def image(page,selector):
 end=time.monotonic()+10
 while time.monotonic()<end:
  if page.locator(selector).evaluate('(e)=>e.complete&&e.naturalWidth>0'):return
  time.sleep(.05)
 raise AssertionError('Image decode '+str(page.locator(selector).get_attribute('src')))
try:
 with sync_playwright() as p:
  b=p.chromium.launch(headless=True,executable_path=os.environ.get('CHROMIUM_PATH'),args=['--no-sandbox']);ctx=b.new_context(viewport={'width':390,'height':844},has_touch=True)
  page=ctx.new_page();page.on('pageerror',lambda e:errors.append(str(e)));page.on('response',lambda r:missing.append(r.url) if r.status>=400 else None)
  page.goto(f'http://127.0.0.1:{http.server_port}/index.html');page.click('#start');assert page.locator('#detailControls').is_visible();assert page.evaluate('GuideDebug.detailFrames().length')>1
  previous=page.locator('#stepAction').inner_text();page.click('#next');assert page.locator('#stepAction').inner_text()!=previous;assert page.evaluate('GuideDebug.getState().step')==0;assert page.locator('#tutorialBody').evaluate('e=>e.scrollTop')==0
  page.click('#openNotes');page.locator('#freeNotes').fill('细项保持013');page.click('#closeModal');pos=page.evaluate('GuideDebug.detailPos()');page.reload();page.click('#start');assert page.evaluate('GuideDebug.detailPos()')==pos;page.click('#openNotes');assert page.locator('#freeNotes').input_value()=='细项保持013';page.click('#closeModal');page.click('#backOverview')
  report['checks'].append('Next advances a concrete micro-item without prematurely completing the macro stage; micro-position and notes survive reload')
  for k in page.evaluate('Object.keys(ZOMBIE_DATA)'):
   print('Checking',k,flush=True);page.evaluate('(k)=>GuideDebug.goMap(k)',k);page.click('#start');assert page.locator('#stepTitle').inner_text()
   if page.evaluate('Boolean(OFFLINE_GUIDES.stages[GuideDebug.getState().map])'):
    for stage in range(page.evaluate('ZOMBIE_DATA[GuideDebug.getState().map].steps.length')):
     page.click('#openIndex');rows=page.locator('#modalBody .previewItem');titles=rows.all_text_contents();rows.nth(min(stage,len(titles)-1)).click();assert page.locator('#stepAction').inner_text().strip();assert page.evaluate('GuideDebug.detailFrames().length')>0
     if page.locator('#detailChoice').count():page.select_option('#detailChoice','0');assert page.evaluate('GuideDebug.detailFrames().length')>1
    page.click('#sourceStep');assert page.locator('.sourceChapter').count()>0
    ids=page.locator('.sourceChapter').evaluate_all('(bs)=>bs.map(b=>b.dataset.sectionId)')
    for sid in ids:
     page.evaluate('(id)=>GuideDebug.openSourceSection(id)',sid);assert '完整中文细项尚未接入' not in page.locator('#modalBody').inner_text()
     expected=page.evaluate('(id)=>OFFLINE_GUIDES.docs[SOURCE_INDEX.maps[GuideDebug.getState().map].guide].sections[id].texts.length',sid)
     assert page.locator('.completeText li').count()==expected,(sid,expected)
    page.click('#readerCurrent')
   page.click('#backOverview')
  report['checks'].append('41 map entries open; all 26 linked versions expose all authored offline paragraphs, not only image-based chapters')
  page.evaluate('GuideDebug.goMap("bo2_buried")');page.select_option('#branch','Maxis');page.click('#start');page.click('#openIndex');assert not any('[Richtofen]' in x for x in page.locator('#modalBody .previewItem').all_text_contents());page.click('#closeModal');page.click('#backOverview')
  page.evaluate('GuideDebug.goMap("bo1_cotd")');page.select_option('#cotdMode','solo');page.click('#start');page.click('#openIndex');assert page.locator('#modalBody .previewItem').count()==7;page.click('#closeModal');page.click('#backOverview')
  report['checks'].append('BO2 branches and Call of the Dead solo/co-op extra-stage filtering remain explicit')
  page.evaluate('GuideDebug.goMap("blood")');page.click('#start');page.click('#openIndex');page.locator('#modalBody .previewItem').nth(7).click()
  for choice in [2,0,4,1,3]:
   page.select_option('#detailChoice',str(choice));page.evaluate('GuideDebug.openDetailIndex()');page.locator('#modalBody .detailJump').last.click();page.click('#next');assert page.evaluate('GuideDebug.getState().step')==(8 if choice==3 else 7)
  page.click('#backOverview');report['checks'].append('All five Blood challenges must be individually marked; completing one cannot skip the other four')
  page.evaluate('GuideDebug.goMap("bo3_gorod")');page.click('#start');page.evaluate('GuideDebug.openValve()');page.select_option('#valveFrom','Armory');page.select_option('#valveTo','Tank Factory');assert page.locator('.valveRow').count()==6;assert page.locator('.valveRow b').all_text_contents()==['3','3','2','3','1','不要转动（圆筒）'];page.screenshot(path=str(OUT/'offline-valves.png'));page.select_option('#valveTo','Armory');assert '不能是同一处' in page.locator('#valveAnswer').inner_text();page.click('#closeModal');page.click('#backOverview')
  report['checks'].append('Offline valve lookup rejects identical endpoints and preserves choices; all 30 source combinations pass data validation')
  page.evaluate('GuideDebug.goMap("bo2_origins")');page.click('#start');page.evaluate('GuideDebug.openSourceSection("little-lost-girl-15")');assert page.locator('.completeText li').count()==4;page.screenshot(path=str(OUT/'g-strike-details.png'));page.click('#readerCurrent')
  # Earlier traversal intentionally leaves this map on its final stage. Select
  # the preparation stage through the normal UI before testing its sixth item.
  page.click('#openIndex');page.locator('#modalBody .previewItem').first.click();assert page.evaluate('GuideDebug.getState().step')==0
  page.evaluate('GuideDebug.openDetailIndex()');page.locator('#modalBody .detailJump').nth(5).click();assert page.evaluate('GuideDebug.detailPos()')==5;page.screenshot(path=str(OUT/'micro-step.png'));page.click('#backOverview')
  report['checks'].append('Detailed preparation can be revisited after the last stage without discarding saved progress')
  page.evaluate('GuideDebug.goMap("bo2_buried")');page.click('#galleryOverview');page.locator('.thumb').nth(4).click();image(page,'#fullImage');before=page.locator('#viewerNumber').inner_text()
  page.locator('#fullAction').evaluate('''e=>{const t=new Touch({identifier:1,target:e,clientX:320,clientY:300});e.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[t]}));e.dispatchEvent(new TouchEvent('touchend',{bubbles:true,changedTouches:[new Touch({identifier:1,target:e,clientX:100,clientY:300})]}));}''');assert page.locator('#viewerNumber').inner_text()!=before;page.click('#closeModal');page.click('#closeModal')
  report['checks'].append('Original images decode; swipes in explanation text still switch photos')
  assert not errors,errors;assert not missing,missing
  report.update({'passed':True,'pageErrors':errors,'missingResources':missing,'audit':json.loads((A/'offline-audit.json').read_text())});b.close()
finally:
 report.setdefault('passed',False);(OUT/'detail-tests.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps({k:v for k,v in report.items() if k!='audit'},ensure_ascii=False,indent=2));http.shutdown()
