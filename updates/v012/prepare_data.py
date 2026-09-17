"""Build an offline atlas and a heading-only source index; publisher prose remains online."""
import argparse,hashlib,json,re,shutil
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('--atlas',type=Path,required=True);p.add_argument('--source',type=Path,required=True);p.add_argument('--assets',type=Path,required=True);args=p.parse_args();assets=args.assets
cat=json.loads((args.atlas/'catalog.json').read_text())
select={0:[2],1:[1,2],2:[2],3:[2,3,4],4:[1,2],5:list(range(1,15)),6:[1,2,3],7:[2,3,4],8:[2],9:[4],10:[1],11:list(range(1,8)),12:[3,4],13:[1,2,3],14:[1,2],15:[1,2],16:[1],17:[1],18:[1],19:[1,2],20:[1],21:[1],22:[1],23:[1,2],24:[3,4],25:[1],26:[1,2],27:[1],28:[2,3,4],29:[1],30:[3,4],31:[1],32:[1,2],33:[1,2],34:[1],35:[1],36:[2,3,4],37:[1],38:[1],39:[2],40:[1],41:[2],42:[2],43:[2],44:[1],47:[1],48:[2],55:[1],56:[1],57:[1,2],58:[0,4],59:[0],60:[0],61:[0],62:[1],63:[1],64:[1],65:[1],66:[1],67:[1,2],68:[1,2],69:[1,2],70:[1],71:[1],72:[1],73:[1],74:[1,2,3],75:[1],76:[1],77:[1,2,3],78:[1],79:[1,2],80:[1],81:[1],82:[1],83:[1],84:[1],85:[1],86:[1],87:[1],88:[2]}
area={0:'竞技场与四座神塔',1:'监狱全区',2:'办公室／作战室／实验室',3:'庄园分层',4:'各地图区域连接',5:'坦克工厂／医务室／补给站／地下室／龙指挥部',6:'军械库分层',7:'百货商店分层',8:'别林斯基广场（出生区）',9:'码头',10:'掩体高射炮区',11:'地下掩体分区',12:'B实验室沼泽',13:'B实验室分层',14:'B实验室外围',15:'A实验室分层',16:'A实验室沼泽',17:'A实验室外围',18:'出生区',19:'火箭试验平台',20:'传送器房间',21:'地下金字塔大厅',22:'家族墓室',23:'任务控制室分层',24:'军械库／电源房',25:'生活区',26:'上层庭院',27:'奖杯室',28:'下层庭院',29:'城堡门外',30:'出生区／缆车站',31:'灯光区上层街道',32:'裂隙地下区',33:'灯光区主街',34:'运河区上层街道',35:'红兔夜总会分层',36:'运河区分层',37:'滨水区上层街道',38:'滨水区后半段',39:'铁砧拳击馆',40:'滨水区入口',41:'灯光区入口',42:'尼禄的房间',43:'路口',44:'出生小巷',47:'寺庙／矿洞／瀑布',48:'灯塔／船体／岸边',55:'工坊分层',56:'坦克站分层',57:'实验室至坦克站／工坊的战壕',58:'全图与出生实验室',59:'二层矿道续段',60:'谷仓分层',61:'全镇街道与建筑关系',62:'女巫宅邸通路',63:'教堂分层',64:'枪械店分层',65:'糖果店分层',66:'银行分层',67:'警长办公室／监狱及相邻房间',68:'酒馆分层（作者称Casino）',69:'杂货店分层',70:'法院分层',71:'地下二层矿道',72:'地表出生区',73:'码头',74:'医务室／缆车通道',75:'屋顶',76:'淋浴间',77:'城堡隧道分区',78:'食堂',79:'密歇根大道／典狱长办公室',80:'牢区第二层',81:'D区牢房（出生区）',82:'弹射器工作台房',83:'屋顶下一层',84:'屋顶／铁塔',85:'第二栋楼电源层',86:'第三层',87:'第二层',88:'第一层出生区'}
notes={61:'先看这张全镇建筑关系图。右下蓝色 Casino/Bar 是酒馆；左下红色是枪械店；上方是教堂、女巫宅邸和花园迷宫。地图表达建筑连接，并非精确比例或当前视角。',68:'作者把酒馆称作 Casino（赌场）。分层图把底层与上层分开画，卫星天线盘在上层阳台，不是在底层柜台。',64:'枪械店底层的电线卷靠角落；底层有通向银行的地道，上层与矿道相连。先用平面图认入口，再看零件近景。',70:'法院可从主街正门进入，也有矿道通向楼上阳台。分清底层法庭和楼上；法院外绞刑架与酒馆旁断头台不同。',60:'天线在谷仓底层，靠右侧深处的隔间。按图中楼梯与落口核对楼层。',63:'麦克西斯路线用的电池在教堂底层讲台后方；教堂左边墓地另有任务球。',65:'图中糖果店上下层分开。电源开关在上层；铃铛阶段的三只铃也在上层。',66:'银行底层地道通向枪械店，先辨认建筑连接，再查看本层点位。',67:'警长办公室、监狱和相邻建筑有楼上跳入及落口。牢门正面并不能到达所有楼上零件。',59:'这是矿道续段，不是地表主街。找到 Lunger Undermines 一带，再对照球或水晶近景。',71:'这是地下二层矿道图，入口和通往建筑的连接分别标注，不要把洞内方向直接当成地表左右。',62:'女巫宅邸后面通向花园迷宫；此图先显示宅邸通路。迷宫会变换，开关另看主线的迷宫变体图。',72:'地表出生区与地下小镇不同层。沿矿道落口下去后，切换全镇图和建筑分层图。',58:'原作社区地图：先认出生实验室、战壕、发电机编号和中央挖掘场。',1:'先分清新工业区、牢区、码头与典狱长区域。这是亡者之血，不是 COD9 监狱。',2:'办公室／会议室、作战室、实验室分属不同层，电梯连接楼层；先确认楼层再找物品。'}
plans={};selected=[]
for di,indices in select.items():
 d=cat['articles'][di]
 for j,ii in enumerate(indices):
  im=d['images'][ii];meta=cat['media'][im['url']];src=args.atlas/meta['file'];raw=src.read_bytes()
  if hashlib.sha256(raw).hexdigest()!=meta['sha256']:raise ValueError('Atlas integrity failure')
  dest='atlas/'+Path(meta['file']).name;(assets/dest).parent.mkdir(exist_ok=True,parents=True);shutil.copyfile(src,assets/dest)
  title=area[di]+(f' · 图{j+1}' if len(indices)>1 else '')
  x={'id':f'plan-{di}-{ii}','map':d['key'],'file':dest,'title':title,'caption':title,'last_heading':'社区地图','isPlan':True,'index':len(plans.get(d['key'],[])),'doc':di,'imageIndex':ii,'note':notes.get(di,'按原图房间标签、楼梯和区域连接寻找入口。图片中的朝向不等于你当前视角；不是实时坐标导航。'),'sourceUrl':d['sourceUrl'],'imageUrl':im['url'],'width':meta['width'],'height':meta['height'],'sha256':meta['sha256'],'originalTitle':d['title'],'date':d['date'][:10]}
  plans.setdefault(d['key'],[]).append(x);selected.append(x)
