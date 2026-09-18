"""Continue the exact preview3 corpus. Never summarize or auto-approve drafts.
Public source text only is sent to the translation transport. Source units,
structure, attribution, and the forty approved translations are immutable.
"""
from __future__ import annotations
import argparse, concurrent.futures as cf, hashlib, io, json, re, threading, time, zipfile
from pathlib import Path
from urllib.parse import urlparse
import requests
from PIL import Image
ROOT=Path('completion'); ROOT.mkdir(exist_ok=True)
ASSETS=Path('app/src/main/assets'); CORPUS=ASSETS/'faithful'
LOCAL=threading.local(); ENGINE='google-gtx-en-zh-CN-protected-v1'
def read_js(p):
    s=p.read_text(encoding='utf-8'); return json.loads(s[s.index('(')+1:s.rindex(')')])
def emit_json(p,d):
    p.parent.mkdir(parents=True,exist_ok=True); tmp=p.with_suffix(p.suffix+'.tmp')
    tmp.write_text(json.dumps(d,ensure_ascii=False,separators=(',',':')),encoding='utf-8');tmp.replace(p)
def restore():
    with zipfile.ZipFile('.base/v014-reader40-generated-sources.zip') as z:
        for n in z.namelist():
            p=Path(n); assert not p.is_absolute() and '..' not in p.parts
            if n.startswith('app/src/') or n=='app/build.gradle':
                p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
    with zipfile.ZipFile('.base/COD_Zombies_Guide_v0.14.0-preview3.apk') as z:
        for n in z.namelist():
            if n.startswith('assets/') and not n.endswith('/'):
                p=Path('app/src/main')/n;assert '..' not in p.parts
                p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(z.read(n))
def session():
    if not hasattr(LOCAL,'session'):
        LOCAL.session=requests.Session()
        LOCAL.session.headers['User-Agent']='COD-source-reader/0.14 (public-source offline reading; requests)'
    return LOCAL.session
