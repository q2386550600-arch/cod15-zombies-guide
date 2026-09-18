"""Pilot self-hosted sentence translation on public wiki prose. No paid service."""
from pathlib import Path
import json,time,hashlib,requests
import ctranslate2,sentencepiece as spm
OUT=Path('translation-pilot');OUT.mkdir(exist_ok=True)
MODEL=Path('.models/opus-en-zh');MODEL.mkdir(exist_ok=True,parents=True)
REV='b86e9540537d109f999f23f0f6de71b99bd9ad0a'
for f in ['model.bin','config.json','shared_vocabulary.json','source.spm','target.spm']:
 p=MODEL/f
 if not p.exists():
  r=requests.get('https://huggingface.co/Sams200/opus-mt-en-zh/resolve/'+REV+'/'+f,stream=True,timeout=120);r.raise_for_status()
  with p.open('wb') as out:
   for chunk in r.iter_content(2**20):out.write(chunk)
 print(f,p.stat().st_size,hashlib.sha256(p.read_bytes()).hexdigest(),flush=True)
src=spm.SentencePieceProcessor(model_file=str(MODEL/'source.spm'));tgt=spm.SentencePieceProcessor(model_file=str(MODEL/'target.spm'))
translator=ctranslate2.Translator(str(MODEL),device='cpu',compute_type='int8',inter_threads=1,intra_threads=4)
samples=[
'The photograph is hidden behind the monitor. Do not shoot the monitor. Go to the upper floor of the Saloon.',
'The player must shoot the nameplates in the following order: George Washington, Benjamin Franklin, Alexander Hamilton, Abraham Lincoln.',
'If the player steps in the mud, the tablet becomes dirty and must be washed again.',
'To charge the lantern, kill ten witches while the player holding the lantern is nearby.',
'Players must stand near the Guillotine and activate the Time Bomb. The switch cannot be installed during round infinity.',
'The player must now shoot the correct numbers on the split-flap display and then press the red button. The codes must be entered in the following order.',
'Once the skull is floating and stops absorbing souls, the player can pick it up. This process must be repeated for all four skulls.',
'A maximum of six perks can be purchased, although more may be obtained through other means.',
'In the final stage, the boss is invulnerable until its shield is lowered. All players should fire at the exposed weak point.',
'The Thundergun can only be obtained from the Mystery Box, and can be upgraded using the Pack-a-Punch Machine.'
]
results=[]
for prefix in ['', '>>cmn_Hans<<']:
 batch=[([prefix] if prefix else [])+src.encode(s,out_type=str) for s in samples];start=time.monotonic()
 out=translator.translate_batch(batch,beam_size=4,max_decoding_length=512)
 for s,r in zip(samples,out):results.append({'prefix':prefix,'en':s,'zh':tgt.decode(r.hypotheses[0])})
 print('seconds',time.monotonic()-start,flush=True)
(OUT/'pilot.json').write_text(json.dumps({'model':'Sams200/opus-mt-en-zh','revision':REV,'rows':results},ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2))