for lst in plans.values():lst.sort(key=lambda x:(0 if any(s in x['title'] for s in ['全镇','全图','全区']) else 1,x['doc'],x['imageIndex']))
for new,old in {'bo3_origins':'bo2_origins','bo3_shang':'bo1_shang'}.items():plans[new]=[dict(x,note='原作社区地图，仅作区域与楼层对照。复刻版的任务和道具条件以本作品为准。 '+x['note']) for x in plans[old]]
routes={'bo2_buried':[
 {'indices':[0],'planDocs':[61,65,68],'text':'总览右侧糖果店与右下酒馆之间的通路；球不在店内。'},
 {'indices':[1],'planDocs':[61,63],'text':'先到主街尽头教堂，再去教堂左侧墓地区，不是讲台后电池的位置。'},
 {'indices':[2,6],'planDocs':[61,71,59],'text':'先进入地下矿道，对照 Lunger Undermines 一带；不是在地表主街上找。'},
 {'indices':[3],'planDocs':[61,62],'text':'经过女巫宅邸到后方花园一侧，先用宅邸通路图判断前后。'},
 {'indices':[4],'planDocs':[61,68],'text':'总览右下方蓝色 Casino/Bar 就是酒馆。进入建筑上楼，再找上层阳台；下方酒馆分层图可核对楼梯和阳台。'},
 {'indices':[5,15],'planDocs':[61,64],'text':'总览左下红色 Gunsmith Shop 是枪械店。进入底层找电线卷角落，本层有通向银行的地道，不是在楼上矿道。'},
 {'indices':[7,17],'planDocs':[61,60],'text':'按总览找到谷仓，进入底层马厩，到右侧深处隔间找天线。'},
 {'indices':[9,19],'planDocs':[61,64],'text':'这是枪械店屋顶放灯符号，不是地面工作台；先认建筑，再到屋顶。'},
 {'indices':[13],'planDocs':[61,62],'text':'从女巫宅邸后方进花园迷宫，先辨认当前变体，再找四色开关；图片不提供本局固定答案。'},
 {'indices':[14],'planDocs':[61,63],'text':'电池在教堂底层讲台后面，不是楼上或外侧墓地。'},
 {'indices':[16],'planDocs':[61,67],'text':'警长办公室牢房上方，按监狱及相邻房间的分层图找楼上连接和落口。'},
 {'indices':[22],'planDocs':[61,62],'text':'经过女巫宅邸暗门书架，在后面房间沙发上找九灯面板；另三人分别去糖果店上层、谷仓上层、法院底层。'},
 {'indices':[23,24],'planDocs':[61],'text':'教堂与女巫宅邸外的喷水池是最终靶场启动点，不是迷宫尽头强化机。'}],
 'classified':[{'match':'Filing','planDocs':[2],'text':'中央档案室在开局办公室所在层，不是地下实验室。'},{'match':'War Room','planDocs':[2],'text':'办公室乘电梯到作战室后，还要分清上方环廊和中央下层。'},{'match':'Labs|Laborator','planDocs':[2],'text':'从作战室乘另一段电梯到实验室层。南／北实验室是这一层的分区。'}]}
