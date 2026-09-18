"""Test-only adjustments for the v0.14.3 review batch.
No application assets, translations, security policy, or APK code are modified.
"""
from pathlib import Path
import ast

NEW_IDS=[569291,677612,314600,562251,590076,678817,12655,678880,595383]

def replace_once(text,old,new,path):
    count=text.count(old)
    assert count==1,(path,old,count)
    return text.replace(old,new)

p=Path('updates/v014/complete/browser_test.py')
s=p.read_text()
s=replace_once(s,"assert page.evaluate('FaithfulArticleIndex.report.articlesTranslated')==52",
                 "assert page.evaluate('FaithfulArticleIndex.report.articlesTranslated')==61",p)
s=replace_once(s,"checks.append('52 source-by-source reviewed sources: all new units, full tables, recommended items, narrative, optional quests and media captions retained')",
                 "checks.append('61 source-by-source reviewed sources: source units, tables, gameplay conditions, narrative and media captions remain source-bound')",p)
marker="  assert not errors,errors;assert not missing,missing"
extra="""  for pid in [569291,677612,314600,562251,590076,678817,12655,678880,595383]:
   page.evaluate('pid=>FaithfulDebug.openDoc(pid)',pid)
   assert page.evaluate('FaithfulDebug.getDoc().reviewed')
   assert page.evaluate('FaithfulDebug.getDoc().translationStatus')=='reviewed'
   assert all(page.evaluate('FaithfulDebug.getDoc().units.map(u=>u.zh.trim().length>0)'))
  checks.append('Nine additional fixed-revision sources are fully reviewed and render every source-bound Chinese unit')
"""
assert s.count(marker)==1
s=s.replace(marker,extra+marker)
ast.parse(s);p.write_text(s)

p=Path('updates/v014/complete/feature_test.py')
s=p.read_text()
s=replace_once(s,'page.click(\'[data-filter="translated"]\');assert page.locator(\'.articleRow\').count()==52',
                 'page.click(\'[data-filter="translated"]\');assert page.locator(\'.articleRow\').count()==61',p)
s=replace_once(s,'page.click(\'[data-filter="pending"]\');assert page.locator(\'.articleRow\').count()==130',
                 'page.click(\'[data-filter="pending"]\');assert page.locator(\'.articleRow\').count()==121',p)
s=replace_once(s,"report['checks'].append('All 182 articles accessible; 52 reviewed / 130 full automatic drafts separated honestly')",
                 "report['checks'].append('All 182 articles accessible; 61 reviewed / 121 full automatic drafts separated honestly')",p)
old="for pid in [644198,644199,642369,642364,679946,679947,679948,679949,680030,682790,516886,634530]:"
new="for pid in [644198,644199,642369,642364,679946,679947,679948,679949,680030,682790,516886,634530,569291,677612,314600,562251,590076,678817,12655,678880,595383]:"
s=replace_once(s,old,new,p)
s=replace_once(s,"report['checks'].append('Twelve new complete reviewed source articles retain all original units and bilingual display')",
                 "report['checks'].append('Twenty-one post-preview reviewed source articles retain all original units and bilingual display')",p)
ast.parse(s);p.write_text(s)

p=Path('updates/v014/complete/native_test.py')
s=p.read_text()
s=replace_once(s,"assert page.evaluate('FaithfulArticleIndex.report.articlesTranslated')==52",
                 "assert page.evaluate('FaithfulArticleIndex.report.articlesTranslated')==61",p)
s=replace_once(s,"report['checks'].append('All complete KT-4/Classified source units render offline; native TOC-to-next navigation and 52-reviewed / 182-full-Chinese source inventory verified')",
                 "report['checks'].append('All complete KT-4/Classified source units render offline; native TOC-to-next navigation and 61-reviewed / 182-full-Chinese source inventory verified')",p)
ast.parse(s);p.write_text(s)
print('v0.14.3 tests now expect 61 reviewed / 121 automatic drafts and verify all nine new reviewed pages')
