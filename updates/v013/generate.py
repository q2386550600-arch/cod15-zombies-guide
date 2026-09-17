"""Compile independent Chinese procedures with source-section and image provenance."""
from pathlib import Path
import json,runpy,re,hashlib,argparse,subprocess
R=Path(__file__).resolve().parent
arg=argparse.ArgumentParser();arg.add_argument('--assets',type=Path,default=Path('app/src/main/assets'));arg.add_argument('--source',type=Path,default=Path('.source'));a=arg.parse_args()
E=json.loads((R/'export.json').read_text());contents={}
for f in sorted((R/'content').glob('bo*.py')):
 for k,v in runpy.run_path(str(f))['CONTENT'].items():
  if k in contents:raise ValueError('Duplicate guide '+k)
  contents[k]=v
B=runpy.run_path(str(R/'content/bindings.py'));bindings=B['BINDINGS'];choices=B['CHOICES']
assert len(contents)==22
for k,v in B['EXTRA'].items():contents[k].update(v)
contents['mined-games'][2][1]=contents['mined-games'][2][1].replace('在断头台装好、对应语音进入此阶段后，','')
contents['salvation-lies-above'][40]=[x.replace('範火','篝火') for x in contents['salvation-lies-above'][40]]
# The hand-carry restriction follows the final candidate image in the source;
# surface it before any recipe, not as an invisible tail of a location caption.
contents['greek-tragedy'][10].append('每只手单独制作：每做下一只救赎之手都要再取一只沉睡之手，一次只能推进一只。已经持有救赎之手时，先把它放回对应神龛，再取新的沉睡之手开始另一条制作路线。')
docs={};audit={'guides':{},'scope':'Chinese procedural adaptation of 22 main-quest sources, plus explicitly cited preparation. Not a verbatim publisher translation; recommended loadout tables, lore, credits and embedded videos are references, not counted as mandatory procedures.'}
for key,src in E['source']['guides'].items():
 sections={};procedures=contents[key];images=E['media']['guides'][key]['images'];zh=E['captions'][key]
 for sec in src['sections']:
  n=int(sec['id'].rsplit('-',1)[1]);data=dict(sec);data['texts']=procedures.get(n,[]);data['kind']='procedure' if data['texts'] else 'group'
  meta=bool(re.search(r'Recommended|Video|Credits|[Gg]uide [Bb]y|Walkthrough|[Ww]alkthrough',sec['heading']))
  if meta and not data['texts']:data['kind']='reference'
  if n==0 and not data['texts']:data['kind']='introduction'
  if not data['texts'] and sec['images'] and not meta:
   data['kind']='locations';data['texts']=['候选点：'+zh[i]['where']+'。按本节对应原图检查。' for i in sec['images']]
  sections[sec['id']]=data
 if key=='little-lost-girl':sections[key+'-14']['texts']=['开始天降火雨前，至少一位玩家已经取得G轰击；没有就展开下方G轰击制作，不能拿普通手雷代替。'];sections[key+'-14']['kind']='procedure'
 for num,texts in procedures.items():
  sid=key+'-'+str(num)
  if sid not in sections:sections[sid]={'id':sid,'heading':'开电与强化机：信号增幅器','level':3,'parent':None,'images':[],'texts':texts,'kind':'procedure','extraSources':B.get('EXTRA_SOURCES',{}).get(key,{}).get(str(num),[]),'startLine':None,'endLine':None}
 doc=dict(src);doc['sections']=sections;doc['order']=list(sections);doc['paragraphs']=sum(len(s['texts']) for s in sections.values());docs[key]=doc
 audit['guides'][key]={'procedureSections':sum(s['kind']=='procedure' for s in sections.values()),'locationSections':sum(s['kind']=='locations' for s in sections.values()),'operatingParagraphs':doc['paragraphs'],'referenceOnlySections':[s['id'] for s in sections.values() if s['kind']=='reference']}
def frames(key,items):
 out=[]
 for v in items:
  n=v if isinstance(v,int) else v['section'];sec=docs[key]['sections'].get(key+'-'+str(n))
  if not sec:raise ValueError(f'No section {key}:{n}')
  start=0 if isinstance(v,int) else v['first'];end=None if isinstance(v,int) else v['last']
  selected=list(enumerate(sec['texts']))[start:end]
  if not selected:raise ValueError(f'Empty stage segment {key}:{v}')
  for i,text in selected:out.append({'id':f'{sec["id"]}/p{i}','section':sec['id'],'paragraph':i,'text':text,'images':sec['images']})
 return out
stages={}
for mk,b in bindings.items():
 key=E['source']['maps'][mk]['guide'];assert len(b)==len(E['maps'][mk]['steps']),(mk,len(b),len(E['maps'][mk]['steps']))
 stages[mk]=[]
 for i,items in enumerate(b):
  stage={'frames':frames(key,items),'choices':[]}
  if i in choices.get(mk,{}):
   c=choices[mk][i];stage['choiceTitle']=c['title'];stage['mustCompleteAll']=bool(c.get('mustCompleteAll'))
   for label,ids in zip(c['labels'],c['options']):stage['choices'].append({'title':label,'frames':frames(key,ids)})
  stages[mk].append(stage)
ts=(a.source/'src_data/gk-values.ts').read_text();obj=ts.split('export const valveRoutes: ValveRoutes =',1)[1].strip()
route_js='const data='+re.sub(r'\bas const\b','',obj)+';console.log(JSON.stringify(data))'
valves=json.loads(subprocess.check_output(['node','-e',route_js],text=True));assert len(valves)==30
for k,v in valves.items():assert len(v)==6 and list(v.values()).count(None)==1 and all(x is None or x in (1,2,3) for x in v.values())
valves_hash=hashlib.sha256(ts.encode()).hexdigest()
result={'revision':13,'sourceCommit':E['source']['sourceCommit'],'docs':docs,'stages':stages,'valves':valves,'valveSourceHash':valves_hash,'audit':audit}
a.assets.mkdir(parents=True,exist_ok=True)
(a.assets/'offline-guides.js').write_text('window.OFFLINE_GUIDES='+json.dumps(result,ensure_ascii=False,separators=(',',':'))+';\n')
audit.update({'guideCount':len(docs),'mapVersionCount':len(stages),'operatingParagraphs':sum(d['paragraphs'] for d in docs.values()),'stageFrames':sum(len(s['frames']) for x in stages.values() for s in x),'originalImages':1148,'communityPlans':134,'valveCombinations':len(valves),'notInGameTested':True})
(a.assets/'offline-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in audit.items() if k!='guides'},ensure_ascii=False,indent=2))
