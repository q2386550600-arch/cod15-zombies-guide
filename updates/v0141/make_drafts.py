"""Produce explicitly UNREVIEWED Chinese drafts. Never modify original source trees.
Only public, already archived Call of Duty Wiki text is sent for translation.
The existing reviewed translations are immutable. An interrupted run preserves its cache.
"""
from __future__ import annotations
import argparse, collections, concurrent.futures, hashlib, json, pathlib, re, threading, time, urllib.error, urllib.parse, urllib.request

GLOSSARY = {
 'Pack-a-Punched':'强化过的','Pack-a-Punch Machine':'武器强化机','Pack-a-Punch machine':'武器强化机','Pack-a-Punch':'武器强化',
 'Mystery Box':'神秘箱','Quick Revive':'快速救援','Jugger-Nog':'厚血饮料','Juggernog':'厚血饮料','Speed Cola':'快手饮料','Stamin-Up':'快跑饮料',
 'Double Tap Root Beer':'双倍火力汽水','Double Tap II':'双倍火力二型','Mule Kick':'骡子踢','Deadshot Daiquiri':'死亡射手','PhD Flopper':'博士爆破','PhD Slider':'博士滑铲',
 'Electric Cherry':'电气樱桃','Widow\'s Wine':'寡妇之酒','Who\'s Who':'谁是谁','Tombstone Soda':'墓碑汽水','Vulture Aid':'秃鹫援助','Death Perception':'死亡感知',
 'GobbleGums':'泡泡糖','GobbleGum':'泡泡糖','Mega GobbleGums':'超级泡泡糖','Perk-a-Cola':'特长饮料','Perk-a-Colas':'特长饮料','Wonder Weapons':'奇迹武器','Wonder Weapon':'奇迹武器',
 'Max Ammo':'弹药全满','Carpenter':'木匠奖励','Insta-Kill':'即死奖励','Double Points':'双倍点数','Fire Sale':'火力拍卖','Bonus Points':'额外点数',
 'Call of Duty: Black Ops III':'使命召唤：黑色行动3','Call of Duty: Black Ops II':'使命召唤：黑色行动2','Call of Duty: Black Ops 4':'使命召唤：黑色行动4','Call of Duty: Black Ops':'使命召唤：黑色行动',
 'Nacht der Untoten':'亡者之夜','Verrückt':'精神病院','Shi No Numa':'死亡沼泽','Der Riese':'巨人工厂','Kino der Toten':'死亡剧院','Call of the Dead':'亡者召唤',
 'Shangri-La':'香格里拉','Ascension':'升天','TranZit':'迁徙','Die Rise':'大厦','Mob of the Dead':'亡者之群','Nuketown Zombies':'核弹镇僵尸',
 'Shadows of Evil':'邪恶之影','The Giant':'巨人','Der Eisendrache':'德尔艾森德拉赫','Zetsubou No Shima':'绝望之岛','Gorod Krovi':'血色城堡',
 'Voyage of Despair':'绝望之旅','Blood of the Dead':'亡者之血','Dead of the Night':'死亡之夜','Ancient Evil':'远古邪恶','Alpha Omega':'阿尔法·欧米伽','Tag der Toten':'亡者之日',
 'Ray Gun Mark II':'射线枪二型','Ray Gun':'射线枪','Wunderwaffe DG-Scharfschütze':'DG狙击型奇迹武器','Wunderwaffe DG-2':'DG-2奇迹武器','Thundergun':'雷霆枪',
 'Winter\'s Howl':'冬日哀嚎','Thrustodyne Aeronautics Model 23':'喷气推进航空器23型','Sliquifier':'液化枪','Paralyzer':'麻痹器','Blundergat':'碎颅者',
 'Acid Gat Kit':'酸液加特改装套件','Acid Gat':'酸液加特','Vitriolic Withering':'酸蚀凋零','Magmagat':'熔岩加特','Hell\'s Retriever':'地狱猎犬斧','Hell\'s Redeemer':'地狱救赎者',
 'Golden Spork':'黄金叉勺','Golden Helmet':'黄金头盔','Golden Shovel':'黄金铲','Bowie Knife':'鲍伊猎刀','Silver Bullets':'银子弹','Stake Knife':'木桩匕首',
 'Elemental Staffs':'元素法杖','Staff of Fire':'火杖','Staff of Ice':'冰杖','Staff of Wind':'风杖','Staff of Lightning':'雷杖','Maxis Drone':'麦克西斯无人机',
 'Apothicon Servant':'阿波西肯仆从','Apothicon Sword':'阿波西肯之剑','Wrath of the Ancients':'远古之怒','Skull of Nan Sapwe':'南萨普维之颅','Gauntlet of Siegfried':'齐格弗里德护手',
 'Guard of Fafnir':'法夫尼尔之盾','Dragon Strike':'飞龙轰击','Dragon Egg':'龙蛋','Ragnarok DG-4':'诸神黄昏DG-4','Zombie Shield':'僵尸盾','Rocket Shield':'火箭盾',
 'Brazen Bull':'铜牛盾','Spectral Shield':'幽灵盾','Ballistic Shield':'防暴盾','Apollo\'s Will':'阿波罗之意志','Death of Orion':'俄里翁之死','Alistair\'s Folly':'阿利斯泰尔的愚行',
 'Alistair\'s Annihilator':'阿利斯泰尔歼灭者','Savage Impaler':'野蛮穿刺者','Pegasus Strike':'飞马轰击','Hand of Charon':'卡戎之手','Hand of Gaia':'盖亚之手',
 'Hand of Hemera':'赫墨拉之手','Hand of Ouranos':'乌拉诺斯之手','Samantha\'s Music Box':'萨曼莎音乐盒','G-Strike':'G轰击信标','Time Bomb':'时间炸弹','Trample Steam':'弹射器',
 'Subsurface Resonator':'地下共振器','Vril Device':'维里尔装置','Focusing Stone':'聚焦石','Navcard':'导航卡','Persistent Upgrades':'持久升级',
 'Edward Richtofen':'爱德华·里希托芬','Richtofen':'里希托芬','Ludvig Maxis':'路德维希·麦克西斯','Maxis':'麦克西斯','Samantha':'萨曼莎',
 'Tank Dempsey':'坦克·邓普西','Dempsey':'邓普西','Nikolai Belinski':'尼古莱·别林斯基','Nikolai':'尼古莱','Takeo Masaki':'正木武雄','Takeo':'武雄',
 'Marlton Johnson':'马尔顿·约翰逊','Marlton':'马尔顿','Samuel Stuhlinger':'塞缪尔·斯图林格','Stuhlinger':'斯图林格','Russman':'拉斯曼','Misty':'米丝蒂',
 'Albert Arlington':'阿尔伯特·阿灵顿','Weasel':'黄鼠狼','Billy Handsome':'比利·汉森','Sal DeLuca':'萨尔·德卢卡','Finn O\'Leary':'芬恩·奥利里',
 'Scarlett Rhodes':'斯嘉丽·罗兹','Diego Necalli':'迭戈·内卡利','Bruno Delacroix':'布鲁诺·德拉克鲁瓦','Stanton Shaw':'斯坦顿·肖','Alistair Rhodes':'阿利斯泰尔·罗兹',
 'Hellhounds':'地狱犬','Hellhound':'地狱犬','Panzersoldats':'装甲僵尸','Panzersoldat':'装甲僵尸','Margwas':'玛格瓦','Margwa':'玛格瓦','Thrashers':'吞噬者','Thrasher':'吞噬者',
 'Apothicons':'阿波西肯','Apothicon':'阿波西肯','Keepers':'守护者','Keeper':'守护者','Apothicon language':'阿波西肯语','Sentinel Artifact':'哨兵神器',
 'players':'玩家','player':'玩家','zombies':'僵尸','zombie':'僵尸'
}
DIRECT = {'Gallery':'图库','Overview':'概述','Trivia':'杂项','References':'参考资料','Contents':'目录','Quotes':'对白','Radios':'无线电录音','Location':'位置','Locations':'位置',
 'Weapon Class':'武器类别','Wonder Weapon':'奇迹武器','Magazine Size':'弹匣容量','Starting Ammunition':'初始弹药','Maximum Ammunition':'最大备弹','Fire Mode':'射击模式',
 'Single-fire':'单发','Semi-automatic':'半自动','Fully-automatic':'全自动','Damage':'伤害','Range':'射程','Rate of Fire':'射速','Reload Time':'换弹时间','Cost':'价格','Points':'点数',
 'Yes':'是','No':'否','None':'无','N/A':'不适用','Infinite':'无限','Infinity':'无限','Infinite Damage':'无限伤害','Unlimited':'无限','Unknown':'未知','Unsolved':'未解开','Cipher':'密文','Plaintext':'明文','Decrypted Text':'解密文本'}
