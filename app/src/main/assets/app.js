(() => {
  const DATA = window.BO4_DATA;
  const ORDER = window.BO4_ORDER;
  const $ = (id) => document.getElementById(id);
  const esc = (s='') => String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const STORAGE_KEY = 'bo4-guide-v07-state';
  const NOTE_KEY = 'bo4-guide-v07-notes';
  const REC_KEY = 'bo4-guide-v07-recorder';

  let state = { map:'alpha', step:0, done:{} };
  let notes = {};
  let rec = {};

  const QUICK = {
    ix: [
      ['强化机','神殿地下：四座塔冠军头全部插上后解锁'],['挑战台','竞技场中央：开局砍旗帜可启动挑战'],['拉塔方尖碑','拉塔祭坛室：两轮特殊敌人顺序'],['地下金属杆','丹努隧道 / 奥丁隧道 / 诅咒房 / 坍塌隧道'],['最终入口','竞技场出生点对面传送门']
    ],
    voyage: [
      ['哨兵神器','船尾 Poop Deck 方向盘上方'],['4个强化机基座','Poop Deck / Turbine Room / Lower Grand Staircase / Cargo Hold'],['时钟机关','舰桥调分针；船尾调空气/土小时；引擎室调火/水小时'],['元素封锁顺序','毒 → 水 → 电 → 火'],['太阳系模型','货舱；太阳固定最后处理'],['Boss入口','Poop Deck 传送符号进入冰山']
    ],
    blood: [
      ['盾牌','Spectral Shield 全程关键；屋顶用盾冲击开强化机'],['3位数字','典狱长办公室用幽灵盾看隐藏数字'],['872','城堡隧道固定输入 872 进入 Zombie Blood'],['秘密房','典狱长之家二楼；需要 Brutus 砸墙'],['红石挑战','码头 / 发电房 / 新工业区 / 典狱长办公室 / 淋浴间'],['最终入口','全部红石回实验室墙图后推进剧情']
    ],
    classified: [
      ['主结局','不是传统解谜：唯一硬目标是第150回合'],['高回合推荐点','Weapon Testing 盾牌工作台附近'],['盾牌循环','Victorious Tortoise + 修盾/买盾'],['强化机','开电与传送后在 51 区体系内使用']
    ],
    dead: [
      ['哨兵神器','主大厅 Grand Staircase 顶部'],['3颗水晶','主人/奖杯区、酒窖、图书馆/书房'],['森林入口','3把 Tuning Fork 开门；森林内有强化机'],['银弹','先熔银制品，再配木炭/蝙蝠粪/硫磺'],['三条主线','望远镜 / 雕像 / 骑士，可任意顺序'],['最终Boss','森林深处，靠雕像光线制造绿色方框']
    ],
    ancient: [
      ['哨兵神器','Amphitheater 圆形剧场'],['金缰绳','Intersection of Treasuries 或 Stoa of the Athenians'],['强化机','骑 Pegasus 去 Underworld，完成鹰笼与封锁'],['Apollo’s Will','Marketplace 工作台制作'],['四种 Hand','Charon / Gaia / Hemera / Ouranos'],['最终战','Center of the World：Pegasus → Perseus']
    ],
    alpha: [
      ['Rushmore','Operations 作战室绿色电脑'],['电拳套','地图中央墙买 Galvaknuckles'],['雪花电视','只会在 Beds / Lounge / Diner 三选一'],['字母房映射','A黄房 B绿房 C囚房 D输血 E作战 F审讯'],['强化机','修好4台通风后在地下 Beds'],['最终战','APD Control 启动，最后把 Avogadro 推回 APD']
    ],
    tag: [
      ['三处电','Docks / Bridge / Human Infusion'],['蓝色岩石','Lighthouse Approach 洞穴；交给 Lighthouse 4 的 Pablo'],['挑战图腾','Frozen Crevasse / Forecastle / Beach / Lighthouse / Specimen Storage 五选二'],['转盘','Pablo 给4个 → Artifact Storage 安装'],['篝火','Sunken Path，用 Samantha’s Music Box 净化'],['最终护送','Golden PaP → 跟 Seal 保护圈一路回 Facility']
    ]
  };

  const REC_DEFAULTS = {
    ix:{r1:['','','',''],r2:['','','','']},
    voyage:{air:'',earth:'',fire:'',water:'',planets:''},
    blood:{kronorium:'',morse:'',trials:''},
    classified:{round:'1'},
    dead:{z1:'',z2:'',z3:'',marks1:'',marks2:'',marks3:''},
    ancient:{oracle:'',danu:'',hands:''},
    alpha:{codes:['','','','',''],final:'',clockCurrent:'0630',clockTarget:'0245'},
    tag:{clue1:'',clue2:'',clue3:'',seal:''}
  };

  function safeLoad() {
    try {
      const s = JSON.parse(localStorage.getItem(STORAGE_KEY) || '{}');
      if (s && DATA[s.map]) state.map = s.map;
      if (Number.isInteger(s.step)) state.step = s.step;
      if (s.done && typeof s.done === 'object') state.done = s.done;
      notes = JSON.parse(localStorage.getItem(NOTE_KEY) || '{}') || {};
      rec = JSON.parse(localStorage.getItem(REC_KEY) || '{}') || {};
    } catch (_) {}
    ORDER.forEach(k => {
      if (!Array.isArray(state.done[k])) state.done[k] = [];
      if (!rec[k]) rec[k] = JSON.parse(JSON.stringify(REC_DEFAULTS[k] || {}));
    });
    clampStep();
  }
  function save(){localStorage.setItem(STORAGE_KEY,JSON.stringify(state));}
  function saveNotes(){localStorage.setItem(NOTE_KEY,JSON.stringify(notes));}
  function saveRec(){localStorage.setItem(REC_KEY,JSON.stringify(rec));}
  function clampStep(){const len=DATA[state.map].steps.length;state.step=Math.max(0,Math.min(Number(state.step)||0,len-1));}
  function isDone(map,i){return state.done[map].includes(i);}
  function setDone(map,i,val){const set=new Set(state.done[map]);val?set.add(i):set.delete(i);state.done[map]=[...set].sort((a,b)=>a-b);}

  function selectMap(k){state.map=k;state.step=0;clampStep();save();render();window.scrollTo({top:0,behavior:'smooth'});}
  function selectStep(i){state.step=i;clampStep();save();renderStep();renderFlow();renderProgress();renderMapVisual();window.scrollTo({top:0,behavior:'smooth'});}

  function renderTabs(){
    const host=$('mapTabs');host.innerHTML='';
    ORDER.forEach(k=>{const b=document.createElement('button');b.type='button';b.className='tab'+(k===state.map?' active':'');b.textContent=DATA[k].name;b.addEventListener('click',()=>selectMap(k));host.appendChild(b);});
  }
  function renderHeader(){const m=DATA[state.map];$('mapName').textContent=m.name;$('mapMeta').textContent=`${m.quest} · ${m.difficulty} · ${m.time}`;$('source').textContent=`步骤核对：${m.source}`;$('requirements').innerHTML=m.requirements.map(x=>`<li>${esc(x)}</li>`).join('');}
  function renderProgress(){const m=DATA[state.map],complete=state.done[state.map].length;$('progressText').textContent=`${complete} / ${m.steps.length} 已完成`;$('progressBar').style.width=`${Math.round(complete/m.steps.length*100)}%`;}

  function wrapText(str,max=20){
    const s=String(str||''); const lines=[]; let cur='';
    for(const ch of s){cur+=ch;if(cur.length>=max||/[→/，；：]/.test(ch)){lines.push(cur);cur='';}}
    if(cur)lines.push(cur);return lines.slice(0,3);
  }
  function svgTextLines(lines,x,y,size=14,fill='#f4f5f6',weight='500',anchor='start'){
    return `<text x="${x}" y="${y}" font-size="${size}" fill="${fill}" font-weight="${weight}" text-anchor="${anchor}" font-family="system-ui,Microsoft YaHei,sans-serif">${lines.map((l,i)=>`<tspan x="${x}" dy="${i?size+3:0}">${esc(l)}</tspan>`).join('')}</text>`;
  }
  function mapFlowSvg(){
    const m=DATA[state.map],steps=m.steps; const w=720,nodeW=300,nodeH=74,gapY=28,pad=28; const rows=steps.length; const h=pad*2+rows*(nodeH+gapY)-gapY+28;
    let s=`<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="${esc(m.name)}主线流程示意"><rect width="100%" height="100%" fill="#111418"/>`;
    s+=svgTextLines([m.name+' · 主线流程示意'],28,28,18,'#f3c14b','800');
    let prev=null;
    steps.forEach((st,i)=>{
      const left=i%2===0; const x=left?28:w-nodeW-28; const y=48+i*(nodeH+gapY);
      if(prev){const x1=prev.x+(prev.left?nodeW:0),y1=prev.y+nodeH/2;const x2=x+(left?0:nodeW),y2=y+nodeH/2;s+=`<path d="M${x1},${y1} C360,${y1} 360,${y2} ${x2},${y2}" fill="none" stroke="#46505b" stroke-width="2" stroke-dasharray="5 5"/>`;}
      const done=isDone(state.map,i),cur=i===state.step; const stroke=cur?'#f3c14b':done?'#71d69a':'#3a424c';const fill=cur?'#2b2516':done?'#17261e':'#1c2025';
      s+=`<rect x="${x}" y="${y}" width="${nodeW}" height="${nodeH}" rx="14" fill="${fill}" stroke="${stroke}" stroke-width="${cur?3:1.5}"/>`;
      s+=`<circle cx="${x+24}" cy="${y+24}" r="14" fill="${done?'#71d69a':cur?'#f3c14b':'#2a3037'}"/><text x="${x+24}" y="${y+29}" text-anchor="middle" font-size="12" font-weight="800" fill="${done||cur?'#111':'#a8b0b8'}">${done?'✓':i+1}</text>`;
      s+=svgTextLines(wrapText(st.title,16),x+48,y+23,14,'#f4f5f6','750');
      s+=svgTextLines(wrapText(st.place,22),x+48,y+58,11,'#9fa7b1','500');
      prev={x,y,left};
    });
    s+=`</svg>`;return s;
  }
  function stepLocatorSvg(){
    const m=DATA[state.map],i=state.step,st=m.steps[i],prev=m.steps[i-1],next=m.steps[i+1],w=720,h=245;
    const box=(x,y,width,height,title,place,kind)=>{const stroke=kind==='cur'?'#f3c14b':kind==='prev'?'#6cb6ff':'#b690ff';const fill=kind==='cur'?'#2b2516':'#1c2025';return `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="16" fill="${fill}" stroke="${stroke}" stroke-width="${kind==='cur'?3:1.5}"/>${svgTextLines(wrapText(title,13),x+14,y+30,14,'#f4f5f6','750')}${svgTextLines(wrapText(place,16),x+14,y+73,11,'#aab1b9','500')}`;};
    let s=`<svg viewBox="0 0 ${w} ${h}" xmlns="http://www.w3.org/2000/svg"><rect width="100%" height="100%" fill="#111418"/>${svgTextLines(['当前步骤定位示意 · 非比例地图'],20,27,14,'#9fa7b1','600')}`;
    const y=55,bw=205,bh=132,g=32,x1=20,x2=257,x3=494;
    if(prev){s+=box(x1,y,bw,bh,'上一步',prev.place,'prev');s+=`<path d="M225,121 H250" stroke="#6d7681" stroke-width="3"/><path d="M244,114 l8,7 -8,7" fill="none" stroke="#6d7681" stroke-width="3"/>`;} else {s+=box(x1,y,bw,bh,'起点','当前主线从这里开始','prev');s+=`<path d="M225,121 H250" stroke="#6d7681" stroke-width="3"/>`;}
    s+=box(x2,y,bw,bh,`第${i+1}步`,st.place,'cur');
    if(next){s+=`<path d="M462,121 H487" stroke="#6d7681" stroke-width="3"/><path d="M481,114 l8,7 -8,7" fill="none" stroke="#6d7681" stroke-width="3"/>`;s+=box(x3,y,bw,bh,'下一步',next.place,'next');} else {s+=`<path d="M462,121 H487" stroke="#6d7681" stroke-width="3"/>`;s+=box(x3,y,bw,bh,'终点','完成主线 / 触发结局','next');}
    s+=svgTextLines(['黄框就是现在该去的区域'],360,222,13,'#f3c14b','750','middle');s+=`</svg>`;return s;
  }
  function visualBlock(svg,title){return `${svg}<div class="visual-caption"><span>${esc(title)}</span><button type="button" class="zoom-visual">点开放大</button></div>`;}
  function bindVisualZoom(host,title){const b=host.querySelector('.zoom-visual');if(!b)return;b.addEventListener('click',()=>openVisual(host.querySelector('svg').outerHTML,title));host.querySelector('svg')?.addEventListener('click',()=>openVisual(host.querySelector('svg').outerHTML,title));}
  function openVisual(svg,title){$('modalTitle').textContent=title;$('modalVisual').innerHTML=svg;$('visualModal').classList.add('open');}
  function closeVisual(){$('visualModal').classList.remove('open');$('modalVisual').innerHTML='';}

  function renderMapVisual(){const host=$('mapVisual');host.innerHTML=visualBlock(mapFlowSvg(),`${DATA[state.map].name} 主线流程图`);bindVisualZoom(host,`${DATA[state.map].name} 主线流程图`);}
  function renderStep(){
    const m=DATA[state.map],s=m.steps[state.step];
    $('stepNo').textContent=`第 ${state.step+1} / ${m.steps.length} 步`;$('stepTitle').textContent=s.title;$('stepPlace').textContent=`地点：${s.place}`;$('stepAction').textContent=s.action;$('stepSuccess').textContent=s.success;$('stepTips').textContent=s.tips||'—';$('prevBtn').disabled=state.step===0;$('nextBtn').textContent=state.step===m.steps.length-1?'标记完成':'完成这一步 →';$('doneBtn').textContent=isDone(state.map,state.step)?'✓ 已完成（点此取消）':'标记当前步骤完成';$('doneBtn').classList.toggle('done-active',isDone(state.map,state.step));
    const v=$('stepVisual');v.innerHTML=visualBlock(stepLocatorSvg(),`第${state.step+1}步定位示意`);bindVisualZoom(v,`第${state.step+1}步定位示意`);
  }
  function renderFlow(){const host=$('flow');host.innerHTML='';DATA[state.map].steps.forEach((s,i)=>{const row=document.createElement('button');row.type='button';row.className='flow-row'+(i===state.step?' current':'')+(isDone(state.map,i)?' done':'');const mark=isDone(state.map,i)?'✓':String(i+1);row.innerHTML=`<span class="flow-num">${mark}</span><span class="flow-copy"><b>${esc(s.title)}</b><small>${esc(s.place)}</small></span>`;row.addEventListener('click',()=>selectStep(i));host.appendChild(row);});}
  function renderNotes(){$('notes').value=notes[state.map]||'';}

  function renderQuick(){
    const items=QUICK[state.map]||[];$('quickList').innerHTML=items.map(x=>`<li><b>${esc(x[0])}</b>：${esc(x[1])}</li>`).join('');const pills=$('quickPills');pills.innerHTML='';items.forEach(x=>{const b=document.createElement('button');b.type='button';b.textContent=x[0];b.addEventListener('click',()=>{$('search').value=x[0];renderSearch();$('search').scrollIntoView({behavior:'smooth',block:'center'});});pills.appendChild(b);});
  }

  function field(label,key,value,placeholder=''){return `<div class="code-row"><label>${esc(label)}</label><input class="tool-input rec-field" data-key="${esc(key)}" value="${esc(value||'')}" placeholder="${esc(placeholder)}"></div>`;}
  function bindRecFields(){document.querySelectorAll('.rec-field').forEach(el=>el.addEventListener('input',()=>{const key=el.dataset.key;if(key.includes('.')){const [a,b]=key.split('.');if(!rec[state.map][a])rec[state.map][a]=[];rec[state.map][a][Number(b)]=el.value;}else rec[state.map][key]=el.value;saveRec();renderRecorderResult();}));}
  function parseHHMM(v){const s=String(v||'').replace(/\D/g,'').padStart(4,'0').slice(-4);let h=Number(s.slice(0,2)),m=Number(s.slice(2));if(h>23||m>59)return null;h%=12;if(h===0)h=12;return{h,m,s};}
  function alphaCalc(){const a=parseHHMM(rec.alpha.clockCurrent),b=parseHHMM(rec.alpha.clockTarget);if(!a||!b||b.m%15!==0||a.m%15!==0)return '请输入有效4位时间，分钟必须是00/15/30/45。';const hits=(b.h-a.h+12)%12;const presses=((b.m-a.m+60)%60)/15;return `从 ${a.s.slice(0,2)}:${a.s.slice(2)} → ${b.s.slice(0,2)}:${b.s.slice(2)}：电拳/近战敲 ${hits} 下，互动键按 ${presses} 下。`;}
  function renderRecorderResult(){
    const r=$('toolResult');if(!r)return;
    if(state.map==='alpha'){
      const map={A:'黄房',B:'绿房',C:'囚房区',D:'输血设施',E:'作战室',F:'审讯室'};const rows=(rec.alpha.codes||[]).map((v,i)=>{const s=String(v||'').toUpperCase().replace(/\s/g,'');const m=s.match(/^([A-F])(\d{4})$/);return m?`${i+1}. ${m[1]}=${map[m[1]]} → ${m[2].slice(0,2)}:${m[2].slice(2)}`:`${i+1}. ${s||'未填'}`;});r.innerHTML=`<b>按播报顺序：</b><br>${rows.map(esc).join('<br>')}<br><br>${esc(alphaCalc())}`;
    } else if(state.map==='voyage'){
      const out=['空气 Air='+rec.voyage.air,'土 Earth='+rec.voyage.earth,'火 Fire='+rec.voyage.fire,'水 Water='+rec.voyage.water].join('；');r.textContent=`记录：${out}。舰桥4杆调“分钟”；船尾调空气/土“小时”；引擎室调火/水“小时”。`;
    } else if(state.map==='classified'){
      const n=Math.max(1,Math.min(150,Number(rec.classified.round)||1));r.textContent=`当前 ${n} 回合，距离结局还差 ${150-n} 回合，完成度 ${Math.round(n/150*100)}%。`;
    } else r.textContent='已自动保存。';
  }
  function renderRecorder(){
    const host=$('recorder'),k=state.map,o=rec[k];let html='<div class="code-list">';
    if(k==='alpha'){
      html+='<div class="muted">电视播报5组代码一定按顺序填。A黄 B绿 C囚房 D输血 E作战 F审讯。</div>';
      for(let i=0;i<5;i++)html+=field(`第${i+1}组`,`codes.${i}`,o.codes[i],'E0215');
      html+=field('第6钟密码','final',o.final,'0745');
      html+='</div><div class="tool-box" style="margin-top:10px"><h4>时钟敲击计算器</h4><div class="muted">只算向前递增：近战+1小时，互动+15分钟。</div><div class="tool-row">'+`<input class="tool-input rec-field" data-key="clockCurrent" value="${esc(o.clockCurrent)}" placeholder="当前0630"><input class="tool-input rec-field" data-key="clockTarget" value="${esc(o.clockTarget)}" placeholder="目标0245">`+'</div><div id="toolResult" class="tool-result"></div></div>';
    } else if(k==='voyage'){
      html+='<div class="muted">记录四元素对应时钟时间；分钟机关和小时机关分开。</div>'+field('空气','air',o.air,'0350')+field('土','earth',o.earth,'0915')+field('火','fire',o.fire,'1205')+field('水','water',o.water,'0740')+field('行星顺序','planets',o.planets,'月→金→…→太阳')+'<div id="toolResult" class="tool-result"></div>';
    } else if(k==='blood'){
      html+=field('书本3位码','kronorium',o.kronorium,'483')+field('摩斯码','morse',o.morse,'... --- ...')+field('当前挑战','trials',o.trials,'码头/发电房/…')+'<div id="toolResult" class="tool-result"></div>';
    } else if(k==='classified'){
      html+=field('当前回合','round',o.round,'50')+'<div id="toolResult" class="tool-result"></div>';
    } else if(k==='dead'){
      html+='<div class="muted">望远镜线：记3个黄道符号和每个旁边划痕数，最后按划痕从少到多输入。</div>'+field('符号1','z1',o.z1,'♈/图案')+field('划痕1','marks1',o.marks1,'1')+field('符号2','z2',o.z2,'图案')+field('划痕2','marks2',o.marks2,'2')+field('符号3','z3',o.z3,'图案')+field('划痕3','marks3',o.marks3,'3')+'<div id="toolResult" class="tool-result"></div>';
    } else if(k==='ancient'){
      html+=field('Oracle线索','oracle',o.oracle,'Where the…')+field('Danu顺序','danu',o.danu,'1个→2个→3个')+field('Hand分工','hands',o.hands,'Charon=我…')+'<div id="toolResult" class="tool-result"></div>';
    } else if(k==='tag'){
      html+='<div class="muted">字幕打开后，把 Apothicon Blood 的三条供品线索和 Seal 线索原句/关键词记下来。</div>'+field('供品线索1','clue1',o.clue1,'关键词')+field('供品线索2','clue2',o.clue2,'关键词')+field('供品线索3','clue3',o.clue3,'关键词')+field('Seal线索','seal',o.seal,'Artifact Storage…')+'<div id="toolResult" class="tool-result"></div>';
    } else if(k==='ix'){
      html+='<div class="muted">拉塔方尖碑两轮各4个特殊敌人，必须按显示顺序击杀。</div>';for(let i=0;i<4;i++)html+=field(`第一轮${i+1}`,`r1.${i}`,o.r1[i],'老虎/毁灭者…');for(let i=0;i<4;i++)html+=field(`第二轮${i+1}`,`r2.${i}`,o.r2[i],'…');html+='<div id="toolResult" class="tool-result"></div>';
    } else html+='<div id="toolResult" class="tool-result">此图暂无额外随机码；自由记事仍会长期保存。</div>';
    html+='</div>';host.innerHTML=html;bindRecFields();renderRecorderResult();
  }

  function renderSearch(){
    const q=$('search').value.trim().toLowerCase(),box=$('searchResults');box.innerHTML='';if(!q){box.hidden=true;return;}const hits=[];
    ORDER.forEach(k=>DATA[k].steps.forEach((s,i)=>{const quick=(QUICK[k]||[]).map(x=>x.join(' ')).join(' ');const hay=`${DATA[k].name} ${DATA[k].english} ${s.title} ${s.place} ${s.action} ${s.tips} ${quick}`.toLowerCase();if(hay.includes(q))hits.push({k,i,s});}));box.hidden=false;if(!hits.length){box.innerHTML='<div class="search-empty">没搜到。可试：电视、时钟、蓝石、盾牌、图腾、强化机、872。</div>';return;}hits.slice(0,30).forEach(h=>{const b=document.createElement('button');b.type='button';b.className='search-hit';b.innerHTML=`<b>${esc(DATA[h.k].name)} · ${esc(h.s.title)}</b><small>${esc(h.s.place)}</small>`;b.addEventListener('click',()=>{state.map=h.k;state.step=h.i;save();$('search').value='';render();box.hidden=true;});box.appendChild(b);});
  }

  function render(){clampStep();renderTabs();renderHeader();renderMapVisual();renderQuick();renderProgress();renderStep();renderRecorder();renderFlow();renderNotes();}

  $('prevBtn').addEventListener('click',()=>{if(state.step>0)selectStep(state.step-1);});
  $('nextBtn').addEventListener('click',()=>{setDone(state.map,state.step,true);if(state.step<DATA[state.map].steps.length-1)state.step++;save();render();window.scrollTo({top:0,behavior:'smooth'});});
  $('doneBtn').addEventListener('click',()=>{setDone(state.map,state.step,!isDone(state.map,state.step));save();renderStep();renderFlow();renderProgress();renderMapVisual();});
  $('resetBtn').addEventListener('click',()=>{if(confirm(`清空“${DATA[state.map].name}”的完成进度？记事和记录器不会删除。`)){state.done[state.map]=[];state.step=0;save();render();}});
  $('notes').addEventListener('input',e=>{notes[state.map]=e.target.value;saveNotes();$('noteStatus').textContent='已保存';clearTimeout(window.__noteTimer);window.__noteTimer=setTimeout(()=>$('noteStatus').textContent='自动保存',900);});
  $('search').addEventListener('input',renderSearch);$('searchClear').addEventListener('click',()=>{$('search').value='';renderSearch();$('search').focus();});
  $('modalClose').addEventListener('click',closeVisual);$('visualModal').addEventListener('click',e=>{if(e.target===$('visualModal'))closeVisual();});

  safeLoad();render();
})();