GLOSSARY={
 'Call of Duty: Black Ops III':'使命召唤：黑色行动3','Call of Duty: Black Ops II':'使命召唤：黑色行动2',
 'Call of Duty: Black Ops 4':'使命召唤：黑色行动4','Call of Duty: Black Ops 6':'使命召唤：黑色行动6',
 'Call of Duty: Black Ops':'使命召唤：黑色行动','Call of Duty: World at War':'使命召唤：战争世界',
 'Pack-a-Punch Machine':'武器升级机','Pack-a-Punch':'武器升级','Mystery Box':'神秘箱',
 'Juggernog':'厚血汽水（Juggernog）','Quick Revive':'快速救援（Quick Revive）',
 'Speed Cola':'快速换弹汽水（Speed Cola）','Double Tap Root Beer':'双倍射速汽水（Double Tap）',
 'Double Tap II':'双倍射速2.0（Double Tap II）','Mule Kick':'骡子踢（Mule Kick）',
 'Stamin-Up':'持久耐力（Stamin-Up）','PHD Flopper':'PHD防爆汽水（PHD Flopper）',
 "Widow's Wine":'寡妇之酒（Widow’s Wine）','GobbleGum':'泡泡糖（GobbleGum）',
 'Shadows of Evil':'邪恶之影','Der Eisendrache':'德尔艾森德拉赫','Zetsubou No Shima':'绝望之岛',
 'Gorod Krovi':'血色城堡','Mob of the Dead':'亡者监狱','Blood of the Dead':'亡者之血',
 'Call of the Dead':'亡者召唤','Kino der Toten':'亡者剧院','Nacht der Untoten':'亡者之夜',
 'Shi No Numa':'死亡沼泽','Verrückt':'疯狂疗养院','Shangri-La':'香格里拉',
 'Nuketown Zombies':'核弹镇僵尸','Voyage of Despair':'绝望之旅','Dead of the Night':'死亡之夜',
 'Ancient Evil':'远古邪恶','Alpha Omega':'阿尔法·欧米伽','Tag der Toten':'亡者之日',
 'TranZit':'迁徙','Die Rise':'大厦','Apothicon Servant':'阿波西康仆从','Apothicon Sword':'阿波西康之剑',
 'Wrath of the Ancients':'远古之怒',"Hell's Retriever":'地狱猎犬斧',"Hell's Redeemer":'地狱救赎者',
 'Golden Spork':'黄金叉勺','Spectral Shield':'灵魂盾','Zombie Shield':'僵尸盾',
 'Ragnarok DG-4':'诸神黄昏DG-4','Skull of Nan Sapwe':'南萨普韦之颅','Gauntlet of Siegfried':'齐格弗里德护手',
 'Maxis Drone':'麦克西斯无人机','G-Strike':'G轰击信标','Navcard':'导航卡',
 'Hand of Charon':'卡戎之手','Hand of Gaia':'盖亚之手','Hand of Hemera':'赫墨拉之手','Hand of Ouranos':'乌拉诺斯之手',
 'Fallen Hand':'堕落之手','Redeemed Hand':'救赎之手','Exalted Hand':'尊贵之手',
 'Death of Orion':'猎户座之死',"Alistair's Folly":'阿利斯泰尔的愚行',"Apollo's Will":'阿波罗之志',
 'Guard of Fafnir':'法夫尼尔之盾','Brazen Bull':'铜牛盾','Pegasus Strike':'飞马轰击',
 'Samantha Maxis':'萨曼莎·麦克西斯','Edward Richtofen':'爱德华·里希托芬',
 'Ludvig Maxis':'路德维希·麦克西斯','Ludwig Maxis':'路德维希·麦克西斯',
 'Nikolai Belinski':'尼古莱·贝林斯基','Takeo Masaki':'正崎武雄','Tank Dempsey':'坦克·邓普西',
 'Richtofen':'里希托芬','Maxis':'麦克西斯','Dempsey':'邓普西','Nikolai':'尼古莱','Takeo':'武雄',
 'Samantha':'萨曼莎','Primis':'Primis小队','Ultimis':'Ultimis小队','Victis':'Victis小队',
 'Afterlife':'灵魂状态（Afterlife）','Golden Gate Bridge':'金门大桥',
 'Perk-a-Cola':'技能汽水','Perk-a-Colas':'技能汽水','Max Ammo':'弹药全满',
}
WORDS=re.compile('|'.join(r'(?<![A-Za-z])'+re.escape(k)+r'(?![A-Za-z])' for k in sorted(GLOSSARY,key=len,reverse=True)))
NUMBERS=re.compile(r'\d+(?:[.,:/\-]\d+)*(?:%|\+)?')
TOKEN=re.compile(r'\[P\s*(\d{5})\s*\]'); MARK=re.compile(r'\[Z\s*(\d{5})\s*\]')
def protect(text):
    vals=[]
    pattern=re.compile(WORDS.pattern+'|https?://[^\\s<>]+|'+NUMBERS.pattern)
    def sub(m):
        raw=m.group(); vals.append(GLOSSARY.get(raw,raw));return '[P%05d]'%(len(vals)-1)
    return pattern.sub(sub,text),vals
def unprotect(text,vals):
    found=[int(m.group(1)) for m in TOKEN.finditer(text)]
    if sorted(found)!=list(range(len(vals))):raise ValueError('protected literal missing or duplicated')
    result=TOKEN.sub(lambda m:vals[int(m.group(1))],text).strip()
    if re.search(r'\[(?:P|Z)\s*\d{5}',result) or not result:raise ValueError('unfinished translation')
    return result
def request_translation(text):
    last=None
    for attempt in range(5):
        try:
            r=session().get('https://translate.googleapis.com/translate_a/single',params={'client':'gtx','sl':'en','tl':'zh-CN','dt':'t','q':text},timeout=(10,35))
            if r.status_code==429:
                time.sleep(min(60,4*2**attempt));last=RuntimeError('translation rate limited');continue
            r.raise_for_status();j=r.json()
            if not isinstance(j,list) or not isinstance(j[0],list):raise ValueError('unexpected translation response')
            out=''.join(x[0] for x in j[0] if x and isinstance(x[0],str))
            if not out:raise ValueError('empty translation transport response')
            return out
        except Exception as e:last=e;time.sleep(min(15,1+2**attempt))
    raise RuntimeError(str(last))
