"""Fetch full publicly licensed wiki articles; never treat a search excerpt as a page.

Archive source HTML and metadata, plus structured article nodes. No summary or
mandatory/optional filter is applied to article prose. Refusals are recorded.
"""
import hashlib,json,time,re,concurrent.futures
from pathlib import Path
from urllib.parse import quote,urljoin
import requests
from bs4 import BeautifulSoup
OUT=Path('source-archive');OUT.mkdir(exist_ok=True)
TITLES=['Cold War Remedy','Mined Games','Ensemble Cast','Casimir Mechanism','Time Travel Will Tell',"Richtofen's Grand Scheme",'Tower of Babble','High Maintenance','Pop Goes the Weasel','Little Lost Girl','Apocalypse Averted',"My Brother's Keeper",'Seeds of Doubt','Love and War','For The Good Of All','Fly Trap','Venerated Warrior','Abandon Ship','Most Escape Alive','Trial by Ordeal','Greek Tragedy','Electromagnetic Awakening Party','Salvation Lies Above','Golden Spork',"Hell's Retriever",'Elemental Staffs/Staff of Ice','Elemental Staffs','G-Strike','Hand of Charon','Golden Helmet','Easter Eggs','Origins','Mob of the Dead','The Giant','Dead of the Night','Stand-in','Elemental Staffs/Staff of Fire','Elemental Staffs/Staff of Wind','Elemental Staffs/Staff of Lightning','Hand of Hemera','Hand of Ouranos','Hand of Gaia','Golden Shovel','Guillotine','Gallows','Icarus','Maxis Drone','Savage Impaler','Stake Knife','Alistair\'s Folly','KT-4','Masamune','Wrath of the Ancients','Kreema\'ahm la Ahmahm','Kreeaho\'ahm nal Ahmhogaroc','Kreegakaleet lu Gosata\'ahm','Kreeholo lu Kreemasaleet']
BASE='https://callofduty.fandom.com'
HEADERS={'User-Agent':'CodGuideSourceReview/0.14 (noncommercial attribution-preserving wiki research; https://github.com/q2386550600-arch/cod15-zombies-guide)'}

def request(url):
 r=requests.get(url,headers=HEADERS,timeout=(10,22));r.raise_for_status();return r

def fetch(title):
 safe=hashlib.sha256(title.encode()).hexdigest()[:16];url=BASE+'/wiki/'+quote(title.replace(' ','_'),safe='/');record={'title':title,'url':url,'errors':[],'fetched':False}
 try:
  r=request(url);html=r.text
  soup=BeautifulSoup(html,'html.parser');root=soup.select_one('#mw-content-text .mw-parser-output')
  if root is None:raise ValueError('No article root (challenge, redirect or non-article response)')
  if len(root.get_text(' ',strip=True))<100:raise ValueError('Article root too short')
  record['licenseLinks']=[{'label':a.get_text(' ',strip=True),'url':urljoin(url,a.get('href',''))} for a in soup.find_all('a',href=True) if 'creativecommons.org/licenses/' in a['href']]
  record['revision']=next(iter(re.findall(r'"wgRevisionId"\s*:\s*(\d+)',html)),None)
  record['historyUrl']=BASE+'/wiki/'+quote(title.replace(' ','_'),safe='/')+'?action=history'
  record['sha256']=hashlib.sha256(r.content).hexdigest();record['file']=safe+'.html';record['articleFile']=safe+'-article.html'
  (OUT/record['file']).write_bytes(r.content);(OUT/record['articleFile']).write_text(str(root))
  record['textLength']=len(root.get_text(' ',strip=True))
  record['headings']=[e.get_text(' ',strip=True) for e in root.find_all(['h2','h3','h4','h5'])]
  record['articleLinks']=[{'text':a.get_text(' ',strip=True),'url':urljoin(url,a['href'])} for a in root.find_all('a',href=True)]
  record['images']=[{'src':i.get('data-src',i.get('src','')),'alt':i.get('alt',''),'filePage':urljoin(url,i.parent.get('href','')) if i.parent.name=='a' else ''} for i in root.find_all('img')]
  record['videos']=[{'url':urljoin(url,i.get('src',i.get('data-src',''))),'title':i.get('title','')} for i in root.find_all('iframe')]
  record['fetched']=True
 except Exception as exc:record['errors'].append(type(exc).__name__+': '+str(exc))
 print(title,record['fetched'],record.get('textLength'),record['errors'],flush=True)
 return record
# Probe three articles before scheduling all requests: avoid hammering a blocked host.
results=[fetch(t) for t in TITLES[:3]]
if any(x['fetched'] for x in results):
 for title in TITLES[3:]:
  time.sleep(.65);results.append(fetch(title))
else:
 for title in TITLES[3:]:results.append({'title':title,'url':BASE+'/wiki/'+quote(title.replace(' ','_'),safe='/'),'fetched':False,'errors':['Not attempted: all three connection probes failed.']})
 for endpoint in [BASE+'/api.php?action=parse&page=Cold_War_Remedy&prop=text%7Crevid%7Clinks%7Cimages&format=json',BASE+'/wiki/Special:Export/Cold_War_Remedy']:
  try:
   r=request(endpoint);(OUT/('api-probe-'+str(len(list(OUT.glob('api-*'))))+'.txt')).write_bytes(r.content);print('API probe',r.status_code,len(r.content),r.text[:150],flush=True)
  except Exception as exc:print('API probe failed',repr(exc),flush=True)
(OUT/'catalog.json').write_text(json.dumps({'source':'Call of Duty Wiki contributors / Fandom','requested':len(TITLES),'fetched':sum(x['fetched'] for x in results),'pages':results,'method':'Full public page fetch; no translation or media-license completeness implied'},ensure_ascii=False,indent=2))