TERM_RE = re.compile(r'(?<![A-Za-z])('+'|'.join(re.escape(k) for k in sorted(GLOSSARY,key=len,reverse=True))+r')(?![A-Za-z])',re.I)
TERM_LOWER={k.lower():v for k,v in GLOSSARY.items()}
MARK_RE=re.compile(r'[\[［]\s*U\s*(\d+)\s*[\]］]',re.I)
RATE_LOCK=threading.Lock();NEXT_CALL=0.0

def read_doc(p):
 s=p.read_text(encoding='utf-8');return json.loads(s[s.index('(')+1:s.rfind(')')])
def digest(s):return hashlib.sha256(s.encode()).hexdigest()
def save_json(p,obj):
 p=pathlib.Path(p);p.parent.mkdir(parents=True,exist_ok=True);tmp=p.with_suffix(p.suffix+'.tmp');tmp.write_text(json.dumps(obj,ensure_ascii=False,separators=(',',':')),encoding='utf-8');tmp.replace(p)
def rate_wait():
 global NEXT_CALL
 with RATE_LOCK:
  t=time.monotonic();wait=max(0,NEXT_CALL-t);NEXT_CALL=max(t,NEXT_CALL)+1.05
 if wait:time.sleep(wait)
def request_translation(text):
 # Public web translation endpoint, not a claim of a paid or reviewed service.
 url='https://translate.googleapis.com/translate_a/single?'+urllib.parse.urlencode({'client':'gtx','sl':'en','tl':'zh-CN','dt':'t','q':text})
 for attempt in range(5):
  rate_wait()
  try:
   req=urllib.request.Request(url,headers={'User-Agent':'Mozilla/5.0'})
   with urllib.request.urlopen(req,timeout=50) as r:data=json.load(r)
   if not isinstance(data,list) or not data or not isinstance(data[0],list):raise ValueError('Unexpected translation response')
   out=''.join(x[0] for x in data[0] if x and isinstance(x[0],str)).strip()
   if not out:raise ValueError('Empty translation')
   return out
  except urllib.error.HTTPError as e:
   if e.code in (400,413,414):raise
   delay=max(int(e.headers.get('Retry-After','0')) if str(e.headers.get('Retry-After','0')).isdigit() else 0,min(120,8*2**attempt))
   print('Translation HTTP',e.code,'retry',attempt+1,'wait',delay,flush=True);time.sleep(delay)
  except Exception:
   if attempt==4:raise
   time.sleep(min(30,4*2**attempt))
 raise RuntimeError('Translation service remained unavailable; cache retained')

