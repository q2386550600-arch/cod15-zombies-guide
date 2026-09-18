"""Recover immutable source inputs, quarantine old drafts, publish a truthful ledger."""
from pathlib import Path
import json,argparse,hashlib
from recovery_state import make_plan,split_exact
p=argparse.ArgumentParser();p.add_argument('--parsed',default='parsed');p.add_argument('--legacy',default='legacy');p.add_argument('--out',default='recovery');a=p.parse_args()
P=Path(a.parsed);O=Path(a.out);O.mkdir(parents=True,exist_ok=True)
manifest=json.loads((P/'manifest.json').read_text());units=json.loads((P/'units.json').read_text())
plan=make_plan(units,64);(O/'work-plan.json').write_text(json.dumps(plan,ensure_ascii=False,separators=(',',':')))
assert all(''.join(x[2] for x in split_exact(u['en']))==u['en'] for u in units)
legacy={}
for f in Path(a.legacy).rglob('shard-*.json'):legacy.update(json.loads(f.read_text()))
for key,record in legacy.items():
 if hashlib.sha256(record['en'].encode()).hexdigest()!=key:raise ValueError('Legacy source hash failed')
 record['reviewed']=False;record['status']='quarantined-prior-draft'
Q=O/'quarantine';Q.mkdir(exist_ok=True)
(Q/'legacy-drafts.json').write_text(json.dumps(legacy,ensure_ascii=False,separators=(',',':')))
ledger=[]
for meta in manifest['pages']:
 raw=P/(str(meta['pageid'])+'.json');page=json.loads(raw.read_text())
 ledger.append({'pageid':meta['pageid'],'revision':meta.get('revision'),'title':meta['title'],'url':meta['url'],'fixedUrl':meta.get('fixedUrl'),'historyUrl':meta.get('historyUrl'),'sourceSha256':hashlib.sha256(raw.read_bytes()).hexdigest(),'units':len(page['units']),'images':len(page['images']),'externalLinks':meta.get('externalLinks',[]),'translationStatus':'not-reviewed','rawInputRetained':True})
report={'sourceRun':35304272902,'sourcePages':len(ledger),'sourceUnits':len(units),'uniqueTexts':plan['uniqueTexts'],'retainedOldDrafts':len(legacy),'oldDraftsWithUnknownTokens':sum('unknown-token' in r.get('flags',[]) for r in legacy.values()),'approvedOldDrafts':0,'shards':64,'maxMinLoadDifference':max(plan['estimatedLoads'])-min(plan['estimatedLoads']),'allSourceTextPartitionedWithoutLoss':True,'failedSourceTitles':[f['requestedTitle'] for f in manifest.get('failures',[])],'newApkBuilt':False,'completionClaim':False,'pages':ledger}
(O/'recovery-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in report.items() if k!='pages'},ensure_ascii=False,indent=2))
