"""Keep every article image slot and its original file/credit link.
Download a bounded display rendition; missing images remain explicit links.
No image is relabelled as CC merely because surrounding text is CC.
"""
from pathlib import Path
import json,re,time,hashlib,concurrent.futures,threading
from urllib.parse import quote
import requests
from PIL import Image
from io import BytesIO
P=Path('parsed');OUT=Path('wiki-media');OUT.mkdir(exist_ok=True);(OUT/'files').mkdir(exist_ok=True)
man=json.loads((P/'manifest.json').read_text());refs=[]
for m in man['pages']:refs+=json.loads((P/(str(m['pageid'])+'.json')).read_text())['images']
byname={}
for im in refs:
 name=im['name'] or im['originalUrl'];byname.setdefault(name,[]).append(im)
metadata={};names=[n for n in byname if not n.startswith('http')]
for offset in range(0,len(names),40):
 batch=names[offset:offset+40]
 try:
  r=requests.get('https://callofduty.fandom.com/api.php',params={'action':'query','titles':'|'.join('File:'+n for n in batch),'prop':'imageinfo','iiprop':'url|size|mime|extmetadata|user|timestamp','iiurlwidth':1280,'format':'json'},timeout=(10,40));r.raise_for_status();j=r.json()
  for page in j.get('query',{}).get('pages',{}).values():
   if page.get('imageinfo'):metadata[page['title'][5:].replace('_',' ')]=page['imageinfo'][0]
 except Exception as exc:print('metadata batch failed',offset,repr(exc),flush=True)
 print('metadata',offset,'/',len(names),flush=True);time.sleep(.2)
(OUT/'file-metadata.json').write_text(json.dumps(metadata,ensure_ascii=False,separators=(',',':')))
stop=threading.Event()
def one(item):
 name,uses=item;first=uses[0];info=metadata.get(name.replace('_',' '),{});url=info.get('thumburl') or info.get('url') or first['url']
 rec={'name':name,'url':url,'originalUrl':info.get('url') or first['originalUrl'],'filePage':info.get('descriptionurl') or first.get('filePage'),'info':info,'referenceIds':[x['id'] for x in uses],'downloaded':False,'rendition':'publisher 1280px preview where available; original file linked'}
 if stop.is_set():rec['error']='Stopped after CDN rate limit';return rec
 try:
  r=requests.get(url,timeout=(10,40))
  if r.status_code==429:stop.set();raise RuntimeError('CDN rate limit; stop new downloads')
  r.raise_for_status();raw=r.content
  if len(raw)>20*1024*1024:raise ValueError('Preview exceeds 20MB; retain original link instead')
  ct=r.headers.get('Content-Type','').split(';')[0]
  if ct=='image/svg+xml':ext='svg';w=int(first.get('width') or 200);h=int(first.get('height') or 200)
  else:
   img=Image.open(BytesIO(raw));img.verify();img=Image.open(BytesIO(raw));w,h=img.size;ext={'JPEG':'jpg','PNG':'png','GIF':'gif','WEBP':'webp'}.get(img.format)
   if not ext:raise ValueError('Unsupported image format '+str(img.format))
  digest=hashlib.sha256(raw).hexdigest();file='files/'+digest[:28]+'.'+ext;(OUT/file).write_bytes(raw);rec.update({'downloaded':True,'file':file,'sha256':digest,'bytes':len(raw),'width':w,'height':h})
 except Exception as exc:rec['error']=repr(exc)
 return rec
results=[]
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
 for rec in pool.map(one,list(byname.items())):
  results.append(rec)
  if len(results)%100==0:print('images',len(results),'/',len(byname),'ok',sum(x['downloaded'] for x in results),flush=True)
(OUT/'catalog.json').write_text(json.dumps({'files':results,'references':len(refs),'uniqueNames':len(byname),'downloaded':sum(x['downloaded'] for x in results),'bytes':sum(x.get('bytes',0) for x in results),'rights':'Images retain individual rights; refer to each file metadata and original description. Article text licensing does not automatically cover media.'},ensure_ascii=False,separators=(',',':')))
try:
 r=requests.get('https://community.fandom.com/api.php',params={'action':'parse','page':'Help:Licensing','prop':'text|wikitext|revid','format':'json'},timeout=35);r.raise_for_status();(OUT/'license-policy.json').write_bytes(r.content)
except Exception as exc:(OUT/'license-policy-error.txt').write_text(repr(exc))
print('Done',len(results),sum(x['downloaded'] for x in results),sum(x.get('bytes',0) for x in results),flush=True)
