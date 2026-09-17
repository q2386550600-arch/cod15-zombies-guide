const fs=require('fs'),vm=require('vm'),P=(process.argv[2]||'app/src/main/assets').replace(/\/$/,'')+'/';
global.window=global;
for(const f of ['data.js','bo1-data.js','bo2-data.js','bo3-data.js','games.js','media.js','v09-fixes.js','image-help.js','image-bilingual.js','image-goals.js','zh-locale.js','zh-display.js','navigation.js','source-index.js','details.js'])vm.runInThisContext(fs.readFileSync(P+f,'utf8'),{filename:f});
const out={maps:ZOMBIE_DATA,media:COMMUNITY_MEDIA,source:SOURCE_INDEX,captions:{}};
for(const [key,s]of Object.entries(COMMUNITY_MEDIA.maps))out.captions[s.guide]=COMMUNITY_MEDIA.guides[s.guide].images.map(p=>ZhDisplay.info(key,p,false));
fs.writeFileSync(process.argv[3]||__dirname+'/export.json',JSON.stringify(out,null,2));
console.log('Exported 41 existing map entries and pinned source associations.');
