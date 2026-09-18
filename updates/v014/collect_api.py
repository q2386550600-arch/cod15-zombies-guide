"""Full MediaWiki parse snapshots through the wiki's public API.
HTML page delivery rejects the runner; the site's public parse API works.
"""
import hashlib,json,time,re,runpy
from pathlib import Path
from urllib.parse import quote,urljoin
import requests
from bs4 import BeautifulSoup
OUT=Path('source-archive');OUT.mkdir(exist_ok=True)
BASE='https://callofduty.fandom.com';API=BASE+'/api.php'
TITLES=['Cold War Remedy','Mined Games','Ensemble Cast','Casimir Mechanism','Time Travel Will Tell',"Richtofen's Grand Scheme",'Tower of Babble','High Maintenance','Pop Goes the Weasel','Little Lost Girl','Apocalypse Averted',"My Brother's Keeper",'Seeds of Doubt','Love and War','For The Good Of All','Fly Trap','Venerated Warrior','Abandon Ship','Most Escape Alive','Trial by Ordeal','Greek Tragedy','Electromagnetic Awakening Party','Salvation Lies Above','Golden Spork',"Hell's Retriever",'Elemental Staffs/Staff of Ice','Elemental Staffs','G-Strike','Hand of Charon','Golden Helmet','Easter Eggs','Origins','Mob of the Dead','The Giant','Dead of the Night','Stand-in','Elemental Staffs/Staff of Fire','Elemental Staffs/Staff of Wind','Elemental Staffs/Staff of Lightning','Hand of Hemera','Hand of Ouranos','Hand of Gaia','Golden Shovel','Guillotine','Gallows','Icarus','Maxis Drone','Savage Impaler','Stake Knife',"Alistair's Folly",'KT-4','Masamune','Wrath of the Ancients',"Kreema'ahm la Ahmahm","Kreeaho'ahm nal Ahmhogaroc","Kreegakaleet lu Gosata'ahm",'Kreeholo lu Kreemasaleet',
'Nacht der Untoten','Verrückt','Shi No Numa','Der Riese','Kino der Toten','Five','Ascension','Call of the Dead','Shangri-La','Moon','Bus Depot','Farm','Town','Nuketown Zombies','TranZit','Die Rise','Buried','Shadows of Evil','Der Eisendrache','Zetsubou No Shima','Gorod Krovi','Revelations','IX','Voyage of Despair','Blood of the Dead','Classified','Ancient Evil','Alpha Omega','Tag der Toten',
'Thundergun','Wunderwaffe DG-2',"Winter's Howl",'Sliquifier','Paralyzer','Thrustodyne Aeronautics Model 23','Trample Steam','Navcard','Turbine','Subsurface Resonator','Time Bomb','Blundergat','Acid Gat Kit','Magmagat','Spectral Shield','Zombie Shield','Dragon Shield','Dragon Strike','Gauntlet of Siegfried',"Apothicon Servant","Apothicon Sword",'Ragnarok DG-4','Skull of Nan Sapwe','Gas Mask','KT-4/Masamune','Brazen Bull','Death of Orion','Kraken',"Alistair's Annihilator",'Ballistic Shield','Pegasus Strike','Apollo\'s Will','Ray Gun Mark II','Wunderwaffe DG-Scharfschütze','Samantha\'s Music Box','Silver Bullets','Golden Rod','Focusing Stone']
TITLES=list(dict.fromkeys(TITLES));HEAD={'User-Agent':'CodGuideSourceReview/0.14 (attribution-preserving public wiki research)'}
def get(params):
 r=requests.get(API,params=params,headers=HEAD,timeout=(8,28));r.raise_for_status();j=r.json()
 if 'error' in j:raise ValueError(j['error'])
 return j,r
try:
 lic,_=get({'action':'query','meta':'siteinfo','siprop':'rightsinfo','format':'json'});(OUT/'license-siteinfo.json').write_text(json.dumps(lic,ensure_ascii=False,indent=2))
except Exception as exc:(OUT/'license-fetch-error.txt').write_text(repr(exc))
results=[]
for title in TITLES:
 rec={'requestedTitle':title,'title':title,'url':BASE+'/wiki/'+quote(title.replace(' ','_'),safe='/'),'fetched':False,'errors':[]}
 try:
  j,r=get({'action':'parse','page':title,'prop':'text|wikitext|revid|links|images|externallinks|sections|categories|displaytitle','redirects':1,'format':'json'})
  p=j['parse'];safe=str(p['pageid'])+'-'+str(p['revid']);html=p['text']['*'];root=BeautifulSoup(html,'html.parser').select_one('.mw-parser-output')
  if root is None or len(root.get_text(' ',strip=True))<70:raise ValueError('Missing or empty article body')
  rec.update({'fetched':True,'title':p['title'],'pageid':p['pageid'],'revision':p['revid'],'file':safe+'.json','articleFile':safe+'.html','wikitextFile':safe+'.wiki','sha256':hashlib.sha256(r.content).hexdigest(),'textLength':len(root.get_text(' ',strip=True)),'historyUrl':BASE+'/wiki/'+quote(p['title'].replace(' ','_'),safe='/')+'?action=history','fixedUrl':BASE+'/wiki/'+quote(p['title'].replace(' ','_'),safe='/')+'?oldid='+str(p['revid']), 'sections':p.get('sections',[]),'images':p.get('images',[]),'externalLinks':p.get('externallinks',[]),'links':p.get('links',[])})
  (OUT/rec['file']).write_bytes(r.content);(OUT/rec['articleFile']).write_text(html);(OUT/rec['wikitextFile']).write_text(p.get('wikitext',{}).get('*',''))
 except Exception as exc:rec['errors'].append(repr(exc))
 results.append(rec);print(len(results),title,rec['fetched'],rec.get('textLength'),rec['errors'],flush=True);time.sleep(.25)
# Probe an ordinary public translation request. No credentials or user data sent.
try:
 sample='The photograph is hidden behind the monitor. Do not shoot the monitor. Go to the upper floor of the Saloon.'
 r=requests.get('https://translate.googleapis.com/translate_a/single',params={'client':'gtx','sl':'en','tl':'zh-CN','dt':'t','q':sample},timeout=20);r.raise_for_status();(OUT/'translation-probe.json').write_text(json.dumps({'source':sample,'response':r.json()},ensure_ascii=False,indent=2));print('Translation endpoint available',flush=True)
except Exception as exc:(OUT/'translation-probe-error.txt').write_text(repr(exc))
(OUT/'catalog.json').write_text(json.dumps({'source':'Call of Duty Wiki contributors / Fandom','requested':len(TITLES),'fetched':sum(x['fetched'] for x in results),'pages':results,'method':'Full public MediaWiki parse response including source wikitext and fixed revision; all article sections retained'},ensure_ascii=False,indent=2))