patterns={'bo3_de':[('Rocket',[19]),('Teleporter',[20]),('Undercroft|Pyramid',[21]),('Tomb',[22]),('Church|Control',[23]),('Armory|Power',[24]),('Trophy',[27]),('Courtyard|Clock|Death Ray',[26,28]),('Spawn|Cable',[30])],'bo3_shadows':[('Canal',[34,36]),('Waterfront',[37,38,40]),('Footlight',[31,33,41]),('Rift',[32]),('Nero',[42]),('Junction',[43]),('Spawn',[44]),('Pink|Rabbit',[35]),('Boxing',[39])],'bo3_zets':[('Lab A|Laboratory A',[15,17]),('Lab B|Laboratory B',[13,14]),('Dock',[9]),('Bunker',[11]),('Spawn',[18])],'bo2_mob':[('Docks?|M1927|Tommy',[73]),('Infirmary',[74]),('Roof',[75]),('Shower',[76]),('Citadel|Spiral|Number Pad',[77]),('Cafeteria',[78]),('Warden|Michigan',[79]),('Broadway|Second Floor',[80]),('D-Block',[81])],'bo2_origins':[('Generator 2|Gen 2|Tank Station',[56]),('Spawn|Laboratory',[58]),('Workshop',[55])],'bo2_dierise':[('Roof|Tower',[84]),('Power',[85])]}
for k,rs in patterns.items():routes[k]=[{'match':m,'planDocs':ds,'text':'先用下方社区区域图辨认这一分区，再按近景和房间／楼层名称找交互点。两张图朝向不同时，用门、楼梯和相邻区域的标签对照。'} for m,ds in rs]
routes['bo3_origins']=routes['bo2_origins'];links={}
for i in [46,49,50,51,52,53,54]:
 d=cat['articles'][i];k={'bo1_der_riese':'bo1_der'}.get(d['key'],d['key']);links.setdefault(k,[]).append({'title':'社区地图／PDF指南原页（未离线收录）','url':d['sourceUrl']})
