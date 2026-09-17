import fs from 'node:fs';import vm from 'node:vm';
global.window=global;const base='app/src/main/assets/';
for(const f of ['data.js','bo1-data.js','bo2-data.js','bo3-data.js','games.js','media.js','v09-fixes.js','image-help.js','image-bilingual.js','image-goals.js'])vm.runInThisContext(fs.readFileSync(base+f,'utf8'),{filename:f});
let all=[],seen=new Set();for(const [map,s]of Object.entries(COMMUNITY_MEDIA.maps)){if(seen.has(s.guide))continue;seen.add(s.guide);for(const p of COMMUNITY_MEDIA.guides[s.guide].images)all.push({map,g:s.guide,index:p.index,caption:p.caption,heading:p.last_heading,...ImageHelp.info(map,p)});}
const gaps=all.filter(p=>!/[\u4e00-\u9fff]/.test(p.titleZH));if(gaps.length!==655)throw Error('Unexpected source caption baseline');
const rows=[1,2,3].flatMap(i=>fs.readFileSync('updates/v011/captions-'+i+'.tsv','utf8').trim().split('\n'));if(rows.length!==655)throw Error('Missing captions');
const captions={};for(const row of rows){const tab=row.indexOf('\t'),n=Number(row.slice(0,tab)),text=row.slice(tab+1),p=gaps[n];if(!p||!text||captions[p.g+':'+p.index])throw Error('Invalid duplicate caption');captions[p.g+':'+p.index]=text;}
const heads=[...new Set(all.map(p=>p.heading))],translated=fs.readFileSync('updates/v011/headings-translations.txt','utf8').trim().split('\n');if(heads.length!==325||translated.length!==heads.length)throw Error('Heading baseline mismatch');
const headings=Object.fromEntries(heads.map((h,i)=>[h,translated[i]]));
fs.writeFileSync(base+'zh-locale.js','window.ZH_LOCALE='+JSON.stringify({captions,headings})+';\n');console.log('Chinese captions:',rows.length,'headings:',heads.length);
