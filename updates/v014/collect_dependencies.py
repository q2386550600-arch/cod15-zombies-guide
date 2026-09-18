"""Follow article-owned dependency links without following global navboxes."""
from pathlib import Path
from urllib.parse import quote,unquote,urljoin,urlparse
from collections import deque
import requests,json,time,re,hashlib
from bs4 import BeautifulSoup
OUT=Path('source-archive');BASE='https://callofduty.fandom.com';API=BASE+'/api.php'
cat=json.loads((OUT/'catalog.json').read_text());known={p['title'] for p in cat['pages'] if p.get('fetched')};requested={p['requestedTitle'] for p in cat['pages']};edges=[]
QUEUE=['Revelations (map)','Kraken (wonder weapon)','Turbine (Zombies)']
# These dependencies are explicitly linked by the collected article body.
for rec in cat['pages']:
 if not rec.get('fetched'):continue
 raw=json.loads((OUT/rec['file']).read_text())['parse'];html=BeautifulSoup(raw['text']['*'],'html.parser')
 for nav in html.select('.navbox, #toc, .mw-editsection, #va-titleicons'):nav.decompose()
 for a in html.select('a[href]'):
  h=a.get('href','')
  if not h.startswith('/wiki/'):continue
  title=unquote(h.split('/wiki/',1)[1]).split('#',1)[0].replace('_',' ')
  edges.append({'from':rec['title'],'to':title,'label':a.get_text(' ',strip=True)})
  if re.search(r'/Transcript$|/Quotes$|/Radios|/Ciphers|/Trivia$|Easter Egg|Easter egg|Musical Easter|Melee Weapons|Bowie|Redeemer|Spoon|Spork|Exalted|Upgrad|Dragon Egg|Easter Eggs/|Side Quest',title):
   if not any(title.startswith(x) for x in ['File:','Template:','Category:','User:','Special:']):QUEUE.append(title)
QUEUE=list(dict.fromkeys(x for x in QUEUE if x not in known and x not in requested))
print('Dependencies requested',len(QUEUE),QUEUE,flush=True)
for title in QUEUE:
 rec={'requestedTitle':title,'title':title,'url':BASE+'/wiki/'+quote(title.replace(' ','_'),safe='/'),'fetched':False,'errors':[],'discoveredDependency':True}
 try:
  r=requests.get(API,params={'action':'parse','page':title,'prop':'text|wikitext|revid|links|images|externallinks|sections|categories|displaytitle','redirects':1,'format':'json'},timeout=(10,35));r.raise_for_status();j=r.json()
  if 'error' in j:raise ValueError(j['error'])
  p=j['parse'];safe=str(p['pageid'])+'-'+str(p['revid']);rec.update({'title':p['title'],'pageid':p['pageid'],'revision':p['revid'],'file':safe+'.json','articleFile':safe+'.html','wikitextFile':safe+'.wiki','sha256':hashlib.sha256(r.content).hexdigest(),'textLength':len(BeautifulSoup(p['text']['*'],'html.parser').get_text(' ',strip=True)),'historyUrl':BASE+'/wiki/'+quote(p['title'].replace(' ','_'),safe='/')+'?action=history','fixedUrl':BASE+'/wiki/'+quote(p['title'].replace(' ','_'),safe='/')+'?oldid='+str(p['revid']), 'sections':p.get('sections',[]),'images':p.get('images',[]),'externalLinks':p.get('externallinks',[]),'links':p.get('links',[]),'fetched':True})
  (OUT/rec['file']).write_bytes(r.content);(OUT/rec['articleFile']).write_text(p['text']['*']);(OUT/rec['wikitextFile']).write_text(p.get('wikitext',{}).get('*',''))
 except Exception as exc:rec['errors'].append(repr(exc))
 cat['pages'].append(rec);print(title,rec['fetched'],rec.get('textLength'),rec['errors'],flush=True);time.sleep(.25)
cat['requested']=len(cat['pages']);cat['fetched']=sum(p.get('fetched',False) for p in cat['pages']);cat['dependencyEdges']=edges
(OUT/'catalog.json').write_text(json.dumps(cat,ensure_ascii=False,indent=2))
try:
 r=requests.get('https://www.fandom.com/licensing',timeout=25);r.raise_for_status();(OUT/'fandom-licensing.html').write_bytes(r.content)
except Exception as exc:(OUT/'fandom-licensing-error.txt').write_text(repr(exc))
