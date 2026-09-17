from pathlib import Path
p=Path('ci/android_runtime_cdp.py');s=p.read_text();s=s.replace('v0.9.apk','v0.10.apk')
extra='''    # Exercise the user's exact Buried gallery complaint on the installed APK.
    page.evaluate('GuideDebug.goMap("bo2_buried")');page.tap('#galleryOverview')
    page.wait('document.querySelector(".thumb img").naturalWidth>0','Gallery thumbnail did not load')
    dims=page.evaluate('(()=>{const im=document.querySelector(".thumb img"),r=im.getBoundingClientRect();return {w:r.width,h:r.height,nw:im.naturalWidth,nh:im.naturalHeight};})()')
    assert abs(dims['h']/dims['w']-dims['nh']/dims['nw'])<.02,dims
    report['galleryThumbnail']=dims;snap('06-buried-gallery')
    page.tap('.thumb[data-image-index="4"]');page.wait('document.querySelector("#fullAction").textContent.includes("Guillotine")','Missing satellite-dish action note')
    snap('07-buried-satellite')
    page.tap('#viewerNext');page.wait('document.querySelector("#fullPlace").textContent.includes("Spool of Wire")','Next image failed')
    page.tap('#viewerPrev');page.wait('document.querySelector("#fullPlace").textContent.includes("Satellite Dish")','Previous image failed')
    # Native Android swipe, not a synthetic JavaScript event.
    r=page.evaluate('(()=>{let r=document.querySelector("#viewerPane").getBoundingClientRect();return {x:r.x,y:r.y,w:r.width,h:r.height,vw:innerWidth,vh:innerHeight};})()')
    x0,y0,x1,y1=page.bounds
    xa=round(x0+(r['x']+r['w']*.8)*(x1-x0)/r['vw']);xb=round(x0+(r['x']+r['w']*.2)*(x1-x0)/r['vw']);yy=round(y0+(r['y']+r['h']*.5)*(y1-y0)/r['vh'])
    adb('shell','input','swipe',str(xa),str(yy),str(xb),str(yy),'250')
    page.wait('document.querySelector("#viewerNumber").textContent==="6 / 25"','Native swipe failed')
    page.tap('#zoomIn');page.tap('#viewerNext');assert page.evaluate('document.querySelector("#fullImage").style.width')=='100%'
    page.tap('#closeModal');page.wait('document.querySelectorAll(".thumb").length===25','Return to gallery failed')
    page.tap('#closeModal');page.wait('document.querySelector("#modal").hidden','Gallery close failed')
    report['checks'].append('Buried natural-ratio thumbnails, English/Chinese action notes, native previous/next/swipe and gallery return pass')
    page.evaluate('GuideDebug.goMap("alpha")')
'''
marker="    report['checks'].append('Native image zoom and modal-close taps work')\n"
assert marker in s;s=s.replace(marker,marker+extra+'\n')
pre='''    old=Path('old/COD_Zombies_Guide_v0.9.apk')
    assert old.is_file()
    assert 'Success' in adb('install','-r',str(old))
    adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
    prior=DevicePage();prior.wait('!!window.GuideDebug','v0.9 did not initialise')
    prior.tap('#start');prior.tap('#next')
    prior.wait('GuideDebug.getState().step===1','v0.9 progress was not created')
    prior.tap('#openNotes')
    prior.evaluate('(()=>{const e=document.querySelector("#freeNotes");e.value="upgrade-keep-0245";e.dispatchEvent(new Event("input",{bubbles:true}));})()')
    prior.tap('#closeModal');prior.close();adb('shell','am','force-stop',PKG)
'''
needle="    report['install']=adb('install','-r',str(APK));assert 'Success' in report['install']"
assert needle in s;s=s.replace(needle,pre+needle)
check='''    assert page.evaluate('GuideDebug.getState().step')==1
    assert page.evaluate('GuideDebug.getState().notes.alpha')=='upgrade-keep-0245'
    report['checks'].append('v0.9 to v0.10 in-place update succeeds and preserves progress and notes')
    page.tap('#reset');page.tap('#confirmReset')
'''
needle="    assert page.evaluate('!document.querySelector(\"#overview\").hidden')"
assert needle in s;s=s.replace(needle,check+needle)
Path('ci/native_v010.py').write_text(s)
