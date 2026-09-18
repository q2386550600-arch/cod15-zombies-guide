"""Native Android swipes; no dispatchEvent or paging calls for assertions."""
from pathlib import Path
exec(Path('ci/android_runtime_cdp.py').read_text().split("report={'package'")[0])
APK=Path('output/COD_Zombies_Guide_v0.13.1.apk');OLD=Path('.base/COD_Zombies_Guide_v0.13.apk')
report={'checks':[],'swipes':[],'apkSha256':hashlib.sha256(APK.read_bytes()).hexdigest()};page=None

def swipe(selector,left=True,duration=300,vertical=False):
 page.evaluate('document.querySelector('+json.dumps(selector)+').scrollIntoView({block:"center"})');time.sleep(.2)
 r=page.evaluate('(()=>{const r=document.querySelector('+json.dumps(selector)+').getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,vw:innerWidth,vh:innerHeight};})()');x0,y0,x1,y1=page.bounds
 if vertical:ax=bx=r['x']+r['w']*.5;ay=r['y']+min(r['h']*.7,80);by=ay-130
 else:ax=r['x']+r['w']*(.78 if left else .22);bx=r['x']+r['w']*(.22 if left else .78);ay=r['y']+min(r['h']/2,50);by=ay+8
 coords=[round(x0+ax*(x1-x0)/r['vw']),round(y0+ay*(y1-y0)/r['vh']),round(x0+bx*(x1-x0)/r['vw']),round(y0+by*(y1-y0)/r['vh'])]
 adb('shell','input','swipe',*map(str,coords),str(duration));time.sleep(.5)
def ix():return page.evaluate('GuideDebug.viewer().index')
def zoom_to(value):
 page.tap('#zoomFit')
 for i in range(round((value-1)*2)):page.tap('#zoomIn')
 assert page.evaluate('GuideDebug.viewer().zoom')==value
try:
 report['sdk']=adb('shell','getprop','ro.build.version.sdk');assert report['sdk']=='36'
 assert 'Success' in adb('install','-r',str(OLD));adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
 page=DevicePage();page.wait('!!window.GuideDebug','Previous app not ready');page.tap('#start');page.tap('#next');page.tap('#openNotes')
 page.evaluate('(()=>{const e=document.querySelector("#freeNotes");e.value="gesture-hotfix-keep";e.dispatchEvent(new Event("input",{bubbles:true}));})()');old=page.evaluate('GuideDebug.getState()');page.close();page=None
 adb('shell','input','keyevent','KEYCODE_HOME');time.sleep(1);adb('shell','am','force-stop',PKG)
 assert 'Success' in adb('install','-r',str(APK));adb('logcat','-c');adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
 page=DevicePage();page.wait('!!window.GuideDebug','Hotfix not ready');assert page.evaluate('guideGestureBackend')=='android'
 new=page.evaluate('GuideDebug.getState()');assert new['notes']==old['notes'] and new['detailPositions']==old['detailPositions'];report['checks'].append('v0.13 to v0.13.1 upgrade preserves notes and micro-steps')
 page.evaluate('GuideDebug.goMap("bo2_buried")');page.tap('#galleryOverview');page.tap('.thumb[data-image-index="4"]');page.wait('document.querySelector("#fullImage").naturalWidth>0','Image failed')
 for z in [1,1.5,2.5]:
  for selector in ['#viewerPane','#fullAction']:
   zoom_to(z);before=ix();swipe(selector,True,300);assert ix()==before+1,(z,selector,before,ix())
   zoom_to(z);before=ix();swipe(selector,False,1000);assert ix()==before-1,(z,selector,before,ix())
   report['swipes'].append({'zoom':z,'area':selector,'bothDirections':True,'exactlyOneImage':True})
 report['checks'].append('Twelve native swipes: image and text at 100%,150%,250%; fast/slow; left/right; exactly one image')
 zoom_to(2.5);before=ix();swipe('#fullAction',duration=600,vertical=True);assert ix()==before;report['checks'].append('Vertical reading does not page')
 page.tap('#viewerTouchMode');before=ix();swipe('#viewerPane');assert ix()==before;assert page.evaluate('document.querySelector("#viewerPane").scrollLeft')>0
 page.tap('#viewerTouchMode');swipe('#viewerPane');assert ix()==before+1;report['checks'].append('Explicit image-move mode pans; browse mode restores paging')
 zoom_to(1.5);snap('zoomed-viewer-swipe-enabled');page.tap('#closeModal');page.tap('#closeModal');page.evaluate('GuideDebug.goMap("bo2_origins")');page.tap('#start');page.tap('#next');saved=page.evaluate('GuideDebug.detailPos()')
 page.close();page=None;adb('shell','input','keyevent','KEYCODE_HOME');time.sleep(1);adb('shell','am','force-stop',PKG);adb('shell','am','start','-W','-n',PKG+'/.MainActivity');page=DevicePage();page.wait('!!window.GuideDebug','Relaunch failed');page.tap('#start');assert page.evaluate('GuideDebug.detailPos()')==saved;report['checks'].append('Tutorial position survives native relaunch')
 report['crashLog']=adb('logcat','-b','crash','-d');assert PKG not in report['crashLog'];report['passed']=True
except Exception as e:
 report['passed']=False;report['error']=repr(e)
 try:snap('failure');report['crashLog']=adb('logcat','-b','crash','-d')
 except Exception:pass
 raise
finally:
 if page:page.close()
 (OUT/'native-gestures.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
