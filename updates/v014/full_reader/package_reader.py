"""Package source-aligned documents without replacing any text with summaries."""
from pathlib import Path
import argparse,json,hashlib,collections,html
P=argparse.ArgumentParser();P.add_argument('--parsed',type=Path,required=True);P.add_argument('--reviewed',type=Path,required=True);P.add_argument('--out',type=Path,required=True);a=P.parse_args();a.out.mkdir(parents=True,exist_ok=True)
reviews={}
for f in sorted(a.reviewed.glob('*.json')):
 r=json.loads(f.read_text());assert r['pageid'] not in reviews;reviews[r['pageid']]=r
manifest=json.loads((a.parsed/'manifest.json').read_text());index=[];checks=[];expected=set(reviews)
for path in sorted(a.parsed.glob('*.json')):
 if not path.stem.isdigit():continue
 d=json.loads(path.read_text());m=d['metadata'];pid=m['pageid'];r=reviews.get(pid);units=d['units'];ids=[u['id'] for u in units];assert len(ids)==len(set(ids))
 digest=hashlib.sha256('\n'.join(u['id']+'\0'+u['en'] for u in units).encode()).hexdigest()
 if r:
  assert m['revision']==r['revision'],(pid,'revision mismatch')
  assert digest==r['sourceUnitDigest'],(pid,'source digest mismatch')
  translated=r['translationsInUnitOrder'];assert len(translated)==len(units),(pid,'unit count',len(translated),len(units))
  assert all(isinstance(z,str) and z.strip() for z in translated),(pid,'empty translation')
  for u,z in zip(units,translated):u['zh']=z
  expected.remove(pid)
 d.pop('bodyText',None);d['titleZh']=r.get('titleZh',m['title']) if r else m['title'];d['translated']=bool(r);d['sourceUnitDigest']=digest
 d['attribution']={'authors':'Call of Duty Wiki contributors','sourceUrl':m['fixedUrl'],'historyUrl':m['historyUrl'],'license':'CC BY-SA 3.0','licenseUrl':'https://creativecommons.org/licenses/by-sa/3.0/','changes':'Added Simplified Chinese translation and reading interface. Original source units and tree retained.','mediaNotice':'Images and videos retain original file-page and source links; their rights are separate from article-text licensing. No new media files are redistributed by this package.'}
 d['translatorNotes']=r.get('translatorNotes',[]) if r else []
 d['reviewMethod']=r.get('reviewMethod','') if r else 'Not translated'
 (a.out/f'p{pid}.js').write_text('window.FaithfulArticles.accept('+json.dumps(d,ensure_ascii=False,separators=(',',':'))+');\n')
 entry={'pageid':pid,'revision':m['revision'],'title':m['title'],'titleZh':d['titleZh'],'translated':bool(r),'units':len(units),'images':len(d['images']),'file':f'p{pid}.js','url':m['fixedUrl']};index.append(entry)
 if r:
  (a.out/f'reviewed-{pid}.json').write_text(json.dumps(r,ensure_ascii=False,indent=2))
  checks.append({'pageid':pid,'title':m['title'],'revision':m['revision'],'textUnits':len(units),'translations':len(r['translationsInUnitOrder']),'imageSlots':len(d['images']),'externalLinks':len(m['externalLinks']),'sourceUnitDigest':digest})
assert not expected,('Missing source pages',expected)
index.sort(key=lambda x:(not x['translated'],x['title'].lower()))
report={'pagesArchived':len(index),'articlesTranslated':len(checks),'translatedUnits':sum(x['textUnits'] for x in checks),'translatedArticleImageSlots':sum(x['imageSlots'] for x in checks),'totalUnits':sum(x['units'] for x in index),'allSourcesTranslated':len(index)==len(checks),'checks':checks,'missingSourceRequests':manifest.get('failures',[]),'scope':'Only articles with complete matching source-unit translations are labelled translated. Remaining archived articles are original English, not approved Chinese translations. UI tests do not prove in-game correctness.'}
(a.out/'index.js').write_text('window.FaithfulArticleIndex='+json.dumps({'pages':index,'aliases':manifest.get('sourceAliases',{}),'report':report},ensure_ascii=False,separators=(',',':'))+';\n')
(a.out/'completeness.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
(a.out/'LICENSE-TEXT.txt').write_text('Article text: Call of Duty Wiki contributors, CC BY-SA 3.0.\nhttps://creativecommons.org/licenses/by-sa/3.0/\nEach document retains its fixed source revision URL and edit-history URL for attribution. Chinese translations are shared under CC BY-SA 3.0. Images and videos may have different rights: retained as original remote references and file-page links, not relicensed.\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
