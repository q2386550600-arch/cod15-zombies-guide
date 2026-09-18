"""Preserve article text, tables, figures and links in their original order."""
from pathlib import Path
from urllib.parse import urljoin,quote
from bs4 import BeautifulSoup,Tag,NavigableString,Comment
import argparse,json,re,hashlib
BLOCKS={'p','li','dt','dd','h1','h2','h3','h4','h5','h6','figcaption','caption','td','th','summary','blockquote','pre'}
STRUCT={'ul','ol','dl','table','thead','tbody','tfoot','tr','figure','aside','details'}
ALL_BLOCK=BLOCKS|STRUCT
SKIP='#toc, .mw-editsection, #va-titleicons, .navbox, .mw-parser-output > .wikia-ad, script, style, noscript'
def normalize(s):return re.sub(r'[ \t\r\f\v]+',' ',s).strip()
class Parser:
 def __init__(self,meta,html):
  self.meta=meta;self.soup=BeautifulSoup(html,'lxml');self.root=self.soup.select_one('.mw-parser-output') or self.soup
  self.removed=[];self.units=[];self.media=[];self.headings=[]
  for n in self.root.select(SKIP):
   if n.parent:self.removed.append({'tag':n.name,'class':n.get('class',[]),'textLength':len(n.get_text())});n.decompose()
  for c in self.root.find_all(string=lambda t:isinstance(t,Comment)):c.extract()
 def unit(self,text,tag='p',links=None):
  text=normalize(text)
  if not text:return None
  uid=f"p{self.meta['pageid']}-u{len(self.units):05}"
  self.units.append({'id':uid,'en':text,'tag':tag,'links':links or []});return {'t':'text','id':uid,'tag':tag}
 def image(self,tag):
  url=tag.get('data-src',tag.get('src',''))
  if not url or url.startswith('data:'):return None
  original=re.sub(r'/revision/latest/(?:scale-to-width-down|scale-to-width|scale-to-height-down|scale-to-height|smart|thumbnail)/[^?]+','/revision/latest',url)
  name=tag.get('data-image-name',tag.get('data-image-key',''));a=tag.find_parent('a',href=True)
  page='https://callofduty.fandom.com/wiki/File:'+quote(name.replace(' ','_')) if name else (urljoin(self.meta['url'],a['href']) if a else original)
  im={'url':url,'originalUrl':original,'alt':tag.get('alt',''),'name':name,'width':tag.get('width'),'height':tag.get('height'),'filePage':page,'id':f"p{self.meta['pageid']}-im{len(self.media):04}"};self.media.append(im)
  node={'t':'image','id':im['id']}
  if im['alt']:node['altUnit']=self.unit(im['alt'],'image-alt')['id']
  return node
 def links(self,tag):return [{'text':a.get_text(' ',strip=True),'url':urljoin(self.meta['url'],a['href'])} for a in tag.find_all('a',href=True) if a['href'] and not a['href'].lower().startswith('javascript:')]
 def group(self,nodes,tag='div',attrs=None):
  children=[];run=[]
  def flush():
   if not run:return
   frag=BeautifulSoup(''.join(str(n) for n in run),'lxml')
   for br in frag.find_all('br'):br.replace_with('\n')
   u=self.unit(frag.get_text(' ',strip=True),'p',self.links(frag))
   if u:children.append(u)
   for im in frag.find_all('img'):
    x=self.image(im)
    if x:children.append(x)
   for frame in frag.find_all(['iframe','video','audio']):
    src=frame.get('src',frame.get('data-src',''))
    if src:children.append({'t':'embed','url':urljoin(self.meta['url'],src),'label':frame.get('title',src)})
   run.clear()
  for n in nodes:
   if isinstance(n,Comment):continue
   if isinstance(n,NavigableString):
    if n.strip():run.append(n)
   elif isinstance(n,Tag):
    if n.name in ALL_BLOCK or n.name in {'div','section','img','iframe','video','audio'}:
     flush();child=self.parse(n)
     if child:children.append(child)
    elif n.name not in {'script','style'}:run.append(n)
  flush();return {'t':'group','tag':tag,'attrs':attrs or {},'children':children} if children else None
 def parse(self,n):
  if n.name=='img':return self.image(n)
  if n.name in {'iframe','video','audio'}:
   url=n.get('src',n.get('data-src',''))
   if url:return {'t':'embed','url':urljoin(self.meta['url'],url),'label':n.get('title',url)}
   return self.group(list(n.contents))
  attrs={k:str(n[k]) for k in ['colspan','rowspan','start','value','id'] if n.get(k) is not None}
  if n.name in BLOCKS and not n.find(list(ALL_BLOCK)):
   u=self.unit(n.get_text(' ',strip=True),n.name,self.links(n))
   if u:
    u['attrs']=attrs
    if re.fullmatch(r'h[1-6]',n.name):
     h=n.find(class_='mw-headline');u['anchor']=h.get('id','') if h else n.get('id','');self.headings.append({'unit':u['id'],'text':n.get_text(' ',strip=True),'level':int(n.name[1]),'anchor':u['anchor']})
    u['images']=[x for x in [self.image(im) for im in n.find_all('img')] if x]
   elif n.find('img'):return self.group(list(n.contents),n.name,attrs)
   return u
  return self.group(list(n.contents),n.name if n.name in ALL_BLOCK else 'div',attrs)
 def finish(self):
  tree=self.group(list(self.root.contents));return {'metadata':self.meta,'tree':tree,'units':self.units,'images':self.media,'headings':self.headings,'removedChrome':self.removed,'bodyText':self.root.get_text(' ',strip=True)}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--source',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);args=ap.parse_args();args.out.mkdir(exist_ok=True,parents=True)
 catalog=json.loads((args.source/'catalog.json').read_text());pages=[];seen=set();units=[]
 for m in catalog['pages']:
  if not m.get('fetched') or m['pageid'] in seen:continue
  seen.add(m['pageid']);print('Parse',m['title'],flush=True);doc=Parser(m,(args.source/m['articleFile']).read_text()).finish();pages.append(doc);units+=doc['units'];(args.out/(str(m['pageid'])+'.json')).write_text(json.dumps(doc,ensure_ascii=False,separators=(',',':')))
 audit={'pages':len(pages),'textUnits':len(units),'englishCharacters':sum(len(u['en']) for u in units),'imageReferences':sum(len(p['images']) for p in pages),'headingCount':sum(len(p['headings']) for p in pages),'removedOnly':'Automated TOC, wiki-wide navigation, edit controls, language icons, scripts/styles. No filtering of loadouts, lore, procedures, trivia, references or optional tasks.'}
 (args.out/'units.json').write_text(json.dumps(units,ensure_ascii=False,separators=(',',':')));(args.out/'manifest.json').write_text(json.dumps({'pages':[p['metadata'] for p in pages],'audit':audit,'failures':[m for m in catalog['pages'] if not m.get('fetched')],'sourceAliases':{m.get('requestedTitle',m['title']):m['pageid'] for m in catalog['pages'] if m.get('fetched')}},ensure_ascii=False,indent=2));print(json.dumps(audit,ensure_ascii=False,indent=2))
if __name__=='__main__':main()
