"""Test the compiled APK, not a browser substitute. CDP locates native adb taps."""
from pathlib import Path
exec(Path('ci/android_runtime_cdp.py').read_text().split("report={'package'")[0])
APK=Path('output/COD_Zombies_Guide_v0.13.apk');OLD=Path('.base/COD_Zombies_Guide_v0.12.apk')
report={'checks':[],'apkSha256':hashlib.sha256(APK.read_bytes()).hexdigest()};page=None

def swipe_text(selector):
 page.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center"})');time.sleep(.2)
 r=page.evaluate('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,vw:innerWidth,vh:innerHeight};})()');x0,y0,x1,y1=page.bounds
 xa=round(x0+(r['x']+r['w']*.78)*(x1-x0)/r['vw']);xb=round(x0+(r['x']+r['w']*.22)*(x1-x0)/r['vw']);yy=round(y0+(r['y']+min(r['h']/2,35))*(y1-y0)/r['vh'])
 adb('shell','input','swipe',str(xa),str(yy),str(xb),str(yy),'280')
try:
 report['sdk']=adb('shell','getprop','ro.build.version.sdk');assert report['sdk']=='36'
 assert 'Success' in adb('install','-r',str(OLD));adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
 page=DevicePage();page.wait('!!window.GuideDebug','Old guide not initialized');page.tap('#start');page.tap('#next');page.tap('#openNotes')
 page.evaluate('(()=>{const e=document.querySelector("#freeNotes");e.value="keep-v013-note";e.dispatchEvent(new Event("input",{bubbles:true}));})()')
 page.wait('GuideDebug.getState().notes.alpha==="keep-v013-note"','Old note input did not save');page.tap('#closeModal');prior=page.evaluate('GuideDebug.getState()');page.close();page=None
 adb('shell','input','keyevent','KEYCODE_HOME');time.sleep(2);adb('shell','am','force-stop',PKG)
 assert 'Success' in adb('install','-r',str(APK));adb('logcat','-c');adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
 page=DevicePage();page.wait('!!window.GuideDebug && !!window.OFFLINE_GUIDES','New guide not initialized');after=page.evaluate('GuideDebug.getState()');assert after['step']==prior['step'];assert after['notes']['alpha']==prior['notes']['alpha'];assert after['done']==prior['done'];report['checks'].append('v0.12 to v0.13 in-place install preserves previous step, completion and notes')
 page.evaluate('GuideDebug.goMap("bo2_origins")');page.tap('#start');before=page.evaluate('document.querySelector("#stepAction").textContent');page.tap('#next');assert page.evaluate('GuideDebug.getState().step')==0;assert page.evaluate('GuideDebug.detailPos()')==1;assert page.evaluate('document.querySelector("#stepAction").textContent')!=before;assert page.evaluate('document.querySelector("#tutorialBody").scrollTop')==0;snap('01-micro-step');report['checks'].append('Native next tap advances one detailed item, not the entire stage, and resets scrolling')
 page.evaluate('GuideDebug.openSourceSection("little-lost-girl-15")');assert page.evaluate('document.querySelectorAll(".completeText li").length')==4;assert '踩泥' in page.evaluate('document.querySelector(".completeText").textContent');snap('02-g-strike-offline-text');page.tap('#readerCurrent');report['checks'].append('Full Chinese G-Strike preparation, transport and retry paragraphs render inside native offline WebView')
 page.evaluate('GuideDebug.goMap("bo3_gorod")');page.tap('#start');page.evaluate('GuideDebug.openValve()')
 page.evaluate('(()=>{const f=document.querySelector("#valveFrom"),t=document.querySelector("#valveTo");f.value="Armory";f.dispatchEvent(new Event("change"));t.value="Tank Factory";t.dispatchEvent(new Event("change"));})()');assert page.evaluate('document.querySelectorAll(".valveRow").length')==6;snap('03-valve-calculator');page.tap('#closeModal')
 page.evaluate('GuideDebug.goMap("bo2_buried")');page.tap('#galleryOverview');page.tap('.thumb[data-image-index="4"]');page.wait('document.querySelector("#fullImage").naturalWidth>0','Original image did not load')
 before=page.evaluate('document.querySelector("#viewerNumber").textContent');swipe_text('#fullAction');page.wait('document.querySelector("#viewerNumber").textContent!=='+json.dumps(before),'Whole-page native swipe failed');snap('04-image-swipe');page.tap('#closeModal');page.tap('#closeModal');report['checks'].append('Native text-area swipe still switches preserved screenshots')
 page.evaluate('GuideDebug.goMap("bo2_origins")');page.tap('#start');saved=page.evaluate('GuideDebug.detailPos()');page.close();page=None
 adb('shell','input','keyevent','KEYCODE_HOME');time.sleep(2);adb('shell','am','force-stop',PKG);adb('shell','am','start','-W','-n',PKG+'/.MainActivity');page=DevicePage();page.wait('!!window.GuideDebug','Relaunch failed');page.tap('#start');assert page.evaluate('GuideDebug.detailPos()')==saved;report['checks'].append('Detailed item position survives Android backgrounding, force-stop and relaunch')
 report['crashLog']=adb('logcat','-b','crash','-d');assert PKG not in report['crashLog'];report['passed']=True
except Exception as exc:
 report['passed']=False;report['error']=repr(exc)
 try:snap('failure');report['crashLog']=adb('logcat','-b','crash','-d')
 except Exception:pass
 raise
finally:
 if page:page.close()
 (OUT/'detail-native.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
