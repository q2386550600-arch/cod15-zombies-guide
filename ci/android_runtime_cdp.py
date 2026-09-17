"""Test the unchanged, compiled APK using native taps plus live WebView inspection.

The API 36 image exposes WebView as one accessibility node. CDP is used only
for locating controls and reading state; navigation is exercised by adb taps.
"""
import hashlib
import json
import re
import subprocess
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path
import websocket

OUT=Path('android-test-results');OUT.mkdir(exist_ok=True)
PKG='com.openai.cod15guide'
APK=Path('output/COD_Zombies_Guide_v0.9.apk')

def adb(*args):
    return subprocess.check_output(['adb',*args],text=True,stderr=subprocess.STDOUT,timeout=90).strip()

def snap(name):
    (OUT/(name+'.png')).write_bytes(subprocess.check_output(['adb','exec-out','screencap','-p'],timeout=30))

class DevicePage:
    def __init__(self):
        self.counter=0
        self.ws=None
        deadline=time.monotonic()+40
        last=''
        while time.monotonic()<deadline:
            try:
                pid=adb('shell','pidof',PKG).split()[0]
                adb('forward','tcp:9222','localabstract:webview_devtools_remote_'+pid)
                with urllib.request.urlopen('http://127.0.0.1:9222/json',timeout=4) as response:
                    pages=json.load(response)
                target=next(p for p in pages if 'android_asset/index.html' in p.get('url',''))
                self.ws=websocket.create_connection(target['webSocketDebuggerUrl'],timeout=20,suppress_origin=True)
                self.target=target
                break
            except Exception as exc:
                last=str(exc);time.sleep(.5)
        if self.ws is None:raise AssertionError('Live WebView inspection unavailable: '+last)
        adb('shell','uiautomator','dump','/sdcard/guide-ui.xml')
        xml=adb('shell','cat','/sdcard/guide-ui.xml')
        (OUT/'native-hierarchy.xml').write_text(xml)
        node=next(n for n in ET.fromstring(xml).iter('node') if n.get('class')=='android.webkit.WebView')
        self.bounds=list(map(int,re.findall(r'\d+',node.get('bounds',''))))

    def call(self,method,params):
        self.counter+=1;ident=self.counter
        self.ws.send(json.dumps({'id':ident,'method':method,'params':params}))
        while True:
            reply=json.loads(self.ws.recv())
            if reply.get('id')!=ident:continue
            if 'error' in reply:raise RuntimeError(reply['error'])
            return reply.get('result',{})

    def evaluate(self,expression):
        result=self.call('Runtime.evaluate',{'expression':expression,'returnByValue':True,'awaitPromise':True})
        if 'exceptionDetails' in result:raise AssertionError(result['exceptionDetails'])
        return result.get('result',{}).get('value')

    def wait(self,expression,message,seconds=20):
        deadline=time.monotonic()+seconds
        while time.monotonic()<deadline:
            if self.evaluate(expression):return
            time.sleep(.15)
        raise AssertionError(message)

    def tap(self,selector):
        select=json.dumps(selector)
        self.evaluate('document.querySelector('+select+').scrollIntoView({block:"center",inline:"nearest"})')
        time.sleep(.15)
        r=self.evaluate('(()=>{const e=document.querySelector('+select+'),r=e.getBoundingClientRect();return {x:r.x+r.width/2,y:r.y+r.height/2,w:innerWidth,h:innerHeight};})()')
        x0,y0,x1,y1=self.bounds
        x=round(x0+r['x']*(x1-x0)/r['w']);y=round(y0+r['y']*(y1-y0)/r['h'])
        if not(x0<=x<x1 and y0<=y<y1):raise AssertionError('Control outside screen: '+selector)
        adb('shell','input','tap',str(x),str(y));time.sleep(.4)

    def state(self,name):
        result=self.evaluate('(()=>{const im=document.querySelector("#stepPhoto");return {map:document.querySelector("#runMap").textContent,title:document.querySelector("#stepTitle").textContent,overviewVisible:!document.querySelector("#overview").hidden,tutorialVisible:!document.querySelector("#tutorial").hidden,scrollTop:document.querySelector("#tutorialBody").scrollTop,imageWidth:im.naturalWidth,imageHeight:im.naturalHeight,progress:window.GuideDebug.getState(),imageCount:COMMUNITY_MEDIA.uniqueImages};})()')
        (OUT/(name+'.json')).write_text(json.dumps(result,ensure_ascii=False,indent=2))
        return result

    def close(self):
        if self.ws:self.ws.close()

report={'package':PKG,'apkSha256':hashlib.sha256(APK.read_bytes()).hexdigest(),'checks':[]}
page=None
try:
    report['sdk']=adb('shell','getprop','ro.build.version.sdk');assert report['sdk']=='36'
    report['install']=adb('install','-r',str(APK));assert 'Success' in report['install']
    adb('logcat','-c');report['launch']=adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
    page=DevicePage();page.wait('!!window.GuideDebug','Guide JavaScript did not initialize')
    assert page.evaluate('!document.querySelector("#overview").hidden')
    snap('01-overview');page.state('01-overview')
    report['checks'].append('Installs on API 36; native Activity and asset-backed overview render')
    page.tap('#start');page.wait('!document.querySelector("#tutorial").hidden && document.querySelector("#overview").hidden','Start did not enter focused tutorial')
    snap('02-first-step');page.state('02-first-step')
    report['checks'].append('Native start tap hides overview and opens focused tutorial')
    page.tap('#next');page.wait('document.querySelector("#stepTitle").textContent==="修4台泄漏通风机"','Next step did not advance')
    page.wait('document.querySelector("#stepPhoto").complete && document.querySelector("#stepPhoto").naturalWidth>0','Packaged original image did not load in Android WebView')
    assert page.evaluate('document.querySelector("#tutorialBody").scrollTop')==0
    snap('03-next-step');page.state('03-next-step')
    report['checks'].append('Native next tap advances, scroll resets, packaged source image decodes')
    page.tap('#zoomPhoto');page.wait('!document.querySelector("#modal").hidden && document.querySelector("#fullImage").naturalWidth>0','Image viewer failed')
    page.tap('#zoomIn');assert page.evaluate('document.querySelector("#fullImage").style.width')=='150%'
    snap('04-image-zoom');page.tap('#closeModal');page.wait('document.querySelector("#modal").hidden','Close control failed')
    report['checks'].append('Native image zoom and modal-close taps work')
    page.close();page=None
    adb('shell','am','force-stop',PKG);adb('shell','am','start','-W','-n',PKG+'/.MainActivity')
    page=DevicePage();page.wait('!!window.GuideDebug','Relaunch did not initialize');page.tap('#start')
    page.wait('document.querySelector("#stepTitle").textContent==="修4台泄漏通风机"','Saved step was lost after force-stop')
    snap('05-resumed');page.state('05-resumed')
    report['checks'].append('Current step survives force-stop and a fresh native Activity launch')
    report['crashLog']=adb('logcat','-b','crash','-d');assert PKG not in report['crashLog']
    report['passed']=True
except Exception as exc:
    report['passed']=False;report['error']=repr(exc)
    try:
        snap('failure');report['crashLog']=adb('logcat','-b','crash','-d')
        if page:page.state('failure-state')
    except Exception:pass
    raise
finally:
    if page:page.close()
    (OUT/'android-smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
    print(json.dumps(report,ensure_ascii=False,indent=2))
