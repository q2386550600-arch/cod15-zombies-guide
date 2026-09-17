#!/usr/bin/env python3
"""Build an offline, traceable image index from the original author's source pack."""
from pathlib import Path
import argparse, hashlib, json, re, shutil

SPECS = {
 'bo1_ascension': ('casimir-mechanism',[['Power Generator'],['Buttons'],['Clock'],['Letter'],['Final Step']]),
 'bo1_cotd': ('ensemble-cast',[['Fuse'],['Generator'],['Vodka'],['Radios'],['Lever'],['Foghorn'],['Dial'],['Golden Rod'],['Final Step']]),
 'bo1_shang': ('time-travel-will-tell',[['Triggering'],['Tiles'],['Water Slide'],['Crystal'],['Gas'],['Holes'],['Panels'],['Wheel'],['Gong'],['Final Step'],['Repeating']]),
 'bo1_moon': ('richtofens-grand-scheme',[['Simon says'],['Hacking'],['Obtaining the Vril sphere'],['Opening the M.P.D.'],['Powering the Vril Device'],['Powering the Vril Device'],['Switching souls'],["Maxis' Revenge"],["Maxis' Revenge"],["Maxis' Revenge"]]),
 'bo2_tranzit': ('tower-of-babble',[['Requirements'],['Maxis Side','Richtofen Side'],['Maxis Side','Richtofen Side'],['Maxis Side','Final Step (Maxis'],['Richtofen Side'],['Richtofen Side'],['Final Step (Richtofen']]),
 'bo2_dierise': ('high-maintenance',[['Elevator Symbols'],['Floor Symbols'],['Sniper'],['Maxis Side'],['Maxis Side'],['Maxis Side'],['Richtofen Side'],['Richtofen Side'],['Final Step'],['Final Step']]),
 'bo2_mob': ('pop-goes-the-weasel',[['Building the Plane'],['Building the Plane'],['Flying and Refueling'],['Acquiring the Skulls'],['Acquiring the Spoons'],['Final Step'],['Final Step'],['Final Step'],['Final Step']]),
 'bo2_buried': ('mined-games',[['Powering the Orbs'],['Richtofen Side','Maxis Side'],['Richtofen Side','Maxis Side'],['Richtofen Side','Maxis Side'],['Richtofen Side'],['Richtofen Side'],['Maxis Side'],['Final Step'],['Final Step']]),
 'bo2_origins': ('little-lost-girl',[['Step 1'],['Step 1'],['Step 2'],['Step 3'],['Step 4'],['Step 5'],['Step 6'],['Step 7'],['Step 8']]),
 'bo3_shadows': ('apocalypse-averted',[['Step 1'],['Step 1'],['Step 1'],['Step 2'],['Step 2'],['Step 3'],['Step 4'],['Step 4'],['Step 5'],['Step 6']]),
 'bo3_de': ('my-brothers-keeper',[['Step 1'],['Step 2'],['Step 2'],['Step 3'],['Step 3'],['Step 4'],['Step 5'],['Step 6'],['Step 7'],['Step 7'],['Step 8']]),
 'bo3_zets': ('seeds-of-doubt',[['Step 1'],['Step 1'],['Step 1'],['Step 1'],['Step 2'],['Step 2'],['Step 2'],['Step 3'],['Step 4']]),
 'bo3_gorod': ('love-and-war',[['Step 1'],['Step 1'],['Step 1'],['Step 2'],['Step 3'],['Step 4'],['Step 4'],['Step 4'],['Step 5'],['Step 5'],['Step 5'],['Step 5'],['Step 6'],['Step 7'],['Step 7']]),
 'bo3_rev': ('for-the-good-of-all',[['Requirements'],['Step 1'],['Step 2'],['Step 2'],['Step 2'],['Step 3'],['Step 4'],['Step 5'],['Step 6'],['Step 7','Step 8'],['Step 9']]),
 'ix': ('venerated-warrior',[['Step 1'],['Step 2'],['Step 2'],['Step 3'],['Step 3'],['Step 4'],['Step 4'],['Step 5'],['Step 5'],['Step 6']]),
 'voyage': ('abandon-ship',[['Step 1'],['Step 2'],['Step 3'],['Step 3'],['Step 4'],['Step 4'],['Step 5'],['Step 6'],['Step 7'],['Step 8'],['Step 9']]),
 'blood': ('most-escape-alive',[['Step: 1'],['Step 2'],['Step 2'],['Step 2'],['Step 3'],['Step 3'],['Step 4'],['Step 4'],['Step 6'],['Step 6'],['Step 7']]),
 'classified': ('classified',[['Main Quest'],['Obtaining the Shield'],['Obtaining the Shield','Main Quest Strategy'],['Main Quest Strategy']]),
 'dead': ('trial-by-ordeal',[['Step 1'],['Step 2'],['Step 2'],['Step 3'],['Step 3'],['Step 3'],['Step 3'],['Step 3'],['Step 3'],['Step 3'],['Step 4']]),
 'ancient': ('greek-tragedy',[['Step 1'],['Step 1'],['Step 2'],['Step 2'],['Step 3'],['Step 4'],['Step 4'],['Step 6'],['Step 5'],['Step 6'],['Step 7']]),
 'alpha': ('electromagnetic-awakening-party',[['Step 1'],['Step 1'],['Step 2'],['Step 2'],['Step 2'],['Step 2'],['Step 2'],['Step 3'],['Step 4'],['Step 4'],['Step 5'],['Step 5'],['Step 6'],['Step 7'],['Step 7'],['Step 8']]),
 'tag': ('salvation-lies-above',[['Step 1'],['Step 1'],['Step 1'],['Step 2'],['Step 3'],['Step 3'],['Step 4'],['Step 4'],['Step 5'],['Step 5'],['Step 6'],['Step 6'],['Step 7'],['Step 8'],['Step 9'],['Step 10']]),
}
for suffix,base in [('ascension','bo1_ascension'),('shang','bo1_shang'),('moon','bo1_moon'),('origins','bo2_origins')]:
 SPECS['bo3_'+suffix]=SPECS[base]

