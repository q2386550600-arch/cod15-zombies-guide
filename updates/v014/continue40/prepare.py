"""Deterministically restore full articles, never accept an incomplete checkpoint."""
from pathlib import Path
import base64,hashlib,json,lzma,struct,zlib,runpy
R=Path('updates/v014');F=R/'full_reader';V=R/'reviewed'
for stem,count,digest,expected in [('reader23',4,'e16b3096dd16b2e3d721a6a9fa4214cb5f007582c4c600022fdbac94efa609a8',17),('reviews30',3,'730a5edb4897f29cc9bb2080f12be3d9700781b8e60be04cafc077904502bdfd',7)]:
 encoded=''.join((R/'delivery'/f'{stem}.xz.b64.part{i}').read_text().strip() for i in range(1,count+1))
 raw=lzma.decompress(base64.b64decode(encoded,validate=True));assert hashlib.sha256(raw).hexdigest()==digest
 items=json.loads(raw);assert len(items)==expected
 for name,text in items.items():
  p=Path(name);assert not p.is_absolute() and '..' not in p.parts
  assert name.startswith(('updates/v014/reviewed/','updates/v014/full_reader/'))
  p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
# The old 36-article ZIP upload stopped mid-entry. Five preceding stored members
# are individually complete and CRC-verifiable. Never accept the unfinished sixth.
encoded=''.join((R/'continue36'/f'bundle.part{i}').read_text().strip() for i in range(3))
raw=lzma.LZMADecompressor().decompress(base64.b64decode(encoded));at=0;recovered=[]
while at+30<=len(raw) and raw[at:at+4]==b'PK\x03\x04':
 h=struct.unpack_from('<IHHHHHIIIHH',raw,at);_,ver,flags,method,tm,dt,crc,size,usize,nlen,xlen=h
 assert not flags&8 and method==0
 name=raw[at+30:at+30+nlen].decode();start=at+30+nlen+xlen;end=start+size
 if end>len(raw):break
 data=raw[start:end];assert len(data)==usize and zlib.crc32(data)&0xffffffff==crc,(name,'CRC')
 if name.startswith('articles/') and name.endswith('.json'):
  obj=json.loads(data);pid=obj['pageid'];assert pid in [635805,640007,646760,646803,651100]
  (V/f'reviewed-{pid}.json').write_bytes(data);recovered.append(pid)
 at=end
assert sorted(recovered)==[635805,640007,646760,646803,651100],recovered
# The separately committed sixth translation is complete, not the ZIP's tail.
reviews=[json.loads(p.read_text()) for p in V.glob('*.json')]
assert len(reviews)==40 and len({r['pageid'] for r in reviews})==40
assert sum(len(r['translationsInUnitOrder']) for r in reviews)==4027
runpy.run_path(str(R/'continue30/patch_reader.py'))
f=F/'faithful.js';s=f.read_text();needle='function renderDoc(anchor){'
helper="""function sourceSectionForAnchor(anchor){
 const contains=n=>n.id===anchor||n.anchor===anchor||n.attrs?.id===anchor||n.altUnit===anchor||(n.children||[]).some(contains)||(n.images||[]).some(contains);
 return sections.findIndex(nodes=>nodes.some(contains));
}
"""
assert needle in s;s=s.replace(needle,helper+needle+'if(anchor){const selected=sourceSectionForAnchor(anchor);if(selected>=0)pos=selected;}',1)
s=s.replace("anchor:decodeURIComponent(u.hash.slice(1))","anchor:decodeURIComponent(u.hash.slice(1))||(typeof alias==='object'?alias.anchor||'':'')")
f.write_text(s)
f=F/'package_reader.py';s=f.read_text();needle="manifest=json.loads((a.parsed/'manifest.json').read_text());index=[];checks=[];expected=set(reviews)"
assert needle in s
s=s.replace(needle,needle+"\nfor name in ['Masamune','KT-4/Masamune']:manifest.setdefault('sourceAliases',{})[name]={'pageid':646760,'title':'KT-4','anchor':'Masamune','resolution':'The standalone title is absent; the complete source section is KT-4#Masamune.'}\n")
f.write_text(s)
f=F/'entry-faithful.js';s=f.read_text().replace('classified:677503','classified:676001').replace('const roots={','const roots={bo1_five:197863,');f.write_text(s)
f=F/'apply_reader.py';s=f.read_text().replace('versionCode 16','versionCode 17').replace("versionName '0.14.0-preview2'","versionName '0.14.0-preview3'");f.write_text(s)
f=F/'test_faithful.py';s=f.read_text()
old="  page.evaluate('pid=>FaithfulDebug.openDoc(pid)',568554);page.click('#mode');page.click('#next');page.screenshot(path=str(OUT/'faithful-lore.png'))"
new="""  page.evaluate('pid=>FaithfulDebug.openDoc(pid)',568554)
  page.click('#toc');page.locator('#chapters button').first.click()
  assert page.evaluate('FaithfulDebug.getState().mode')=='full'
  selected=page.evaluate('FaithfulDebug.getState().pos');page.click('#mode')
  assert not page.locator('#next').is_disabled();page.click('#next')
  assert page.evaluate('FaithfulDebug.getState().pos')==selected+1
  page.screenshot(path=str(OUT/'faithful-lore.png'))
  checks.append('Table-of-contents selection synchronizes section position after resuming the last section')"""
