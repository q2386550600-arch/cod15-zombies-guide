"""Repair test automation only. No APK, web assets, security policy or assertions changed."""
from pathlib import Path
import ast
root=Path('updates/v014/complete')
f=root/'feature_test.py'
s=f.read_text()
s=s.replace('import json,os,threading,hashlib','import json,os,threading,hashlib,time')
s=s.replace('class Quiet(SimpleHTTPRequestHandler):', '''def wait_dom(page, expression, timeout=30):
 # Poll via the same debugger evaluate used by the other assertions. This
 # does not ask the application to eval a string or weaken its strict CSP.
 deadline=time.monotonic()+timeout
 last=None
 while time.monotonic()<deadline:
  try:
   if page.evaluate(expression):return
  except Exception as exc:
   last=exc
  time.sleep(.08)
 raise AssertionError('DOM condition timed out: '+expression+'; '+str(last))
class Quiet(SimpleHTTPRequestHandler):''')
s=s.replace('page.wait_for_function(', 'wait_dom(page, ')
s=s.replace('finally:\n (OUT/', '''except Exception as exc:
 report['error']=repr(exc)
 try:page.screenshot(path=str(OUT/'offline-feature-failure.png'))
 except Exception:pass
 raise
finally:
 (OUT/''')
assert 'page.wait_for_function' not in s
ast.parse(s);f.write_text(s)
f=root/'native_test.py';s=f.read_text()
s=s.replace("exec(base)\n",'''exec(base)

def tap_after_layout(self, selector):
 # A late source-entry card changes the old overview layout on first load.
 # Wait for the real target to be in the viewport and not covered, then
 # send an actual Android input tap. Do not trigger an element click in JS.
 select=json.dumps(selector)
 deadline=time.monotonic()+12
 last=None
 while time.monotonic()<deadline:
  self.evaluate('document.querySelector('+select+').scrollIntoView({block:"center",inline:"nearest",behavior:"instant"})')
  time.sleep(.25)
  r=self.evaluate('(()=>{const e=document.querySelector('+select+'),r=e.getBoundingClientRect(),x=r.x+r.width/2,y=r.y+r.height/2,t=document.elementFromPoint(x,y);return {x,y,w:innerWidth,h:innerHeight,hit:!!t&&(t===e||e.contains(t)),visible:r.width>0&&r.height>0};})()')
  last=r
  if r['visible'] and r['hit'] and 0<=r['x']<r['w'] and 0<=r['y']<r['h']:
   x0,y0,x1,y1=self.bounds
   x=round(x0+r['x']*(x1-x0)/r['w']);y=round(y0+r['y']*(y1-y0)/r['h'])
   adb('shell','input','tap',str(x),str(y));time.sleep(.4)
   return
 raise AssertionError('Real control not tappable after layout settled: '+selector+' '+str(last))
DevicePage.tap=tap_after_layout
''')
s=s.replace("page.wait('!!window.GuideDebug','Old guide failed')", "page.wait('!!window.GuideDebug && !!document.querySelector(\"#startFaithful\")','Old guide failed');time.sleep(.5)")
ast.parse(s);f.write_text(s)
print('Test-only fixes applied; application assets and APK remain untouched')