def translate_batch(batch):
    if not batch:return []
    prepared=[protect(t) for t in batch]
    q='\n'.join('[Z%05d]\n%s'%(i,p[0]) for i,p in enumerate(prepared))
    try:
        out=request_translation(q);matches=list(MARK.finditer(out))
        if [int(m.group(1)) for m in matches]!=list(range(len(batch))):raise ValueError('source-boundary mismatch')
        results=[]
        for i,m in enumerate(matches):
            stop=matches[i+1].start() if i+1<len(matches) else len(out)
            zh=unprotect(out[m.end():stop],prepared[i][1])
            results.append({'en':batch[i],'zh':zh,'method':ENGINE,'reviewed':False})
        return results
    except Exception as e:
        if len(batch)>1:
            middle=len(batch)//2;return translate_batch(batch[:middle])+translate_batch(batch[middle:])
        return [{'en':batch[0],'error':str(e),'reviewed':False}]
def translate_all(docs):
    cache={};checkpoint=ROOT/'translation-checkpoint.jsonl'
    if checkpoint.exists():
        for line in checkpoint.read_text().splitlines():
            try:
                r=json.loads(line)
                if r.get('method')==ENGINE and r.get('zh'):cache[r['en']]=r
            except (ValueError,KeyError):pass
    approved={}
    for d in docs:
        if d['translated']:
            for u in d['units']:approved.setdefault(u['en'],set()).add(u['zh'])
    memory={k:next(iter(v)) for k,v in approved.items() if len(v)==1}
    texts=sorted({u['en'] for d in docs if not d['translated'] for u in d['units']}|{d['metadata']['title'] for d in docs if not d['translated']})
    for en in texts:
        if en in cache:continue
        if en in memory:cache[en]={'en':en,'zh':memory[en],'method':'existing-reviewed-exact-match','reviewed':False}
        elif not re.search('[A-Za-z]',en):cache[en]={'en':en,'zh':en,'method':'literal-numeric-or-symbol','reviewed':False}
        elif en in GLOSSARY:cache[en]={'en':en,'zh':GLOSSARY[en],'method':'bilingual-glossary','reviewed':False}
    todo=[t for t in texts if t not in cache];batches=[];batch=[];n=0
    for t in todo:
        size=len(protect(t)[0])+18
        if batch and (n+size>3300 or len(batch)>=44):batches.append(batch);batch=[];n=0
        batch.append(t);n+=size
    if batch:batches.append(batch)
    print('TRANSLATION batches',len(batches),'units',len(todo),'already available',len(cache),flush=True)
    failures=[]
    with checkpoint.open('a',encoding='utf-8') as log,cf.ThreadPoolExecutor(max_workers=4) as pool:
        futures=[pool.submit(translate_batch,b) for b in batches]
        for number,future in enumerate(cf.as_completed(futures),1):
            for r in future.result():
                log.write(json.dumps(r,ensure_ascii=False)+'\n')
                if r.get('zh'):cache[r['en']]=r
                else:failures.append(r)
            log.flush()
            if number%20==0:print('TRANSLATION',number,'/',len(batches),'cache',len(cache),'errors',len(failures),flush=True)
    emit_json(ROOT/'translation-cache.json',cache);emit_json(ROOT/'translation-errors.json',failures)
    return cache