def prep(s):return TERM_RE.sub(lambda m:TERM_LOWER[m.group().lower()],s)
def parts(s,limit=2400):
 # Split only for service size limits; all source characters remain in these parts.
 if len(s)<=limit:return [s]
 out=[]
 while len(s)>limit:
  candidates=[m.end() for m in re.finditer(r'(?<=[.!?;\n])\s+',s[:limit])]
  cut=candidates[-1] if candidates else s.rfind(' ',0,limit)
  if cut<=0:cut=limit
  out.append(s[:cut]);s=s[cut:]
 if s:out.append(s)
 return out

def translate_batch(batch):
 # IDs keep distinct source units distinct, including short table cells/captions.
 q='\n'.join('[U%05d] %s'%(i,prep(s)) for i,s in enumerate(batch))
 try:
  out=request_translation(q);marks=list(MARK_RE.finditer(out))
  if [int(m.group(1)) for m in marks]!=list(range(len(batch))):raise ValueError('Source-unit markers changed')
  values=[out[m.end():marks[i+1].start() if i+1<len(marks) else len(out)].strip() for i,m in enumerate(marks)]
  if not all(values):raise ValueError('Empty translated unit')
  return values
 except Exception:
  if len(batch)>1:
   mid=len(batch)//2;return translate_batch(batch[:mid])+translate_batch(batch[mid:])
  s=batch[0];chunks=parts(s)
  if len(chunks)>1:return [' '.join(request_translation(prep(c)) for c in chunks)]
  return [request_translation(prep(s))]

