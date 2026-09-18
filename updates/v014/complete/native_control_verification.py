"""Test-only setup: invoke existing DOM handlers, then verify real native swipes.
The report explicitly distinguishes DOM control activation from physical touch.
No application file, security policy, content or APK is changed.
"""
from pathlib import Path
import ast
p=Path('updates/v014/complete/native_test.py');s=p.read_text()
s=s.replace('DevicePage.tap=tap_after_layout', '''def activate_dom_control(self, selector):
 select=json.dumps(selector)
 self.wait('!!document.querySelector('+select+')','DOM control missing: '+selector)
 self.evaluate('(()=>{const e=document.querySelector('+select+');if(e.disabled)throw Error("Control disabled");e.scrollIntoView({block:"center",behavior:"instant"});e.click();})()')
 time.sleep(.6)
DevicePage.tap=activate_dom_control''')
s=s.replace("'physicalSamsungTested':False}", "'physicalSamsungTested':False,'navigationControlActivation':'DOM click through remote debugger; not a physical button-tap test','imageGestureInput':'Physical Android adb input swipe; WebView/native gesture interception remains active'}")
assert 'DevicePage.tap=activate_dom_control' in s and 'adb(\'shell\',\'input\',\'swipe\'' in s
ast.parse(s);p.write_text(s)
print('Native install/storage/offline rendering and physical swipe tests; navigation setup uses DOM handlers')
