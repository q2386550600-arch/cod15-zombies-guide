"""Install and exercise the shipped APK on a clean Android emulator."""
import json,re,subprocess,time,xml.etree.ElementTree as ET
from pathlib import Path
OUT=Path('android-test-results');OUT.mkdir(exist_ok=True)
PKG='com.openai.cod15guide'
def adb(*args):
 return subprocess.check_output(['adb',*args],text=True,stderr=subprocess.STDOUT,timeout=90).strip()
def snap(name):
 (OUT/(name+'.png')).write_bytes(subprocess.check_output(['adb','exec-out','screencap','-p'],timeout=30))
def dump(name):
 adb('shell','uiautomator','dump','/sdcard/guide-ui.xml')
 s=adb('shell','cat','/sdcard/guide-ui.xml');(OUT/(name+'.xml')).write_text(s)
 return s
def tap_text(pattern,name):
 for attempt in range(5):
  xml=dump(name+'-'+str(attempt))
  for n in ET.fromstring(xml).iter('node'):
   if re.search(pattern,n.get('text','')+' '+n.get('content-desc','')):
    xy=list(map(int,re.findall(r'\d+',n.get('bounds',''))))
    if len(xy)==4 and xy[2]>xy[0] and xy[3]>xy[1]:
     adb('shell','input','tap',str((xy[0]+xy[2])//2),str((xy[1]+xy[3])//2));time.sleep(1);return
  size=list(map(int,re.findall(r'\d+',adb('shell','wm','size'))))[-2:]
  w,h=size;adb('shell','input','swipe',str(w//2),str(int(h*.76)),str(w//2),str(int(h*.36)),'350');time.sleep(.5)
 raise AssertionError('Visible control not found: '+pattern)
report={'package':PKG,'checks':[]}
try:
 report['sdk']=adb('shell','getprop','ro.build.version.sdk')
 report['install']=adb('install','-r','output/COD_Zombies_Guide_v0.9.apk');assert 'Success' in report['install']
 adb('logcat','-c');report['launch']=adb('shell','am','start','-W','-n',PKG+'/.MainActivity');time.sleep(5)
 assert adb('shell','pidof',PKG);snap('01-overview');xml=dump('01-overview');assert 'COD' in xml and ('开始解密' in xml or '流程预览' in xml)
 report['checks'].append('APK installs and native Activity renders the overview')
 tap_text('开始解密','start');xml=dump('02-first-step');snap('02-first-step');assert '当前任务' in xml and '流程预览' not in xml
 report['checks'].append('Start hides overview and enters a real Android WebView tutorial')
 tap_text('完成并下一步','next');xml=dump('03-next-step');snap('03-next-step');assert '修4台泄漏通风机' in xml
 report['checks'].append('Pinned next button advances to the new step')
 adb('shell','am','force-stop',PKG);adb('shell','am','start','-W','-n',PKG+'/.MainActivity');time.sleep(3)
 tap_text('继续解密','resume');xml=dump('04-resumed');snap('04-resumed');assert '修4台泄漏通风机' in xml
 report['checks'].append('Progress survives force-stop and native app relaunch')
 report['crashLog']=adb('logcat','-b','crash','-d');assert PKG not in report['crashLog']
 report['passed']=True
except Exception as e:
 report['passed']=False;report['error']=str(e)
 try:snap('failure');report['crashLog']=adb('logcat','-b','crash','-d')
 except Exception:pass
 raise
finally:
 (OUT/'android-smoke.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
