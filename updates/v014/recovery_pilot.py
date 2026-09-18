"""Bounded tokenizer/translation probe. Its output is never marked publishable."""
import argparse,json,os,time
from pathlib import Path
from recovery_state import Journal,split_exact,mechanical_flags,sha
p=argparse.ArgumentParser();p.add_argument('--parsed',default='parsed');p.add_argument('--out',default='recovery/pilot');args=p.parse_args()
out=Path(args.out);out.mkdir(parents=True,exist_ok=True)
report={'publishable':False,'status':'started','samples':[]}
try:
 import ctranslate2
 from huggingface_hub import snapshot_download,HfApi
 from transformers import AutoTokenizer
 name='OpenNMT/nllb-200-distilled-1.3B-ct2-int8'
 info=HfApi().model_info(name,revision='70f572a')
 model=snapshot_download(name,revision=info.sha,allow_patterns=['model.bin','config.json','shared_vocabulary.json','tokenizer*','special_tokens_map.json','sentencepiece.bpe.model'])
 tokenizer=AutoTokenizer.from_pretrained(model,src_lang='eng_Latn',local_files_only=True,trust_remote_code=False)
 translator=ctranslate2.Translator(model,device='cpu',compute_type='int8',intra_threads=2,inter_threads=1)
 engine=f'{name}@{info.sha}/tokenizer/v2';report['engine']=engine
 article=json.loads((Path(args.parsed)/'677503.json').read_text())
 rows=[u for u in article['units'] if u['tag'] not in ['h2','h3'] and len(u['en'])>90][:12]
 report['sourceUnits']=len(rows)
 journal=Journal(out/'checkpoint.sqlite');start_time=time.monotonic()
 for u in rows:
  s=u['en'];existing=journal.get(s,engine)
  if existing:report['samples'].append({'id':u['id'],**existing});continue
  pieces=[]
  for a,b,part in split_exact(s,360):
   source=tokenizer.convert_ids_to_tokens(tokenizer.encode(part))
   result=translator.translate_batch([source],target_prefix=[['zho_Hans']],beam_size=4,max_input_length=0,max_decoding_length=384,return_scores=True)[0]
   target=result.hypotheses[0]
   if target and target[0]=='zho_Hans':target=target[1:]
   output=tokenizer.decode(tokenizer.convert_tokens_to_ids(target),skip_special_tokens=False).replace('</s>','').replace('<pad>','').strip()
   flags=mechanical_flags(part,output)
   if len(target)>=383:flags.append('decoder-cap-hit')
   pieces.append({'start':a,'end':b,'source':part,'zh':output,'flags':flags})
  rec=journal.put(s,engine,pieces);journal.export(out/'checkpoint.json')
  report['samples'].append({'id':u['id'],**rec})
  (out/'pilot.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
  print('SAVED',u['id'],'flags=',rec['flags'],'seconds=',round(time.monotonic()-start_time),flush=True)
 journal.close();report['status']='drafts-produced-for-review';report['seconds']=time.monotonic()-start_time
 report['flagged']=sum(bool(s['flags']) for s in report['samples'])
 report['releaseGate']='BLOCKED: requires source-by-source semantic review regardless of automatic checks.'
except Exception as e:
 report['status']='failed';report['error']=repr(e);raise
finally:
 (out/'pilot.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
 print(json.dumps({k:v for k,v in report.items() if k!='samples'},ensure_ascii=False,indent=2),flush=True)
