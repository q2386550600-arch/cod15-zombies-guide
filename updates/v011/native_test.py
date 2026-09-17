from pathlib import Path
# Reuse the previously verified native-tap/CDP adapter, not its old test body.
exec(Path('ci/android_runtime_cdp.py').read_text().split("report={'package'")[0])
APK=Path('output/COD_Zombies_Guide_v0.11.apk')
report={'checks':[],'apkSha256':hashlib.sha256(APK.read_bytes()).hexdigest()};page=None
try:
 assert adb('shell','getprop','ro.build.version.sdk')=='36'
 assert 'Success' in adb('install','-r','.base/COD_Zombies_Guide_v0.10.apk')
 adb('shell','am','start','-W','-n',PKG+'/.MainActivity');page=DevicePage();page.wait('!!window.GuideDebug','Old version did not initialise')
 page.tap('#start');page.tap('#next');page.wait('GuideDebug.getState().step===1','No old progress')
 page.tap('#openNotes');page.tap('#freeNotes');adb('shell','input','text','keep-011');adb('shell','input','keyevent','4');time.sleep(.5);page.tap('#closeModal')
 page.evaluate('localStorage.setItem("cod-guide-image-language",JSON.stringify("en"))')
 adb('shell','input','keyevent','3');time.sleep(3);page.close();page=None;adb('shell','am','force-stop',PKG)
 assert 'Success' in adb('install','-r',str(APK));adb('logcat','-c');adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
 page=DevicePage();page.wait('!!window.ZhDisplay&&!!window.GuideDebug','Chinese version did not initialise')
 assert page.evaluate('GuideDebug.getState().step')==1
 assert page.evaluate('GuideDebug.getState().notes.alpha')=='keep-011'
 report['checks'].append('v0.10 to v0.11 upgrade preserves step and native-entered notes')
 page.evaluate('GuideDebug.goMap("bo2_buried")');page.tap('#galleryOverview');page.wait('document.querySelector(".thumb img").naturalWidth>0','No thumbnails');snap('chinese-gallery')
 page.tap('.thumb[data-image-index="4"]');page.wait('document.querySelector("#fullImage").naturalWidth>0','No full image')
 assert page.evaluate('document.querySelector("#fullPlace").textContent.startsWith("卫星碟")')
 assert page.evaluate('document.querySelector("#fullAction").textContent.startsWith("捡起")')
 assert page.evaluate('document.querySelector("#imageWhere").textContent.includes("酒馆（Saloon）")')
 assert page.evaluate('document.querySelector("#viewerNext").textContent')=='下一张 ›'
 snap('chinese-viewer');report['checks'].append('Chinese captions, action, location and controls render on Android 16 despite old English preference')
 page.tap('#viewerNext');page.wait('document.querySelector("#fullPlace").textContent.startsWith("线圈")','Next image failed')
 page.tap('#viewerPrev');page.wait('document.querySelector("#fullPlace").textContent.startsWith("卫星碟")','Previous image failed')
 page.tap('#glossaryToggle');assert page.evaluate('document.querySelector("#glossaryToggle").textContent')=='英文名称：关'
 page.tap('#closeModal');page.wait('document.querySelectorAll(".thumb").length===25','Gallery return failed');page.tap('#closeModal')
 report['checks'].append('Native previous/next, parentheses toggle and return-to-gallery pass')
 report['crashLog']=adb('logcat','-b','crash','-d');assert PKG not in report['crashLog'];report['passed']=True
except Exception as e:
 report['passed']=False;report['error']=repr(e)
 try:snap('failure')
 except Exception:pass
 raise
finally:
 if page:page.close()
 (OUT/'chinese-android-test.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False))