assert old in s;s=s.replace(old,new)
needle='  assert not errors,errors;assert not missing,missing'
extra="""  for pid,count in [(635805,119),(640007,126),(646760,111),(646803,53),(651100,184),(654437,182),(676001,379),(198083,144),(678222,62),(561149,34)]:
   page.evaluate('pid=>FaithfulDebug.openDoc(pid)',pid)
   if page.evaluate('FaithfulDebug.getState().mode')!='full':page.click('#mode')
   assert page.evaluate('FaithfulDebug.getDoc().translated') is True
   assert page.locator('#body [data-unit]').count()==count,(pid,'missing text')
   if pid==676001:
    assert '音乐彩蛋' in page.locator('#body').inner_text() and '7.99' in page.locator('#body').inner_text()
    page.click('#toc');page.locator('#chapters button').filter(has_text='防暴盾零件位置').first.click()
    page.screenshot(path=str(OUT/'classified-location-table.png'))
   if pid==646760:
    assert '02182016' in page.locator('#body').inner_text() and '克隆植物' in page.locator('#body').inner_text()
    page.click('#toc');page.locator('#chapters button').filter(has_text='正宗').first.click()
    page.screenshot(path=str(OUT/'kt4-complete-recipe.png'))
  assert page.evaluate('FaithfulArticleIndex.report.articlesTranslated')==40
  checks.append('40 complete sources: all new units, full tables, recommended items, narrative, optional quests and media captions retained')
"""
assert needle in s;s=s.replace(needle,extra+needle);f.write_text(s)
f=F/'native_reader_test.py';s=f.read_text().replace('v0.14.0-preview2','v0.14.0-preview3')
needle=" report['crashLog']=adb('logcat','-b','crash','-d');"
extra=""" page.evaluate('FaithfulDebug.openDoc(646760)');page.wait('FaithfulDebug.getDoc()?.metadata.pageid===646760','KT-4 missing')
 if page.evaluate('FaithfulDebug.getState().mode')!='full':page.tap('#mode')
 assert page.evaluate('document.querySelectorAll("#body [data-unit]").length')==111
 page.tap('#toc');page.evaluate('(()=>{const b=[...document.querySelectorAll("#chapters button")].find(e=>e.textContent.includes("正宗"));b.id="nativeMasamune";})()');page.tap('#nativeMasamune')
 selected=page.evaluate('FaithfulDebug.getState().pos');page.tap('#mode');page.tap('#next');assert page.evaluate('FaithfulDebug.getState().pos')==selected+1
 snap('04-complete-kt4-recipe')
 page.evaluate('FaithfulDebug.openDoc(676001)');page.wait('FaithfulDebug.getDoc()?.metadata.pageid===676001','Classified full source missing')
 if page.evaluate('FaithfulDebug.getState().mode')!='full':page.tap('#mode')
 assert page.evaluate('document.querySelectorAll("#body [data-unit]").length')==379
 page.tap('#toc');page.evaluate('(()=>{const b=[...document.querySelectorAll("#chapters button")].find(e=>e.textContent.includes("防暴盾零件位置"));b.id="nativeShield";})()');page.tap('#nativeShield')
 snap('05-classified-full-location-table')
 assert page.evaluate('FaithfulArticleIndex.report.articlesTranslated')==40
 report['checks'].append('All complete KT-4/Classified source units render offline; native TOC-to-next navigation and 40-source inventory verified')
"""
assert needle in s;s=s.replace(needle,extra+needle);f.write_text(s)
print('40 complete fixed-revision translations recovered: 4027 original text units. Other sources remain explicitly untranslated.')
