from pathlib import Path
import argparse
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path('.'));a=p.parse_args();R=Path(__file__).parent;P=a.root/'app/src/main/assets'
s=(P/'v012.js').read_text()
s="""for(let i=7;i<=11;i++)ZOMBIE_DATA.bo3_gorod.steps[i].title='随机挑战 '+(i-6)+' / 5（按亮起奖杯选择）';
ZOMBIE_DATA.bo3_rev.steps[9].title='召唤钥匙命中地图遗物';
ZOMBIE_DATA.bo2_mob.steps[3].title='猎犬斧、五个骷髅与勺子';
"""+s
s=s.replace('function stepPhotos(){','function legacyStepPhotos(){',1).replace('function renderStep(){','function legacyRenderStep(){',1)
i=s.index('function next(){');j=s.index('function showModal(',i);s=s[:i]+s[j:]
i=s.index('function currentSections(');j=s.index('function openAtlas(',i);s=s[:i]+(R/'reader.js').read_text()+'\n'+s[j:]
i=s.index('window.GuideDebug=');s=s[:i]+(R/'micro.js').read_text()+'\n'+s[i:]
s=s.replace('media:()=>M,currentPhotos:()=>photos','detailFrames,detailPos,currentFrame,openDetailIndex,openValve,media:()=>M,currentPhotos:()=>photos')
s=s.replace("const t=D[state.map].steps[i].title;return", "const t=D[state.map].steps[i].title;if(state.map==='bo1_cotd'&&state.cotdMode==='solo'&&[3,5].includes(i))return false;return")
s=s.replace("state.done[state.map]=[];state.step=0;", "state.done[state.map]=[];for(const field of ['detailPositions','detailCompletedChoices'])for(const k of Object.keys(state[field]||{}))if(k.startsWith(state.map+':'))delete state[field][k];state.step=0;")
s=s.replace("legacyRenderStep();const f=", "$('next').disabled=false;$('toggleDone').hidden=false;$('stepSuccess').closest('section').hidden=false;legacyRenderStep();const f=")
(P/'v013.js').write_text(s)
css=(P/'v012.css').read_text()+'''
.detailControls{margin:10px 0 14px}.readerTools{display:flex;gap:8px;flex-wrap:wrap;margin:12px 0}.readerTools button{flex:1;font-size:13px;min-width:115px}.sourceChapter{width:100%;display:block;text-align:left;margin:7px 0;padding:12px}.sourceChapter b{display:block;font-size:15px;font-weight:600;line-height:1.55}.sourceChapter small{display:block;margin-top:5px}.completeText{padding-left:24px}.completeText li{font-size:17px;line-height:1.8;padding:4px 0;margin-bottom:14px}.sourcePoint{border-top:1px solid var(--line);padding:14px 0}.sourcePoint img{width:100%;height:auto;display:block;aspect-ratio:auto}.valveRow{display:flex;justify-content:space-between;gap:14px;padding:12px;border-bottom:1px solid var(--line)}.valveRow b{color:var(--accent)}.bookList{margin:12px 0}#detailChoice{font-size:14px;line-height:1.5}#stageLabel{line-height:1.7}#stepDetails[hidden]{display:none!important}.detailJump{width:100%;text-align:left;line-height:1.6;margin:5px 0}
'''
(P/'v013.css').write_text(css)
h=(P/'index.html').read_text().replace('v0.12 · 地图定位版','v0.13 · 详细教程版').replace('v012.css','v013.css').replace('<script src="v012.js"></script>','<script src="offline-guides.js"></script><script src="v013.js"></script>')
(P/'index.html').write_text(h)
f=a.root/'app/build.gradle';g=f.read_text().replace('versionCode 12','versionCode 13').replace("versionName '0.12'","versionName '0.13'");f.write_text(g)
print('v0.13 applied: offline Chinese procedures and micro-step navigation; old storage and identity unchanged.')