def literal(s):
 if not re.search('[A-Za-z]',s):return True
 # Preserve model codes/numerical data, never silently treat prose as a literal.
 return len(s)<36 and bool(re.fullmatch(r'[A-Z]{1,8}[- ]?\d+[A-Z\d]*(?:[- /][A-Z\d]{1,8})?',s))

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--assets',default='app/src/main/assets/faithful');ap.add_argument('--out',default='draft-output');ap.add_argument('--workers',type=int,default=2);args=ap.parse_args()
 root=pathlib.Path(args.assets);out=pathlib.Path(args.out);out.mkdir(parents=True,exist_ok=True)
 docs=[read_doc(p) for p in sorted(root.glob('p*.js'))];assert len(docs)==182
 assert sum(len(d['units']) for d in docs)==54189
 seed=collections.defaultdict(set)
 for d in docs:
  for u in d['units']:
   if u.get('zh'):seed[u['en']].add(u['zh'])
 memory={s:{'zh':next(iter(v)),'method':'existing-exact-source-translation'} for s,v in seed.items() if len(v)==1}
 for s,t in {**GLOSSARY,**DIRECT}.items():memory.setdefault(s,{'zh':t,'method':'terminology'})
 cache_path=out/'translation-cache.json'
 if cache_path.exists():memory.update(json.loads(cache_path.read_text()))
 wanted=list(dict.fromkeys(u['en'] for d in docs for u in d['units'] if not u.get('zh')))
 for s in wanted:
  if s not in memory and literal(s):memory[s]={'zh':s,'method':'verbatim-code-or-number'}
 todo=[s for s in wanted if s not in memory]
 # Core gameplay/equipment pages precede dialogue archives, without omitting any.
 priority={u['en'] for d in docs if '/Quotes' not in d['metadata']['title'] and '/Transcript' not in d['metadata']['title'] for u in d['units']}
 todo.sort(key=lambda s:0 if s in priority else 1)
 batches=[];batch=[];size=0
 for s in todo:
  cost=len(prep(s))+12
  if batch and (size+cost>3000 or len(batch)>=60):batches.append(batch);batch=[];size=0
  batch.append(s);size+=cost
 if batch:batches.append(batch)
 print('sources',len(docs),'missing distinct strings',len(todo),'batches',len(batches),flush=True)
 failure=[];finished=0
 try:
  with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
   futures={pool.submit(translate_batch,b):b for b in batches}
   for f in concurrent.futures.as_completed(futures):
    b=futures[f]
    try:
     result=f.result();assert len(result)==len(b)
     for s,t in zip(b,result):memory[s]={'zh':t,'method':'google-web-machine-draft','sourceSha256':digest(s)}
    except Exception as e:failure.append({'sources':[digest(s) for s in b],'error':repr(e)})
    finished+=1
    if finished%10==0 or finished==len(batches):
     save_json(cache_path,memory);print('batches',finished,'/',len(batches),'cached',len(memory),'failures',len(failure),flush=True)
 finally:save_json(cache_path,memory)
 manifest=[];flags=[]
 for d in docs:
  if d['translated']:continue
  rows=[];methods=[]
  for u in d['units']:
   m=memory.get(u['en'],{});z=m.get('zh');rows.append(z);methods.append(m.get('method','missing'))
   if z:
    nums=re.findall(r'\d+(?:[.,]\d+)*',u['en']);znums=re.findall(r'\d+(?:[.,]\d+)*',z)
    if collections.Counter(nums)!=collections.Counter(znums):flags.append({'pageid':d['metadata']['pageid'],'unit':u['id'],'type':'numeric-check','en':u['en'],'zh':z})
    if len(u['en'].split())>5 and not re.search('[\u3400-\u9fff]',z):flags.append({'pageid':d['metadata']['pageid'],'unit':u['id'],'type':'non-Chinese-prose-or-code','en':u['en'],'zh':z})
    if len(u['en'])>150 and len(z)<len(u['en'])*0.18:flags.append({'pageid':d['metadata']['pageid'],'unit':u['id'],'type':'short-output','en':u['en'],'zh':z})
  pid=d['metadata']['pageid'];p={'pageid':pid,'revision':d['metadata']['revision'],'sourceUnitDigest':d['sourceUnitDigest'],'translationsInUnitOrder':rows,'methodsInUnitOrder':methods,'status':'machine-draft-unreviewed','source':d['metadata']['fixedUrl'],'sourceSha256':[digest(u['en']) for u in d['units']]}
  save_json(out/'drafts'/f'{pid}.json',p);manifest.append({'pageid':pid,'title':d['metadata']['title'],'units':len(rows),'translated':sum(bool(x) for x in rows),'status':'machine-draft-unreviewed'})
 save_json(out/'draft-manifest.json',{'articles':manifest,'existingReviewedArticles':40,'newDraftArticles':len(manifest),'missingUnits':sum(p['units']-p['translated'] for p in manifest),'reviewFlags':len(flags),'failures':failure,'notFullyReviewed':True})
 save_json(out/'review-flags.json',flags)
 (out/'README.txt').write_text('UNREVIEWED machine drafts for public Call of Duty Wiki fixed-revision source units.\nOriginal source text, unit IDs, tables, media, and prior reviewed translations are unchanged.\nThese drafts MUST NOT be labelled as individually reviewed or gameplay verified.\nArticle text and translations: CC BY-SA 3.0; contributors and fixed URLs are preserved per article.\n')
 assert not failure,failure
 assert all(p['translated']==p['units'] for p in manifest),'Untranslated units remain; no complete-content claim is permitted'
 print('Draft generation complete, review required:',len(manifest),'articles,',len(flags),'automated review flags',flush=True)

if __name__=='__main__':main()
