"""Durable source-aligned translation journal; no automatic release approval.

Each result is committed before the next unit. Source text and engine revision
bind the checkpoint to one input. Existing suspect translations are quarantined,
not promoted to the approved set.
"""
from __future__ import annotations
import hashlib,json,os,re,sqlite3
from collections import Counter
from pathlib import Path
from typing import Any
SCHEMA_VERSION=1

def sha(text: str)->str:
 return hashlib.sha256(text.encode('utf-8')).hexdigest()

def split_exact(text: str,limit: int=360)->list[tuple[int,int,str]]:
 """Bound chunks without truncating, normalizing, or dropping whitespace."""
 if limit<32:raise ValueError('limit must be at least 32')
 chunks=[];start=0
 while start<len(text):
  stop=min(start+limit,len(text))
  if stop<len(text):
   floor=start+limit//3
   cuts=[m.end() for m in re.finditer(r'[.!?;](?:[\"\u201d\u2019\')\]]*)\s+',text[start:stop]) if start+m.end()>=floor]
   if cuts:stop=start+cuts[-1]
   else:
    cut=text.rfind(' ',floor,stop)
    if cut>=floor:stop=cut+1
  chunks.append((start,stop,text[start:stop]));start=stop
 assert ''.join(c[2] for c in chunks)==text
 assert all(b-a<=limit for a,b,_ in chunks)
 return chunks

def mechanical_flags(source: str,target: str)->list[str]:
 """No flags does NOT mean semantically reviewed or suitable for publication."""
 flags=[]
 if not target.strip():flags.append('empty')
 if any(v in target for v in ['<unk>','\u2047','\ufffd']):flags.append('unknown-token')
 src=Counter(re.findall(r'(?<![A-Za-z])\d+(?:[.,:]\d+)*',source));dst=Counter(re.findall(r'\d+(?:[.,:]\d+)*',target))
 if src!=dst:flags.append('numeric-expression-review')
 if len(source)>180 and len(target)<len(source)*.11:flags.append('suspiciously-short')
 if re.search(r'(.{3,20})\1{5}',target):flags.append('repetition')
 return flags

class Journal:
 def __init__(self,path: Path|str):
  self.path=Path(path);self.path.parent.mkdir(parents=True,exist_ok=True)
  self.db=sqlite3.connect(self.path)
  self.db.execute('PRAGMA journal_mode=DELETE');self.db.execute('PRAGMA synchronous=FULL')
  self.db.execute('CREATE TABLE IF NOT EXISTS records(source_hash TEXT NOT NULL,engine TEXT NOT NULL,source TEXT NOT NULL,result TEXT NOT NULL,PRIMARY KEY(source_hash,engine))');self.db.commit()
 def get(self,source: str,engine: str)->dict[str,Any]|None:
  row=self.db.execute('SELECT source,result FROM records WHERE source_hash=? AND engine=?',(sha(source),engine)).fetchone()
  if not row:return None
  if row[0]!=source:raise ValueError('Hash collision or corrupt source')
  return json.loads(row[1])
 def put(self,source: str,engine: str,chunks: list[dict[str,Any]],reviewed: bool=False)->dict[str,Any]:
  expected=0
  for chunk in chunks:
   if chunk['start']!=expected or source[chunk['start']:chunk['end']]!=chunk['source']:raise ValueError('Source offset mismatch')
   expected=chunk['end']
   if chunk.get('zh') is None:raise ValueError('Incomplete source chunk')
  if expected!=len(source):raise ValueError('Untranslated source tail')
  target='\n'.join(c['zh'] for c in chunks)
  flags=sorted(set(mechanical_flags(source,target)+[f for c in chunks for f in c.get('flags',[])]))
  if reviewed and flags:raise ValueError('Flagged record needs documented review override, not silent approval')
  rec={'en':source,'zh':target,'chunks':chunks,'flags':flags,'reviewed':reviewed,'status':'reviewed' if reviewed else ('needs-review' if flags else 'draft'),'engine':engine,'sourceHash':sha(source)}
  with self.db:self.db.execute('INSERT OR REPLACE INTO records VALUES(?,?,?,?)',(sha(source),engine,source,json.dumps(rec,ensure_ascii=False)))
  return rec
 def export(self,out: Path|str)->None:
  dest=Path(out);dest.parent.mkdir(parents=True,exist_ok=True)
  content={h:json.loads(r) for h,r in self.db.execute('SELECT source_hash,result FROM records ORDER BY source_hash')}
  temp=dest.with_suffix(dest.suffix+'.tmp')
  with temp.open('w',encoding='utf-8') as f:json.dump(content,f,ensure_ascii=False);f.flush();os.fsync(f.fileno())
  os.replace(temp,dest)
 def close(self)->None:self.db.close()

def make_plan(units: list[dict[str,Any]],count: int=64)->dict[str,Any]:
 if count<=0:raise ValueError('count must be positive')
 unique={}
 for u in units:
  k=sha(u['en'])
  if k in unique and unique[k]['source']!=u['en']:raise ValueError('Source collision')
  unique.setdefault(k,{'hash':k,'source':u['en'],'unitIds':[]})['unitIds'].append(u['id'])
 work=[[] for _ in range(count)];loads=[0]*count
 for item in sorted(unique.values(),key=lambda x:(-len(x['source']),x['hash'])):
  slot=min(range(count),key=lambda i:(loads[i],i));work[slot].append(item);loads[slot]+=max(40,len(item['source']))
 assert sum(len(t['unitIds']) for batch in work for t in batch)==len(units)
 return {'schema':SCHEMA_VERSION,'sourceUnits':len(units),'uniqueTexts':len(unique),'shards':work,'estimatedLoads':loads,'reviewedUnits':0,'note':'All source units remain; allocation is scheduling, not editorial filtering.'}
