"""Patch only restored QA scripts so review batches do not need hand-edited counts.
Usage: python updates/review_count_tests.py --reviewed 69 --drafts 113 --extra-ids 558453,558329,...
Application assets are never modified.
"""
from pathlib import Path
import argparse,ast,re

ap=argparse.ArgumentParser()
ap.add_argument('--reviewed',type=int,required=True)
ap.add_argument('--drafts',type=int,required=True)
ap.add_argument('--extra-ids',default='')
a=ap.parse_args()
assert a.reviewed+a.drafts==182
extra=[int(x) for x in a.extra_ids.split(',') if x.strip()]

def one(s,pattern,repl,path):
    matches=list(re.finditer(pattern,s))
    assert len(matches)==1,(str(path),pattern,len(matches))
    return re.sub(pattern,lambda _m:repl,s,count=1)

p=Path('updates/v014/complete/browser_test.py');s=p.read_text()
s=one(s,r"""assert page\.evaluate\('FaithfulArticleIndex\.report\.articlesTranslated'\)==\d+""",
      f"assert page.evaluate('FaithfulArticleIndex.report.articlesTranslated')=={a.reviewed}",p)
s=one(s,r"""checks\.append\('\d+ source-by-source reviewed sources:[^']*'\)""",
      f"checks.append('{a.reviewed} source-by-source reviewed sources: source units, tables, gameplay conditions, narrative and media captions remain source-bound')",p)
if extra:
    marker="  assert not errors,errors;assert not missing,missing"
    block=("  for pid in "+repr(extra)+":\n"
           "   page.evaluate('pid=>FaithfulDebug.openDoc(pid)',pid)\n"
           "   assert page.evaluate('FaithfulDebug.getDoc().reviewed')\n"
           "   assert all(page.evaluate('FaithfulDebug.getDoc().units.map(u=>u.zh.trim().length>0)'))\n"
           "  checks.append('Current semantic-review batch renders every source-bound Chinese unit')\n")
    assert s.count(marker)==1
    s=s.replace(marker,block+marker)
ast.parse(s);p.write_text(s)

p=Path('updates/v014/complete/feature_test.py');s=p.read_text()
# Kino der Toten (197844) became source-reviewed in v0.14.8. The restored legacy
# feature test still hard-codes it as a pending example, so update that assertion
# to match the delivered source state. Keep this as a QA-only patch.
s=re.sub(
    r"""page\.evaluate\('FaithfulDebug\.openDoc\(197844\)'\);assert '待' in page\.locator\('#docStatus'\)\.inner_text\(\) or '未完成' in page\.locator\('#docStatus'\)\.inner_text\(\)""",
    "page.evaluate('FaithfulDebug.openDoc(197844)');assert page.evaluate('FaithfulDebug.getDoc().reviewed');assert '逐段核对译文' in page.locator('#docStatus').inner_text()",
    s,
    count=1,
)
s=one(s,r"""page\.click\('\[data-filter="translated"\]'\);assert page\.locator\('\.articleRow'\)\.count\(\)==\d+""",
      f'''page.click('[data-filter="translated"]');assert page.locator('.articleRow').count()=={a.reviewed}''',p)
s=one(s,r"""page\.click\('\[data-filter="pending"\]'\);assert page\.locator\('\.articleRow'\)\.count\(\)==\d+""",
      f'''page.click('[data-filter="pending"]');assert page.locator('.articleRow').count()=={a.drafts}''',p)
if a.drafts==0:
    old="  assert '待复核' in page.locator('.articleRow small').first.inner_text()"
    assert s.count(old)==1,(str(p),'zero-draft legacy assertion',s.count(old))
    s=s.replace(old,"  assert page.locator('.articleRow').count()==0")
s=one(s,r"""report\['checks'\]\.append\('All 182 articles accessible; \d+ reviewed / \d+ full automatic drafts separated honestly'\)""",
      f"report['checks'].append('All 182 articles accessible; {a.reviewed} reviewed / {a.drafts} full automatic drafts separated honestly')",p)
if extra:
    marker="  # Actual cached bytes are loaded while every HTTPS request is blocked."
    block=("  for pid in "+repr(extra)+":\n"
           "   page.evaluate('pid=>FaithfulDebug.openDoc(pid)',pid)\n"
           "   assert page.evaluate('FaithfulDebug.getDoc().reviewed')\n"
           "   assert '逐段核对译文' in page.locator('#docStatus').inner_text()\n"
           "  report['checks'].append('Current semantic-review batch is explicitly marked reviewed in the delivered UI')\n")
    assert s.count(marker)==1
    s=s.replace(marker,block+marker)
ast.parse(s);p.write_text(s)

p=Path('updates/v014/complete/native_test.py');s=p.read_text()
s=one(s,r"""assert page\.evaluate\('FaithfulArticleIndex\.report\.articlesTranslated'\)==\d+""",
      f"assert page.evaluate('FaithfulArticleIndex.report.articlesTranslated')=={a.reviewed}",p)
s=one(s,r"""report\['checks'\]\.append\('All complete KT-4/Classified source units render offline; native TOC-to-next navigation and \d+-reviewed / 182-full-Chinese source inventory verified'\)""",
      f"report['checks'].append('All complete KT-4/Classified source units render offline; native TOC-to-next navigation and {a.reviewed}-reviewed / 182-full-Chinese source inventory verified')",p)
ast.parse(s);p.write_text(s)
print('QA expectations patched:',a.reviewed,'reviewed /',a.drafts,'drafts; extra ids',extra)