# Captions remain verbatim; translated place names are additional navigation aids,
# never fabricated arrows, coordinates, or altered original screenshots.
PLACES={
 'Lighthouse Level 4':'灯塔四层','Lighthouse Level 3':'灯塔三层','Lighthouse Level 2':'灯塔二层','Lighthouse Level 1':'灯塔一层',
 'Lighthouse Station':'灯塔站','Lighthouse Approach':'灯塔入口通道','Lighthouse Cove':'灯塔湾','Human Infusion':'人体输注室',
 'Artifact Storage':'神器储藏室','Specimen Storage':'标本储藏室','Geological Processing':'地质加工区','Decontamination':'净化室',
 'Security Lobby':'安检大厅','Frozen Crevasse':'冰冻裂隙','Sunken Path':'沉没小路','Hidden Path':'隐藏小路','Outer Walkway':'外侧步道',
 'Boathouse':'船屋','Ice Grotto':'冰洞','Docks':'码头','Dock':'码头','Forecastle':'船首楼','Stern':'船尾','Main Deck':'主甲板','Sun Deck':'日光甲板','Gangway':'舷梯','Lagoon':'泻湖','Beach':'海滩',
 'Power House':'发电站','Generators':'地下发电机室','Operations':'作战室','Prisoner Holding':'囚犯拘留区','Transfusion Facility':'输血设施',
 'APD Interrogation':'APD 审讯室','APD Control':'APD 控制室','Yellow House Upstairs':'黄房二楼','Green House Upstairs':'绿房二楼',
 'Yellow House':'黄房','Green House':'绿房','Solitary':'单独囚禁区','Storage':'储藏室','Lounge':'休息室','Diner':'餐厅','Beds':'卧室区','Bunker':'地下掩体',
 'Central Filing Room':'中央档案室','War Room':'作战室','Weapon Testing':'武器测试室','Labs':'实验室区','Server Room':'主机室',
 "Warden's Office":'典狱长办公室',"Warden's House":'典狱长之家',"Richtofen's Laboratory":'里希托芬实验室',
 'New Industries':'新工业区','Model Industries':'模型工厂','Power Station':'发电站','Citadel Tunnels':'城堡隧道','Showers':'淋浴间',
 'Cafeteria':'食堂','D-Block':'D 区牢房','Michigan Avenue':'密歇根大道','Cell Block':'牢区','Eagle Plaza':'鹰广场','Roof':'屋顶',
 'Poop Deck':'艉楼甲板','Turbine Room':'涡轮机室','Lower Grand Staircase':'大楼梯下层','Upper Grand Staircase':'大楼梯上层','Cargo Hold':'货舱',
 'Bridge':'舰桥','Mail Room':'邮件室','1st Class Lounge':'头等舱休息室','Galley':'厨房','3rd Class Berths':'三等舱卧铺','Engine Room':'引擎室',
 'Wine Cellar':'酒窖','Grand Staircase':'主楼梯','Main Hall':'主大厅','Library':'图书馆','Study':'书房','Dining Room':'餐厅','Master Bedroom':'主卧',
 'Trophy Room':'奖杯室','Billiards Room':'台球室','Smoking Room':'吸烟室','Music Room':'音乐室','East Gallery':'东画廊','West Gallery':'西画廊',
 'Mausoleum':'陵墓','Cemetery':'墓地','Forest':'森林','Gardens':'花园','Greenhouse':'温室','North Atrium':'北中庭','Entrance Hall':'入口大厅',
 'Amphitheater':'圆形剧场','Spartan Monument':'斯巴达纪念碑','River of Sorrow':'悲伤之河','Center of the World':'世界中心','Marketplace':'市场','Underworld':'冥界',
 'Ra Altar Room':'拉塔祭坛室','Danu Arboretum':'丹努树木园','Zeus Bath House':'宙斯浴室','Odin Altar Room':'奥丁祭坛室','Flooded Crypt':'淹水地穴','The Pit':'深坑','Temple':'神殿','Arena':'竞技场',
 'Excavation Site':'挖掘场','Church':'教堂','Crazy Place':'疯狂之地','Tank Station':'坦克站','Wind Tunnel':'风洞','Fire Tunnel':'火洞','Ice Tunnel':'冰洞','Lightning Tunnel':'雷洞',
 'Rocket Test':'火箭测试区','Undercroft':'地下墓室','Bell Tower':'钟楼','Clock Tower':'钟楼','Courtyard':'庭院','Bastion':'堡垒','Death Ray':'死亡射线平台',
 'Spawn':'出生区','Waterfront':'滨水区','Footlight':'灯光区','Canals':'运河区','Junction':'路口','Rift':'裂隙地下室','Buddha Room':'佛像大厅','Roof Top':'屋顶',
 'Biodome':'生态穹顶','Receiving Bay':'接收站','Laboratory':'实验室','MPD Room':'MPD 主机室','Simon Says':'西蒙记忆装置','Tunnel 6':'六号隧道','Tunnel 11':'十一号隧道',
 'Juggernog':'厚血饮料机','Speed Cola':'快手饮料机','Stamin-Up':'快跑饮料机','Quick Revive':'快速救援饮料机','PhD Flopper':'防爆饮料机',
}

