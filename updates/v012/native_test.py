"""Android 16 test of the shipped APK with native taps and swipes."""
from pathlib import Path
exec(Path('ci/android_runtime_cdp.py').read_text().split("report={'package'")[0])
APK=Path('output/COD_Zombies_Guide_v0.12.apk');OLD=Path('.base/COD_Zombies_Guide_v0.11.apk')
report={'checks':[],'apkSha256':hashlib.sha256(APK.read_bytes()).hexdigest()};page=None

def swipe_text(selector):
 page.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center"})');time.sleep(.2)
 r=page.evaluate('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,vw:innerWidth,vh:innerHeight};})()');x0,y0,x1,y1=page.bounds
 xa=round(x0+(r['x']+r['w']*.78)*(x1-x0)/r['vw']);xb=round(x0+(r['x']+r['w']*.22)*(x1-x0)/r['vw']);yy=round(y0+(r['y']+min(r['h']/2,35))*(y1-y0)/r['vh'])
 adb('shell','input','swipe',str(xa),str(yy),str(xb),str(yy),'280')
try:
 assert adb('shell','getprop','ro.build.version.sdk')=='36'
 assert 'Success' in adb('install','-r',str(OLD));adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
 page=DevicePage();page.wait('!!window.GuideDebug','Old guide did not load');page.tap('#start');page.tap('#next');page.tap('#openNotes')
 page.evaluate('(()=>{const e=document.querySelector("#freeNotes");e.value="keep-v012-note";e.dispatchEvent(new Event("input",{bubbles:true}));})()')
 page.wait('GuideDebug.getState().notes.alpha==="keep-v012-note"','Note was not saved in old app');page.tap('#closeModal');page.close();page=None
 adb('shell','input','keyevent','KEYCODE_HOME');time.sleep(2);adb('shell','am','force-stop',PKG)
 assert 'Success' in adb('install','-r',str(APK));adb('logcat','-c');adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
 page=DevicePage();page.wait('!!window.GuideDebug','New guide did not load');assert page.evaluate('GuideDebug.getState().step')==1;assert page.evaluate('GuideDebug.getState().notes.alpha')=='keep-v012-note';report['checks'].append('v0.11 to v0.12 update preserves saved progress and notes')
 page.evaluate('GuideDebug.goMap("bo2_buried")');page.tap('#start');page.tap('#next');assert '蓝色' in page.evaluate('document.querySelector("#photoLocation").textContent')
 page.tap('#zoomPhoto');page.wait('document.querySelector("#fullImage").naturalWidth>0','Point image did not load')
 before=page.evaluate('document.querySelector("#viewerNumber").textContent');swipe_text('#fullAction');page.wait('document.querySelector("#viewerNumber").textContent!=='+json.dumps(before),'Native text-area swipe failed')
 page.tap('#zoomIn');before=page.evaluate('document.querySelector("#viewerNumber").textContent');swipe_text('#fullCaption');page.wait('document.querySelector("#viewerNumber").textContent!=='+json.dumps(before),'Non-image swipe failed while zoomed')
 snap('01-page-swipe');page.tap('#closeModal');report['checks'].append('Native text and non-image-area swipes switch pictures')
 page.tap('#openIndex');page.tap('#modalBody .previewItem:nth-child(2)');page.tap('#pointMapLinks button[data-plan-id="plan-68-1"]');page.wait('document.querySelector("#fullImage").naturalWidth>0','Offline floor plan failed');assert '酒馆' in page.evaluate('document.querySelector("#fullPlace").textContent')
 snap('02-saloon-floor-plan');page.tap('#closeModal');snap('03-atlas');page.tap('#closeModal');assert page.evaluate('document.querySelector("#modal").hidden');report['checks'].append('Offline building floorplan opens and returns to same tutorial')
 page.tap('#allGallery');page.wait('document.querySelectorAll(".thumbContext").length===25','Gallery position cards missing');assert '位置：' in page.evaluate('document.querySelector(".thumbContext").textContent');snap('04-location-gallery');page.tap('#closeModal')
 page.tap('#sourceStep');assert page.evaluate('document.querySelectorAll(".sourceChapter").length')==19;snap('05-source-index');page.tap('#closeModal');report['checks'].append('Positions and actions visible without zoom; source headings exposed')
 page.tap('#routeActions a.sourceLink');time.sleep(2);assert '.ReaderActivity' in adb('shell','dumpsys','activity','activities');snap('06-publisher-reader');adb('shell','input','keyevent','KEYCODE_BACK');time.sleep(.5)
 page.close();page=DevicePage();page.wait('!!window.GuideDebug','Local guide did not resume');assert page.evaluate('GuideDebug.getState().map')=='bo2_buried';report['checks'].append('Publisher reader Activity opens and returns without resetting tutorial')
 report['crashLog']=adb('logcat','-b','crash','-d');assert PKG not in report['crashLog'];report['passed']=True
except Exception as e:
 report['passed']=False;report['error']=repr(e)
 try:snap('failure');report['crashLog']=adb('logcat','-b','crash','-d')
 except Exception:pass
 raise
finally:
 if page:page.close()
 (OUT/'navigation-native.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
