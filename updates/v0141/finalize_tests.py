"""Preserve application CSP and all assertions; avoid eval-based Playwright polling."""
from pathlib import Path
p=Path('updates/v0141/test_complete.py');s=p.read_text()
helper='''
def wait_doc(page, pageid, timeout=15):
    deadline=time.monotonic()+timeout
    last=None
    while time.monotonic()<deadline:
        try:
            last=page.evaluate('window.FaithfulDebug?.getDoc()?.metadata.pageid')
            if last==pageid:
                page.wait_for_selector('#body [data-unit]')
                return
        except Exception as exc:
            # A navigation replaces the execution context. Retry the new context.
            last=str(exc)
        time.sleep(0.05)
    page.screenshot(path=str(OUT/'navigation-readiness-failure.png'))
    raise AssertionError(('Expected source did not finish loading',pageid,last,page.url))
'''
assert '\ndef wait_doc(' not in s
s=s.replace('checks=[];errors=[];missing=[];report={}',helper+'\nchecks=[];errors=[];missing=[];report={}')
count=0
for old in ["page.wait_for_function('FaithfulDebug.getDoc()?.metadata.pageid===330385')","page.wait_for_function('window.FaithfulDebug?.getDoc()?.metadata.pageid===330385')"]:
    count+=s.count(old);s=s.replace(old,'wait_doc(page,330385)')
assert count==2,('Expected both real navigation and final map-state waits',count)
compile(s,str(p),'exec');p.write_text(s)
print('Two source readiness checks now poll from the test process; application CSP and source assertions are unchanged')
