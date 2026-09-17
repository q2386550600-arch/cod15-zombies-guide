"""Verify the unchanged v0.11 APK. Check the old note was actually entered
before comparing persistence across upgrade; collect UI results independently.
"""
from pathlib import Path
exec(Path('ci/android_runtime_cdp.py').read_text().split("report={'package'")[0])
APK=Path('output/COD_Zombies_Guide_v0.11.apk')
report={'apkSha256':hashlib.sha256(APK.read_bytes()).hexdigest(),'checks':[],'failures':[]};page=None

def check(name,condition,detail=None):
    result={'name':name,'passed':bool(condition)}
    if detail is not None:result['detail']=detail
    report['checks'].append(result)
    if not condition:report['failures'].append(name)

def save_state(label):
    state=page.evaluate('GuideDebug.getState()')
    (OUT/(label+'.json')).write_text(json.dumps(state,ensure_ascii=False,indent=2))
    return state

try:
    report['sdk']=adb('shell','getprop','ro.build.version.sdk');assert report['sdk']=='36'
    assert 'Success' in adb('install','-r','.base/COD_Zombies_Guide_v0.10.apk')
    adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
    page=DevicePage();page.wait('!!window.GuideDebug','Old version did not initialise')
    page.tap('#start');page.tap('#next');page.wait('GuideDebug.getState().step===1','Old step was not saved')
    page.tap('#openNotes');page.tap('#freeNotes')
    page.wait('document.activeElement.id==="freeNotes"','Note editor did not receive focus')
    # Use the WebView text editor itself; do not seed the app state or storage.
    page.call('Input.insertText',{'text':'keep011'})
    page.wait('document.querySelector("#freeNotes").value==="keep011"','Note text was not entered')
    page.wait('GuideDebug.getState().notes.alpha==="keep011"','Note input handler did not save the value')
    page.evaluate('document.querySelector("#freeNotes").blur()')
    page.evaluate('window.guideBack()')
    page.evaluate('localStorage.setItem("cod-guide-image-language",JSON.stringify("en"))')
    before=save_state('before-upgrade');snap('before-upgrade')
    check('Old note was entered and saved before upgrading',before['notes'].get('alpha')=='keep011')
    adb('shell','input','keyevent','3');time.sleep(3);page.close();page=None
    adb('shell','am','force-stop',PKG)
    report['install']=adb('install','-r',str(APK));assert 'Success' in report['install']
    adb('logcat','-c');adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
    page=DevicePage();page.wait('!!window.ZhDisplay&&!!window.GuideDebug','Chinese app did not initialise')
    after=save_state('after-upgrade')
    check('Upgrade preserves current step',after['step']==before['step'],{'before':before['step'],'after':after['step']})
    check('Upgrade preserves notes',after['notes'].get('alpha')==before['notes'].get('alpha'),{'before':before['notes'].get('alpha'),'after':after['notes'].get('alpha')})
    page.evaluate('GuideDebug.goMap("bo2_buried")');page.tap('#galleryOverview')
    page.wait('document.querySelector(".thumb img").naturalWidth>0','No gallery thumbnails')
    dims=page.evaluate('(()=>{const i=document.querySelector(".thumb img"),r=i.getBoundingClientRect();return {w:r.width,h:r.height,nw:i.naturalWidth,nh:i.naturalHeight};})()')
    check('Gallery keeps the original image ratio',abs(dims['h']/dims['w']-dims['nh']/dims['nw'])<.02,dims)
    snap('chinese-gallery')
    page.tap('.thumb[data-image-index="4"]');page.wait('document.querySelector("#fullImage").naturalWidth>0','No full image')
    display=page.evaluate('Object.fromEntries(["fullPlace","fullAction","imageWhere","viewerNext","glossaryToggle"].map(id=>[id,document.getElementById(id).textContent]))')
    check('Chinese is the primary image language',display['fullPlace'].startswith('卫星碟') and display['fullAction'].startswith('捡起'),display)
    check('English place name is supplementary parentheses','酒馆（Saloon）' in display['imageWhere'])
    check('Image controls are Chinese',display['viewerNext']=='下一张 ›')
    snap('chinese-viewer')
    page.tap('#viewerNext');page.wait('document.querySelector("#fullPlace").textContent.startsWith("线圈")','Next image failed')
    page.tap('#viewerPrev');page.wait('document.querySelector("#fullPlace").textContent.startsWith("卫星碟")','Previous image failed')
    check('Native previous and next buttons work',True)
    page.tap('#glossaryToggle');check('English-parentheses switch works',page.evaluate('document.querySelector("#glossaryToggle").textContent')=='英文名称：关')
    page.tap('#closeModal');page.wait('document.querySelectorAll(".thumb").length===25','Gallery return failed')
    page.tap('#closeModal');page.wait('document.querySelector("#modal").hidden','Gallery close failed')
    check('Native viewer and gallery close controls work',True)
    report['crashLog']=adb('logcat','-b','crash','-d');check('No app crash recorded',PKG not in report['crashLog'])
except Exception as e:
    report['failures'].append(repr(e))
    try:
        snap('failure')
        if page:save_state('failure-state')
    except Exception:pass
finally:
    if page:page.close()
    report['passed']=not report['failures']
    (OUT/'chinese-native-verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
if not report['passed']:raise AssertionError(report['failures'])