(assets/'navigation.js').write_text('window.NAVIGATION='+json.dumps({'plans':plans,'routes':routes,'links':links,'uniquePlans':len(selected)},ensure_ascii=False,separators=(',',':'))+';\n')
sourcecat=json.loads((args.source/'catalog.json').read_text());guides={}
for d in sourcecat['guides']:
 raw=(args.source/'articles'/d['filename']).read_bytes()
 if hashlib.sha256(raw).hexdigest()!=d['sha256']:raise ValueError('Article hash mismatch')
 text=raw.decode();lines=text.splitlines();matches=list(re.finditer(r'^(#{2,5})\s+(.+)$',text,re.M));sections=[];stack=[];duplicates={}
 for i,m in enumerate(matches):
  heading=re.sub(r'[*`]+','',m.group(2)).strip();level=len(m.group(1));start=text.count('\n',0,m.start())+1;end=text.count('\n',0,matches[i+1].start()) if i+1<len(matches) else len(lines)
  anchor=re.sub(r'[^\w\s-]','',heading.lower());anchor=re.sub(r'\s+','-',anchor);n=duplicates.get(anchor,0);duplicates[anchor]=n+1
  if n:anchor+='-'+str(n)
  while stack and stack[-1]['level']>=level:stack.pop()
  sec={'id':d['key']+'-'+str(i),'heading':heading,'anchor':anchor,'level':level,'parent':stack[-1]['id'] if stack else None,'startLine':start,'endLine':end,'images':[x['index'] for x in d['images'] if start<=x['line']<=end]};sections.append(sec);stack.append(sec)
 included=[i for s in sections for i in s['images']]
 if sorted(included)!=list(range(len(d['images']))):raise ValueError('Image-to-heading coverage mismatch')
 guides[d['key']]={'guide':d['key'],'filename':d['filename'],'sha256':d['sha256'],'sections':sections,'imageReferences':len(included)}
urls={'casimir-mechanism':(1,'ascension'),'ensemble-cast':(1,'call-of-the-dead'),'time-travel-will-tell':(1,'shangri-la'),'richtofens-grand-scheme':(1,'moon'),'tower-of-babble':(2,'tranzit'),'high-maintenance':(2,'die-rise'),'pop-goes-the-weasel':(2,'mob-of-the-dead'),'mined-games':(2,'buried'),'little-lost-girl':(2,'origins'),'apocalypse-averted':(3,'shadows-of-evil'),'my-brothers-keeper':(3,'der-eisendrache'),'seeds-of-doubt':(3,'zetsubou-no-shima'),'love-and-war':(3,'gorod-krovi'),'for-the-good-of-all':(3,'revelations'),'venerated-warrior':(4,'ix'),'abandon-ship':(4,'voyage-of-despair'),'most-escape-alive':(4,'blood-of-the-dead'),'classified':(4,'classified'),'trial-by-ordeal':(4,'dead-of-the-night'),'greek-tragedy':(4,'ancient-evil'),'electromagnetic-awakening-party':(4,'alpha-omega'),'salvation-lies-above':(4,'tag-der-toten')}
media=json.loads((assets/'media.js').read_text().split('=',1)[1].strip().rstrip(';'));maps={}
for k,s in media['maps'].items():
 g=s['guide'];n,slug=urls[g];maps[k]=dict(guides[g],url=f'https://www.codzombiesguides.com/main-quests/black-ops-{n}/{slug}/')
index={'maps':maps,'guides':guides,'sourceCommit':sourcecat['source_commit']};(assets/'source-index.js').write_text('window.SOURCE_INDEX='+json.dumps(index,ensure_ascii=False,separators=(',',':'))+';\n')
audit={'sourceCommit':sourcecat['source_commit'],'guides':len(guides),'headings':sum(len(g['sections']) for g in guides.values()),'sourceImageReferences':sum(g['imageReferences'] for g in guides.values()),'originalCommunityPlans':len(selected),'atlasMapEntries':sorted(plans),'coverage':'All source headings and image references, not a verbatim or complete offline translation of article prose. Complete publisher pages require network access.'};(assets/'navigation-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(json.dumps(audit,ensure_ascii=False))
