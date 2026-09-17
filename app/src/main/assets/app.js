(()=>{
const DATA=window.ZOMBIE_DATA||{};
const GAMES=window.ZOMBIE_GAMES||{};
const GAME_ORDER=window.ZOMBIE_GAME_ORDER||[];
const $=id=>document.getElementById(id);
const esc=(s='')=>String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const STATE_KEY='cod-zombies-guide-v08-state',NOTE_KEY='cod-zombies-guide-v08-notes',REC_KEY='cod-zombies-guide-v08-recorder';
let state={game:'bo4',map:'alpha',step:0,done:{}};let notes={},rec={};
const BO4_QUICK={
ix:[['强化机','神殿地下：四塔冠军头插齐后解锁'],['挑战台','竞技场中央'],['拉塔方尖碑','拉塔祭坛室'],['地下金属杆','丹努隧道 / 奥丁隧道 / 诅咒房 / 坍塌隧道'],['最终入口','竞技场出生点对面传送门']],
voyage:[['哨兵神器','船尾 Poop Deck'],['4个强化机基座','Poop Deck / Turbine Room / Lower Grand Staircase / Cargo Hold'],['时钟机关','舰桥调分钟；船尾/引擎室调小时'],['元素封锁','毒 → 水 → 电 → 火'],['太阳系模型','货舱；太阳最后'],['Boss入口','Poop Deck 传送符号']],
blood:[['幽灵盾','全主线核心'],['3位数字','典狱长办公室用盾看'],['872','城堡隧道固定代码'],['秘密房','典狱长之家二楼'],['红石挑战','码头/发电房/新工业区/典狱长办公室/淋浴间'],['Boss','红石全部回实验室墙图后']],
classified:[['主结局','第150回合'],['强化机','51区体系'],['高回合点','Weapon Testing 一带'],['关键思路','稳定盾循环优先']],
dead:[['哨兵神器','主大厅大楼梯顶'],['3颗水晶','主人/奖杯区、酒窖、图书馆/书房'],['森林入口','3把 Tuning Fork'],['银弹','酒窖熔银 + 图书馆制作'],['三条主线','望远镜 / 雕像 / 骑士'],['Boss','森林深处']],
ancient:[['神器','Amphitheater'],['Golden Bridle','Intersection of Treasuries / Stoa'],['强化机','骑 Pegasus 去 Underworld'],['Apollo’s Will','Marketplace 工作台'],['四种 Hand','Charon/Gaia/Hemera/Ouranos'],['Boss','Center of the World']],
alpha:[['Rushmore','Operations'],['电拳套','Galvaknuckles'],['雪花电视','Beds / Lounge / Diner 三选一'],['字母房','A黄 B绿 C囚 D输血 E作战 F审讯'],['强化机','修4通风后地下 Beds'],['Boss','APD Control → 推回 Avogadro']],
tag:[['三处电','Docks / Bridge / Human Infusion'],['蓝石','Lighthouse Approach → Pablo'],['挑战图腾','五选二'],['转盘','Pablo → Artifact Storage'],['篝火','Sunken Path'],['最终护送','Golden PaP → Facility']]
};
const BO4_REC={
ix:[['r1','方尖碑第1轮','4个特殊敌人顺序'],['r2','方尖碑第2轮','4个特殊敌人顺序']],
voyage:[['air','空气时间','例如 3:15'],['earth','土地时间','例如 6:30'],['fire','火焰时间','例如 9:45'],['water','水时间','例如 12:00'],['planets','行星顺序','按模型记录']],
blood:[['kronorium','Kronorium 3位码','本局随机'],['morse','摩斯/挑战记录','直接记结果'],['trials','五挑战','完成顺序/状态']],
classified:[['round','当前/最高回合','例如 87']],
dead:[['zodiac','黄道符号','符号+划痕数'],['fires','壁炉组','1/2/3完成情况']],
ancient:[['oracle','Oracle 提示','Dormant Hand 位置'],['hands','Hand 进度','Charon/Gaia/Hemera/Ouranos']],
alpha:[['code1','电视1','字母+时间'],['code2','电视2','字母+时间'],['code3','电视3','字母+时间'],['code4','电视4','字母+时间'],['code5','电视5','字母+时间'],['final','第6钟最终密码','4位数']],
tag:[['clue1','供品线索1','字幕关键词'],['clue2','供品线索2','字幕关键词'],['clue3','供品线索3','字幕关键词'],['seal','Seal 线索','保险柜地点']]
};
function deepClone(v){return JSON.parse(JSON.stringify(v));}
function gameOfMap(k){for(const g of GAME_ORDER){if((GAMES[g]?.maps||[]).includes(k))return g;}return 'bo4';}
function validMapForGame(g,k){return (GAMES[g]?.maps||[]).includes(k)&&DATA[k];}
function firstMap(g){return (GAMES[g]?.maps||[]).find(k=>DATA[k])||Object.keys(DATA)[0];}
function safeLoad(){
  try{
    const raw=localStorage.getItem(STATE_KEY);
    if(raw){const s=JSON.parse(raw);if(s&&GAMES[s.game])state.game=s.game;if(s&&DATA[s.map])state.map=s.map;if(Number.isInteger(s.step))state.step=s.step;if(s.done&&typeof s.done==='object')state.done=s.done;}
    else{const old=JSON.parse(localStorage.getItem('bo4-guide-v07-state')||'{}');if(old&&DATA[old.map]){state={game:'bo4',map:old.map,step:Number.isInteger(old.step)?old.step:0,done:old.done||{}};}}
    notes=JSON.parse(localStorage.getItem(NOTE_KEY)||localStorage.getItem('bo4-guide-v07-notes')||'{}')||{};
    rec=JSON.parse(localStorage.getItem(REC_KEY)||localStorage.getItem('bo4-guide-v07-recorder')||'{}')||{};
  }catch(_){ }
  if(!validMapForGame(state.game,state.map)){state.game=gameOfMap(state.map);if(!validMapForGame(state.game,state.map))state.map=firstMap(state.game);}
  Object.keys(DATA).forEach(k=>{if(!Array.isArray(state.done[k]))state.done[k]=[];if(!rec[k])rec[k]={};});clampStep();save();saveNotes();saveRec();
}
function save(){localStorage.setItem(STATE_KEY,JSON.stringify(state));}
function saveNotes(){localStorage.setItem(NOTE_KEY,JSON.stringify(notes));}
function saveRec(){localStorage.setItem(REC_KEY,JSON.stringify(rec));}
function clampStep(){const len=DATA[state.map]?.steps?.length||1;state.step=Math.max(0,Math.min(Number(state.step)||0,len-1));}
function isDone(k,i){return (state.done[k]||[]).includes(i);}
function setDone(k,i,val){const s=new Set(state.done[k]||[]);val?s.add(i):s.delete(i);state.done[k]=[...s].sort((a,b)=>a-b);}
function selectGame(g){state.game=g;state.map=firstMap(g);state.step=0;save();render();window.scrollTo({top:0,behavior:'smooth'});}
function selectMap(k){state.map=k;state.game=gameOfMap(k);state.step=0;save();render();window.scrollTo({top:0,behavior:'smooth'});}
function selectStep(i){state.step=i;clampStep();save();renderStep();renderFlow();renderProgress();renderMapVisual();window.scrollTo({top:0,behavior:'smooth'});}
function renderGameTabs(){const h=$('gameTabs');h.innerHTML='';GAME_ORDER.forEach(g=>{const b=document.createElement('button');b.type='button';b.className='game-tab'+(g===state.game?' active':'');b.textContent=GAMES[g].name;b.onclick=()=>selectGame(g);h.appendChild(b);});}
function renderMapTabs(){const h=$('mapTabs');h.innerHTML='';(GAMES[state.game]?.maps||[]).forEach(k=>{if(!DATA[k])return;const b=document.createElement('button');b.type='button';b.className='tab'+(k===state.map?' active':'');b.textContent=DATA[k].name;b.onclick=()=>selectMap(k);h.appendChild(b);});}
function renderHeader(){const m=DATA[state.map],g=GAMES[state.game];$('gameLabel').textContent=g?g.name:'';$('mapName').textContent=m.name;$('mapMeta').textContent=`${m.quest} · ${m.difficulty} · ${m.time}`;$('source').textContent=`步骤核对：${m.source}`;$('requirements').innerHTML=(m.requirements||[]).map(x=>`<li>${esc(x)}</li>`).join('');}
function renderProgress(){const m=DATA[state.map],n=(state.done[state.map]||[]).length;$('progressText').textContent=`${n} / ${m.steps.length} 已完成`;$('progressBar').style.width=`${Math.round(n/m.steps.length*100)}%`;}
function wrapText(str,max=20){const out=[];let cur='';for(const ch of String(str||'')){cur+=ch;if(cur.length>=max||/[→/，；：]/.test(ch)){out.push(cur);cur='';}}if(cur)out.push(cur);return out.slice(0,3);}
function svgText(lines,x,y,size=14,fill='#f4f5f6',weight='500',anchor='start'){return `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" font-weight="${weight}" text-anchor="${anchor}" font-family="system-ui,Microsoft YaHei,sans-serif">${lines.map((l,i)=>`<tspan x="${x}" dy="${i?size+3:0}">${esc(l)}</tspan>`).join('')}</text>`;}
function mapFlowSvg(){const m=DATA[state.map],steps=m.steps,w=720,nodeW=300,nodeH=74,gap=28,h=76+steps.length*(nodeH+gap);let s=`<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#111418"/>${svgText([`${GAMES[state.game].short} · ${m.name} · 主线/生存流程`],28,30,18,'#f3c14b','800')}`;let prev=null;steps.forEach((st,i)=>{const left=i%2===0,x=left?28:w-nodeW-28,y=50+i*(nodeH+gap);if(prev){const x1=prev.x+(prev.left?nodeW:0),x2=x+(left?0:nodeW),y1=prev.y+nodeH/2,y2=y+nodeH/2;s+=`<path d="M${x1},${y1} C360,${y1} 360,${y2} ${x2},${y2}" fill="none" stroke="#46505b" stroke-width="2" stroke-dasharray="5 5"/>`;}const done=isDone(state.map,i),cur=i===state.step,stroke=cur?'#f3c14b':done?'#71d69a':'#3a424c',fill=cur?'#2b2516':done?'#17261e':'#1c2025';s+=`<rect x="${x}" y="${y}" width="${nodeW}" height="${nodeH}" rx="14" fill="${fill}" stroke="${stroke}" stroke-width="${cur?3:1.5}"/><circle cx="${x+24}" cy="${y+24}" r="14" fill="${done?'#71d69a':cur?'#f3c14b':'#2a3037'}"/><text x="${x+24}" y="${y+29}" text-anchor="middle" font-size="12" font-weight="800" fill="${done||cur?'#111':'#a8b0b8'}">${done?'✓':i+1}</text>${svgText(wrapText(st.title,16),x+48,y+23,14,'#f4f5f6','750')}${svgText(wrapText(st.place,22),x+48,y+58,11,'#9fa7b1','500')}`;prev={x,y,left};});return s+'</svg>';}
function stepLocatorSvg(){const m=DATA[state.map],i=state.step,st=m.steps[i],prev=m.steps[i-1],next=m.steps[i+1],w=720,h=245;const box=(x,title,place,kind)=>{const stroke=kind==='cur'?'#f3c14b':kind==='prev'?'#6cb6ff':'#b690ff',fill=kind==='cur'?'#2b2516':'#1c2025';return `<rect x="${x}" y="55" width="205" height="132" rx="16" fill="${fill}" stroke="${stroke}" stroke-width="${kind==='cur'?3:1.5}"/>${svgText(wrapText(title,13),x+14,85,14,'#f4f5f6','750')}${svgText(wrapText(place,16),x+14,128,11,'#aab1b9','500')}`;};let s=`<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#111418"/>${svgText(['当前步骤定位示意 · 非比例地图'],20,27,14,'#9fa7b1','600')}`;s+=box(20,'上一步',prev?prev.place:'主线从这里开始','prev')+`<path d="M225,121 H250" stroke="#6d7681" stroke-width="3"/>`+box(257,`第${i+1}步`,st.place,'cur')+`<path d="M462,121 H487" stroke="#6d7681" stroke-width="3"/>`+box(494,'下一步',next?next.place:'完成主线 / 生存目标','next');s+=svgText(['黄框 = 现在该去的区域'],360,222,13,'#f3c14b','750','middle');return s+'</svg>';}
function visualBlock(svg,title){return `${svg}<div class="visual-caption"><span>${esc(title)}</span><button type="button" class="zoom-visual">点开放大</button></div>`;}
function openVisual(svg,title){$('modalTitle').textContent=title;$('modalVisual').innerHTML=svg;$('visualModal').classList.add('open');}
function closeVisual(){$('visualModal').classList.remove('open');$('modalVisual').innerHTML='';}
function bindZoom(host,title){const svg=host.querySelector('svg'),b=host.querySelector('.zoom-visual');if(svg)svg.onclick=()=>openVisual(svg.outerHTML,title);if(b)b.onclick=()=>openVisual(svg.outerHTML,title);}
function renderMapVisual(){const h=$('mapVisual');h.innerHTML=visualBlock(mapFlowSvg(),`${DATA[state.map].name} 完整流程图`);bindZoom(h,`${DATA[state.map].name} 完整流程图`);}
function renderStep(){const m=DATA[state.map],s=m.steps[state.step];$('stepNo').textContent=`第 ${state.step+1} / ${m.steps.length} 步`;$('stepTitle').textContent=s.title;$('stepPlace').textContent='地点：'+s.place;$('stepAction').textContent=s.action;$('stepSuccess').textContent=s.success;$('stepTips').textContent=s.tips||'—';$('prevBtn').disabled=state.step===0;$('nextBtn').textContent=state.step===m.steps.length-1?'标记完成':'完成这一步 →';$('doneBtn').textContent=isDone(state.map,state.step)?'✓ 已完成（点此取消）':'标记当前步骤完成';$('doneBtn').classList.toggle('done-active',isDone(state.map,state.step));const h=$('stepVisual');h.innerHTML=visualBlock(stepLocatorSvg(),'当前步骤位置关系');bindZoom(h,'当前步骤位置关系');}
function getQuick(){if(BO4_QUICK[state.map])return BO4_QUICK[state.map];const m=DATA[state.map];return m.steps.slice(0,6).map(s=>[s.title,s.place]);}
function renderQuick(){const q=getQuick(),p=$('quickPills'),l=$('quickList');p.innerHTML='';l.innerHTML='';q.forEach(([a,b])=>{const x=document.createElement('button');x.type='button';x.textContent=a;x.onclick=()=>{$('search').value=a;renderSearch();$('search').focus();};p.appendChild(x);const li=document.createElement('li');li.innerHTML=`<b>${esc(a)}</b>：${esc(b)}`;l.appendChild(li);});}
function specsForMap(){const m=DATA[state.map];if(Array.isArray(m.recorder)&&m.recorder.length)return m.recorder.map(x=>[x.key,x.label,x.placeholder||'']);if(BO4_REC[state.map])return BO4_REC[state.map];return [['misc','本图随机信息','密码、符号、顺序、分工…']];}
function renderRecorder(){const h=$('recorder'),spec=specsForMap();h.innerHTML='<div class="rec-grid">'+spec.map(([k,l,p])=>`<label class="rec-item"><span>${esc(l)}</span><input class="tool-input rec-input" data-rkey="${esc(k)}" placeholder="${esc(p)}" value="${esc(rec[state.map]?.[k]||'')}"></label>`).join('')+'</div>'+(state.map==='alpha'?'<div class="tool-box clock-tool"><h4>Alpha Omega 时钟快捷计算</h4><div class="muted">互动=分钟+15，近战=小时+1。只做计算辅助，不替你判断电视顺序。</div><div class="tool-row"><input id="clockCur" class="tool-input" placeholder="当前 0630"><input id="clockTar" class="tool-input" placeholder="目标 0245"></div><button id="clockCalc" class="mini-btn" type="button">计算最少操作</button><div id="clockOut" class="tool-result"></div></div>':'');h.querySelectorAll('.rec-input').forEach(el=>el.oninput=e=>{rec[state.map][e.target.dataset.rkey]=e.target.value;saveRec();});if(state.map==='alpha'){$('clockCalc').onclick=()=>{const parse=v=>{const d=String(v||'').replace(/\D/g,'').padStart(4,'0').slice(-4);let hh=Number(d.slice(0,2))%12,mm=Number(d.slice(2));if(mm%15!==0||mm>45)return null;return hh*60+mm;},a=parse($('clockCur').value),b=parse($('clockTar').value);if(a==null||b==null){$('clockOut').textContent='请输入 4 位时间，分钟只能是 00/15/30/45。';return;}let best=null;for(let h=0;h<12;h++)for(let m=0;m<4;m++){if((a+h*60+m*15)%720===b){const n=h+m;if(!best||n<best.n)best={h,m,n};}}$('clockOut').textContent=best?`近战 ${best.h} 次 + 互动 ${best.m} 次`:'未找到结果';};}}
function renderNotes(){$('notes').value=notes[state.map]||'';}
function renderFlow(){const h=$('flow');h.innerHTML='';DATA[state.map].steps.forEach((s,i)=>{const b=document.createElement('button');b.type='button';b.className='flow-row'+(i===state.step?' current':'')+(isDone(state.map,i)?' done':'');b.innerHTML=`<span class="flow-num">${isDone(state.map,i)?'✓':i+1}</span><span class="flow-copy"><b>${esc(s.title)}</b><small>${esc(s.place)}</small></span>`;b.onclick=()=>selectStep(i);h.appendChild(b);});}
function renderSearch(){const q=$('search').value.trim().toLowerCase(),box=$('searchResults');box.innerHTML='';if(!q){box.hidden=true;return;}const hits=[];GAME_ORDER.forEach(g=>(GAMES[g]?.maps||[]).forEach(k=>{const m=DATA[k];if(!m)return;m.steps.forEach((s,i)=>{const hay=`${GAMES[g].name} ${m.name} ${m.english||''} ${s.title} ${s.place} ${s.action} ${s.tips||''}`.toLowerCase();if(hay.includes(q))hits.push({g,k,i,s,m});});}));box.hidden=false;if(!hits.length){box.innerHTML='<div class="search-empty">没搜到。可以搜：月球、起源、时钟、盾牌、Richtofen、Maxis、Boss。</div>';return;}hits.slice(0,50).forEach(h=>{const b=document.createElement('button');b.type='button';b.className='search-hit';b.innerHTML=`<b>${esc(GAMES[h.g].short)} · ${esc(h.m.name)} · ${esc(h.s.title)}</b><small>${esc(h.s.place)}</small>`;b.onclick=()=>{state.game=h.g;state.map=h.k;state.step=h.i;save();$('search').value='';box.hidden=true;render();window.scrollTo({top:0,behavior:'smooth'});};box.appendChild(b);});}
function render(){clampStep();renderGameTabs();renderMapTabs();renderHeader();renderQuick();renderProgress();renderMapVisual();renderStep();renderRecorder();renderNotes();renderFlow();}
$('prevBtn').onclick=()=>{if(state.step>0)selectStep(state.step-1);};
$('nextBtn').onclick=()=>{setDone(state.map,state.step,true);if(state.step<DATA[state.map].steps.length-1)state.step++;save();render();window.scrollTo({top:0,behavior:'smooth'});};
$('doneBtn').onclick=()=>{setDone(state.map,state.step,!isDone(state.map,state.step));save();renderStep();renderFlow();renderProgress();renderMapVisual();};
$('resetBtn').onclick=()=>{if(confirm(`清空“${DATA[state.map].name}”完成进度？记录器和记事不会删。`)){state.done[state.map]=[];state.step=0;save();render();}};
$('notes').oninput=e=>{notes[state.map]=e.target.value;saveNotes();$('noteStatus').textContent='已保存';clearTimeout(window.__nt);window.__nt=setTimeout(()=>$('noteStatus').textContent='自动保存',800);};
$('search').oninput=renderSearch;$('searchClear').onclick=()=>{$('search').value='';renderSearch();$('search').focus();};
$('modalClose').onclick=closeVisual;$('visualModal').onclick=e=>{if(e.target===$('visualModal'))closeVisual();};document.addEventListener('keydown',e=>{if(e.key==='Escape')closeVisual();});
safeLoad();render();
})();