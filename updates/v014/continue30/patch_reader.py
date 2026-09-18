from pathlib import Path
F=Path('updates/v014/full_reader')
f=F/'test_faithful.py';s=f.read_text()
old="""  a=page.locator('#body a').filter(has_text=link['text']).first
  a.locator('xpath=ancestor::details').evaluate('e=>e.open=true');a.click()
  assert page.evaluate('FaithfulDebug.getDoc().metadata.pageid')==569107"""
new="""  # Assert the exact href and await async article-script loading.
  a=page.locator('#body a[href="https://callofduty.fandom.com/wiki/G-Strike"]').first
  assert a.count()==1
  a.locator('xpath=ancestor::details').evaluate('e=>e.open=true');a.click()
  deadline=time.monotonic()+10
  while time.monotonic()<deadline and page.evaluate('FaithfulDebug.getDoc()?.metadata.pageid')!=569107:
   time.sleep(.05)
  actual_page=page.evaluate('FaithfulDebug.getDoc()?.metadata.pageid')
  if actual_page!=569107:
   page.screenshot(path=str(OUT/'dependency-failure.png'))
   raise AssertionError(('Exact original dependency did not resolve',actual_page,page.url))"""
assert old in s;s=s.replace(old,new)
needle='  assert not errors,errors;assert not missing,missing'
extra="""  for pid,count in [(677509,37),(680694,29),(677511,37),(681329,54),(682250,73),(678809,82),(677699,112)]:
   page.evaluate('pid=>FaithfulDebug.openDoc(pid)',pid)
   if page.evaluate('FaithfulDebug.getState().mode')!='full':page.click('#mode')
   assert page.evaluate('FaithfulDebug.getDoc().translated') is True
   assert page.locator('#body [data-unit]').count()==count
   if pid==677699:
    text=page.locator('#body').inner_text()
    assert '建议一到两位玩家' in text and '灭队' in text and '结尾过场动画' in text
    page.click('#toc');page.locator('#chapters button').filter(has_text='第9步').first.click()
    page.screenshot(path=str(OUT/'voyage-unabridged-loadout.png'))
   if pid==682250:
    page.click('#toc');page.locator('#chapters button').filter(has_text='第5步').first.click()
    page.screenshot(path=str(OUT/'tag-ending-preserved.png'))
  checks.append('All seven new BO4 source articles have every original unit translated, including full boss/loadout paragraphs, dialogue, narrative endings and trivia')
"""
assert needle in s;s=s.replace(needle,extra+needle);f.write_text(s)
f=F/'apply_reader.py';s=f.read_text().replace('versionCode 15','versionCode 16').replace("versionName '0.14.0-preview1'","versionName '0.14.0-preview2'");f.write_text(s)
f=F/'native_reader_test.py';s=f.read_text().replace('v0.14.0-preview1','v0.14.0-preview2')
old=" page.tap('#back');page.tap('#back');page.wait('!!window.GuideDebug','Returning to legacy guide failed');assert page.evaluate('GuideDebug.getState().notes.alpha')=='faithful-upgrade-note'"
new=""" # Return through dependency history and library using actual native taps.
 for _ in range(4):
  if page.evaluate('!!window.GuideDebug'):break
  page.tap('#back');time.sleep(.4)
 page.wait('!!window.GuideDebug','Returning to legacy guide failed');assert page.evaluate('GuideDebug.getState().notes.alpha')=='faithful-upgrade-note'"""
assert old in s;s=s.replace(old,new)
needle=" report['crashLog']=adb('logcat','-b','crash','-d');"
extra=""" page.evaluate('GuideDebug.goMap("voyage")');page.tap('#startFaithful');page.wait('!!window.FaithfulDebug && FaithfulDebug.getDoc()?.metadata.pageid===677699','New full BO4 article did not open')
 assert page.evaluate('FaithfulDebug.getDoc().translated') is True
 if page.evaluate('FaithfulDebug.getState().mode')!='full':page.tap('#mode')
 assert page.evaluate('document.querySelectorAll("#body [data-unit]").length')==112
 page.tap('#toc');page.evaluate('(()=>{let b=[...document.querySelectorAll("#chapters button")].find(b=>b.textContent.includes("第9步"));b.id="nativeBossChapter";})()');page.tap('#nativeBossChapter');snap('03-voyage-complete-source-loadout')
 assert '人造小人' in page.evaluate('document.querySelector("#body").textContent')
 report['checks'].append('New Voyage main source renders all 112 units including loadouts and full boss prose with network radios disabled')
"""
assert needle in s;s=s.replace(needle,extra+needle);f.write_text(s)
f=F/'faithful.js';s=f.read_text();old='f.append(notice,links);return f;}'
new="const inspect=element('button','查看图注／左右翻图','imageRecordButton');inspect.onclick=()=>openPicture(n.id);f.append(notice,inspect,links);return f;}"
assert old in s;s=s.replace(old,new);f.write_text(s)
f=F/'faithful.css';f.write_text(f.read_text()+'\n.imageRecordButton{font-size:12px;margin-top:7px;min-height:40px}\n')
print('Source content is untouched by reader fixes; original figures remain inspectable even when remote pixels are unavailable.')