def download_one(url):
    rec={'originalUrl':url,'downloaded':False}
    if urlparse(url).scheme!='https' or urlparse(url).hostname not in ['static.wikia.nocookie.net','vignette.wikia.nocookie.net','images.wikia.com']:
        rec['error']='Non-whitelisted source host; original link retained';return rec
    key=hashlib.sha256(url.encode()).hexdigest()[:24];meta=ROOT/'media-checkpoints'/f'{key}.json'
    if meta.exists():
        r=json.loads(meta.read_text());p=ASSETS/r.get('localSrc','MISSING')
        if r.get('downloaded') and p.is_file() and hashlib.sha256(p.read_bytes()).hexdigest()==r['sha256']:return r
    last=None
    for attempt in range(3):
        try:
            response=session().get(url,timeout=(10,40))
            if response.status_code==429:time.sleep(5*2**attempt);last=RuntimeError('CDN rate limit');continue
            response.raise_for_status();raw=response.content
            if len(raw)>80*1024*1024:raise ValueError('Original exceeds 80 MiB; link retained, never replaced by thumbnail')
            mime=response.headers.get('Content-Type','').split(';')[0]
            if mime=='image/svg+xml':
                import xml.etree.ElementTree as ET
                e=ET.fromstring(raw);assert e.tag.endswith('svg');ext='svg';w=h=None
            else:
                with Image.open(io.BytesIO(raw)) as im:
                    w,h=im.size;ext={'JPEG':'jpg','PNG':'png','GIF':'gif','WEBP':'webp'}.get(im.format);im.verify()
                if not ext:raise ValueError('Unsupported original image encoding')
            local=f'faithful/media/{key}.{ext}';p=ASSETS/local;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(raw)
            rec.update(downloaded=True,localSrc=local,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),width=w,height=h,mime=mime)
            emit_json(meta,rec);return rec
        except Exception as e:last=e;time.sleep(1+2**attempt)
    rec['error']=str(last);emit_json(meta,rec);return rec
def download_all(docs):
    refs=[im for d in docs for im in d['images']];urls=sorted({im.get('originalUrl') or im.get('url') for im in refs});records=[]
    with cf.ThreadPoolExecutor(max_workers=8) as pool:
        for n,r in enumerate(pool.map(download_one,urls),1):
            records.append(r)
            if n%100==0:print('MEDIA',n,'/',len(urls),'ok',sum(x['downloaded'] for x in records),'MiB',round(sum(x.get('bytes',0) for x in records)/1048576),flush=True)
    report={'uniqueOriginalUrls':len(urls),'sourceReferences':len(refs),'downloaded':sum(x['downloaded'] for x in records),'bytes':sum(x.get('bytes',0) for x in records),'files':records,'policy':'Publisher original-size URL bytes retained without resizing/recompression; original URLs and individual file-page credits preserved. No transfer of media rights is claimed.'}
    emit_json(ROOT/'media-audit.json',report);return {r['originalUrl']:r for r in records}
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--skip-restore',action='store_true');a=ap.parse_args()
    if not a.skip_restore:restore()
    docs=[read_js(p) for p in sorted(CORPUS.glob('p*.js'))];assert len(docs)==182 and sum(len(d['units']) for d in docs)==54189
    with cf.ThreadPoolExecutor(max_workers=2) as pool:
        ft=pool.submit(translate_all,docs);fm=pool.submit(download_all,docs);translations=ft.result();media=fm.result()
    emit_json(ROOT/'materials-summary.json',{'translationCacheRecords':len(translations),'mediaAvailable':sum(r['downloaded'] for r in media.values()),'mediaUrls':len(media),'automaticDraftsAreNotApproved':True})
    with zipfile.ZipFile(ROOT/'translation-materials.zip','w',zipfile.ZIP_DEFLATED) as z:
        for p in ROOT.glob('*.json'):z.write(p,p.name)
        z.write(ROOT/'translation-checkpoint.jsonl','translation-checkpoint.jsonl')
    with zipfile.ZipFile(ROOT/'original-image-cache.zip','w',zipfile.ZIP_STORED) as z:
        for p in (CORPUS/'media').glob('*'):z.write(p,str(p.relative_to(ASSETS)))
    print((ROOT/'materials-summary.json').read_text(),flush=True)
if __name__=='__main__':main()
