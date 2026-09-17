/* Chinese is the reading language. English is supplemental nomenclature only. */
(()=>{'use strict';
const data=window.ZH_LOCALE,source=window.IMAGE_HELP_DATA;
const named={...source.TERMS,...window.IMAGE_HELP.terms,'Rushmore':'拉什莫尔电脑','Sawyer':'索耶','McCain':'麦凯恩','Pernell':'珀内尔','Vril Device':'维里尔装置','Vril Sphere':'维里尔球','Vril':'维里尔','Groph':'格罗夫','S.O.P.H.I.A.':'索菲娅','EMP':'电磁脉冲手雷','BO1':'黑色行动1','BO3':'黑色行动3','Lunger Undermines':'朗格矿道','G-Strike':'雷霆空袭信标','G-Strikes':'雷霆空袭信标','APD':'美国金字塔装置'};
for(const [k,v]of Object.entries(data.headings))if(k.startsWith('"'))named[k.slice(1,-1)]=v;
const escape=s=>s.replace(/[.*+?^${}()|[\]\\]/g,'\\$&');
const entries=Object.entries(named).sort((a,b)=>b[0].length-a[0].length),enRx=new RegExp('(?<![A-Za-z])('+entries.map(x=>escape(x[0])).join('|')+')(?![A-Za-z])','gi'),lookup=Object.fromEntries(entries.map(([en,zh])=>[en.toLowerCase(),zh]));
const optional={'酒馆':'Saloon','断头台':'Guillotine','绞刑架':'Gallows','枪械店':'Gunsmith','卫星碟':'Satellite Dish','卫星天线盘':'Satellite Dish','里希托芬':'Richtofen','麦克西斯':'Maxis','朗格矿道':'Lunger Undermines','女巫宅邸':"Witches' Mansion",'瘫痪器':'Paralyzer','脑腐':'Brain Rot','秃鹫援助':'Vulture Aid','电拳套':'Galvaknuckles','召唤之钥':'Summoning Key','维里尔':'Vril','拉什莫尔电脑':'Rushmore'},zhRx=new RegExp(Object.keys(optional).sort((a,b)=>b.length-a.length).map(escape).join('|'),'g');
function text(raw,showEnglish=true){const seen=new Set();let count=0;const parts=String(raw??'').split(/(（[^）]*）|\([^)]*\))/g);return parts.map((part,partIndex)=>{if(!part||/^[（(]/.test(part))return part||'';part=part.replace(enRx,match=>{const zh=lookup[match.toLowerCase()];seen.add(zh);return showEnglish?zh+'（'+match+'）':zh;});return part.replace(zhRx,(word,offset,whole)=>{if(!showEnglish||count>=4||seen.has(word)||/^[（(]/.test(whole.slice(offset+word.length))||(offset+word.length===whole.length&&/^[（(]/.test(parts[partIndex+1]||'')))return word;seen.add(word);count++;return word+'（'+optional[word]+'）';});}).join('');}
function heading(h){return data.headings[h]||text(h,false);}
function info(map,p,showEnglish=true){const h=ImageHelp.info(map,p),g=COMMUNITY_MEDIA.maps[map]?.guide,title=data.captions[g+':'+p.index]||h.titleZH,where=data.captions[g+':'+p.index]||h.whereZH;return {title:text(title,showEnglish),where:text(where,showEnglish),action:text(h.taskZH,showEnglish),heading:heading(p.last_heading)};}
window.ZhDisplay={text,heading,info};
})();
