from pathlib import Path
import json,time,hashlib,requests
import ctranslate2,sentencepiece as spm
MODEL=Path('.models/nllb13');MODEL.mkdir(exist_ok=True,parents=True);OUT=Path('translation-pilot');OUT.mkdir(exist_ok=True)
REV='30c36268408177b0fce2bfcfa205d877accd327d'
for f in ['model.bin','config.json','shared_vocabulary.txt','sentencepiece.bpe.model']:
 p=MODEL/f
 if not p.exists():
  r=requests.get('https://huggingface.co/JustFrederik/nllb-200-distilled-1.3B-ct2-int8/resolve/'+REV+'/'+f,stream=True,timeout=(15,120));r.raise_for_status()
  with p.open('wb') as dst:
   for chunk in r.iter_content(2**20):dst.write(chunk)
 print(f,p.stat().st_size,flush=True)
sp=spm.SentencePieceProcessor(model_file=str(MODEL/'sentencepiece.bpe.model'))
t=ctranslate2.Translator(str(MODEL),device='cpu',compute_type='int8',inter_threads=1,intra_threads=4)
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
start=time.monotonic();batch=[['eng_Latn']+sp.encode(s,out_type=str)+['</s>'] for s in samples]
out=t.translate_batch(batch,target_prefix=[['zho_Hans'] for _ in batch],beam_size=4,max_decoding_length=512)
rows=[{'en':s,'zh':sp.decode(r.hypotheses[0][1:])} for s,r in zip(samples,out)]
(OUT/'nllb-pilot.json').write_text(json.dumps({'model':'JustFrederik/nllb-200-distilled-1.3B-ct2-int8','revision':REV,'seconds':time.monotonic()-start,'rows':rows},ensure_ascii=False,indent=2));print(json.dumps(rows,ensure_ascii=False,indent=2),flush=True)
