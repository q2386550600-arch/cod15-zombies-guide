"""Unabridged, aligned translation drafts. No source paragraph is summarized.

Model output is not marked as semantically reviewed. Source text, per-chunk
alignment and mechanical warnings are retained for subsequent review.
"""
from pathlib import Path
import argparse,json,hashlib,re,time
import ctranslate2,sentencepiece as spm
ap=argparse.ArgumentParser();ap.add_argument('--shard',type=int,required=True);ap.add_argument('--shards',type=int,default=8);a=ap.parse_args()
P=Path('parsed');OUT=Path('translations');OUT.mkdir(exist_ok=True);M=Path('.models/nllb13')
sp=spm.SentencePieceProcessor(model_file=str(M/'sentencepiece.bpe.model'))
t=ctranslate2.Translator(str(M),device='cpu',compute_type='int8',inter_threads=1,intra_threads=4)
units=json.loads((P/'units.json').read_text());unique={hashlib.sha256(u['en'].encode()).hexdigest():u['en'] for u in units};todo=[(k,v) for k,v in sorted(unique.items()) if int(k[:8],16)%a.shards==a.shard]
# Every split has an exact source offset. No tail is truncated to model length.
def chunks(text):
 parts=[];start=0
 while start<len(text):
  end=min(len(text),start+650)
  if end<len(text):
   cut=max(text.rfind('. ',start+180,end),text.rfind('! ',start+180,end),text.rfind('? ',start+180,end),text.rfind('; ',start+180,end))
   if cut>=0:end=cut+2
   else:
    cut=text.rfind(' ',start+180,end)
    if cut>=0:end=cut+1
  parts.append((start,end,text[start:end]));start=end
 assert ''.join(p[2] for p in parts)==text
 return parts
# Short literal values (numbers, weapon codes, punctuation) are preserved exactly.
def literal(s):return not re.search('[A-Za-z]',s) or bool(re.fullmatch(r'[A-Z0-9 ._+/%×–:()-]{1,32}',s))
records={};queue=[]
for key,text in todo:
 rec={'en':text,'zh':'','chunks':[],'flags':[],'reviewed':False,'method':'NLLB-200-1.3B sentence-aligned draft'};records[key]=rec
 for start,end,part in chunks(text):
  ch={'start':start,'end':end,'source':part,'zh':None};rec['chunks'].append(ch)
  if literal(part.strip()):ch['zh']=part.strip();ch['method']='literal'
  else:queue.append((key,ch,['eng_Latn']+sp.encode(part.strip(),out_type=str)+['</s>']))
# Similar lengths improve CPU batching without changing output order.
queue.sort(key=lambda x:len(x[2]));start_time=time.monotonic()
for offset in range(0,len(queue),48):
 batch=queue[offset:offset+48]
 outputs=t.translate_batch([x[2] for x in batch],target_prefix=[['zho_Hans'] for _ in batch],beam_size=4,max_input_length=0,max_decoding_length=768,max_batch_size=2048,batch_type='tokens',return_scores=True)
 for (key,ch,tokens),out in zip(batch,outputs):
  pieces=out.hypotheses[0][1:]
  # Preserve BPE pieces literally; SentencePiece.decode maps newer vocabulary
  # entries to its unknown marker and silently loses Chinese characters.
  target=''.join(x for x in pieces if x not in ['</s>','<s>','<pad>']).replace('▁',' ').strip()
  ch['zh']=target;ch['score']=out.scores[0];ch['tokens']=len(pieces)
  if not target:records[key]['flags'].append('empty-output')
  if '<unk>' in target or '⁇' in target:records[key]['flags'].append('unknown-token')
  if len(pieces)>=767:records[key]['flags'].append('decoder-length-limit')
  src_numbers=re.findall(r'(?<![A-Za-z])\d+(?:[.,:]\d+)*',ch['source']);dst_numbers=re.findall(r'\d+(?:[.,:]\d+)*',target)
  if sorted(src_numbers)!=sorted(dst_numbers):records[key]['flags'].append('check-numeric-expression')
 if offset%240==0:print('shard',a.shard,'chunks',offset,'/',len(queue),'seconds',round(time.monotonic()-start_time,1),flush=True)
for key,rec in records.items():
 assert all(ch['zh'] is not None for ch in rec['chunks']);rec['zh']=' '.join(ch['zh'] for ch in rec['chunks']);rec['flags']=sorted(set(rec['flags']))
 if not rec['zh']:raise ValueError('Missing translation '+key)
path=OUT/f'shard-{a.shard}.json';path.write_text(json.dumps(records,ensure_ascii=False,separators=(',',':')))
report={'shard':a.shard,'units':len(todo),'chunks':len(queue),'seconds':time.monotonic()-start_time,'unknown':sum('unknown-token' in r['flags'] for r in records.values()),'lengthLimit':sum('decoder-length-limit' in r['flags'] for r in records.values()),'method':'Complete automatic draft, not a claim of completed semantic proofreading','model':'JustFrederik/nllb-200-distilled-1.3B-ct2-int8','revision':'30c36268408177b0fce2bfcfa205d877accd327d'}
(OUT/f'report-{a.shard}.json').write_text(json.dumps(report,ensure_ascii=False,indent=2));print(json.dumps(report,ensure_ascii=False,indent=2))
