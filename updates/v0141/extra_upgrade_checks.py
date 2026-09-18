from pathlib import Path
p=Path('updates/v0141/native_complete.py');s=p.read_text()
a="previous=page.evaluate('GuideDebug.getState()');page.close();page=None"
b="""previous=page.evaluate('GuideDebug.getState()')
 page.evaluate('GuideDebug.goMap("bo2_origins")');previous=page.evaluate('GuideDebug.getState()');page.tap('#startFaithful');page.wait('!!window.FaithfulDebug && FaithfulDebug.getDoc()?.metadata.pageid===567822','Old full-source reader did not load')
 page.tap('#next');page.tap('#next');old_source_position=page.evaluate('FaithfulDebug.getState().pos');old_source_storage=page.evaluate('localStorage.getItem("cod-faithful-reader-014")');assert old_source_storage
 page.close();page=None"""
assert s.count(a)==1;s=s.replace(a,b)
a="after=page.evaluate('GuideDebug.getState()');assert after['notes']==previous['notes'];assert after['detailPositions']==previous['detailPositions'];"
b=a+"assert page.evaluate('localStorage.getItem(\"cod-faithful-reader-014\")')==old_source_storage;report['checks'].append('Previous full-source reader storage remains byte-for-byte identical across the signed in-place update');"
assert s.count(a)==1;s=s.replace(a,b)
a="before=page.evaluate('FaithfulDebug.getState().pos');page.tap('#next');"
b="before=page.evaluate('FaithfulDebug.getState().pos');assert before==old_source_position;page.tap('#next');"
assert s.count(a)==1;s=s.replace(a,b);p.write_text(s)
p=Path('updates/v0141/test_complete.py');s=p.read_text();a="checks.append('Whole-source Chinese coverage and review status are independently reported: 182 present, 53 reviewed, 129 drafts')"
# Corpus structure checks already compare every translated unit with its stored source-bound value.
# Assert the actual parsed data directly so generic machine senses cannot return unnoticed.
marker="  assert not errors,errors"
extra="""  page.evaluate('FaithfulDebug.openDoc(330385)');page.wait_for_function('window.FaithfulDebug?.getDoc()?.metadata.pageid===330385')
  assert page.evaluate('FaithfulDebug.getDoc().units.find(u=>u.en==="Moon").zh')=='月球'
  assert page.evaluate('FaithfulDebug.getDoc().units.find(u=>u.en==="BO").zh')=='黑色行动1（BO）'
  checks.append('Moon and BO labels are source-bound map/version labels, not generic machine senses')
"""
assert s.count(marker)==1;s=s.replace(marker,extra+marker);p.write_text(s)
print('Added previous-reader update preservation and exact map/version terminology checks')