def clean_heading(s):return re.sub(r'[*`#]','',s).strip()
def main_heading(text,offset):
 heads=list(re.finditer(r'^(#{2,3})\s+(.+)$',text[:offset],re.M));current='';
 for h in heads:
  title=clean_heading(h.group(2))
  if len(h.group(1))==2 or re.match(r'Step\s*\d',title,re.I):current=title
 return current

def main():
 a=argparse.ArgumentParser();a.add_argument('--source',type=Path,required=True);a.add_argument('--media',type=Path,required=True);a.add_argument('--assets',type=Path,required=True);args=a.parse_args()
 catalog=json.loads((args.source/'catalog.json').read_text());out=args.assets;out.mkdir(exist_ok=True,parents=True)
 refs=[];guides={};failures=[];used=set()
 for doc in catalog['guides']:
  text=(args.source/'articles'/doc['filename']).read_text()
  if hashlib.sha256(text.encode()).hexdigest()!=doc['sha256']:raise ValueError('Article hash mismatch: '+doc['key'])
  entries=[]
  for img in doc['images']:
   meta=catalog['media'][img['source_path']];src=args.media/meta['file']
   if not src.is_file() or hashlib.sha256(src.read_bytes()).hexdigest()!=meta.get('sha256'):failures.append(img['source_path']);continue
   dest=out/meta['file'];dest.parent.mkdir(exist_ok=True,parents=True)
   if meta['file'] not in used:shutil.copyfile(src,dest);used.add(meta['file'])
   entry={k:img[k] for k in ['file','caption','source_path','line','last_heading','index']};entry['chapter']=main_heading(text,img['offset']);entry['width']=meta['width'];entry['height']=meta['height'];entry['places']=[zh+' / '+en for en,zh in PLACES.items() if en.lower() in img['caption'].lower()];entries.append(entry)
  guides[doc['key']]={'images':entries,'sourceFile':doc['filename']}
  refs.append({'guide':doc['key'],'expected':len(doc['images']),'included':len(entries),'sha256':doc['sha256']})
 if failures:raise ValueError('Missing or corrupt images: '+str(failures))
 index={'source':'COD Zombies Guides / PlagueFPS','commit':catalog['source_commit'],'guides':guides,'maps':{k:{'guide':v[0],'chapters':v[1]} for k,v in SPECS.items()},'uniqueImages':len(used),'references':sum(x['included'] for x in refs),'placeNames':PLACES}
 (out/'media.js').write_text('window.COMMUNITY_MEDIA='+json.dumps(index,ensure_ascii=False,separators=(',',':'))+';\n')
 audit={'sourceCommit':catalog['source_commit'],'uniqueImages':len(used),'imageReferences':sum(x['included'] for x in refs),'failed':failures,'documents':refs,'scope':'22 original main-quest articles. Remaster variants can share author screenshots. All image references included; no claim of complete worldwide community coverage or in-game testing.'}
 (out/'media-audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2));print(json.dumps(audit,ensure_ascii=False))

if __name__=='__main__':main()
