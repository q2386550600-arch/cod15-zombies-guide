// Offline procedures: source links are optional verification, never a substitute for text.
const OFF=window.OFFLINE_GUIDES;
const offlineDoc=()=>OFF.docs[sourceDoc()?.guide]||null;
function bookSections(){return Object.values(offlineDoc()?.sections||{}).filter(s=>s.texts.length||s.kind==='group');}
function sectionFacts(sec){return offlineDoc()?.sections[sec.id]?.texts||[];}
function sourceCoverageNotice(){return '本地为中文操作教程，按来源章节关联制作、随机点位、主线与失败重试。正文离线可读；原链接仅供查证。不是原作者文章逐字译本，推荐配置表、剧情介绍和视频不冒充必做步骤。原版与复刻版条件以当前作品提示为准。';}
function renderNavigation(){const src=offlineDoc(),m=plansForMap();$('atlasOverview').textContent=m.length?`地图与楼层定位 · ${m.length}张`:'地图与楼层定位 / 来源';$('sourceOverview').textContent='详细中文攻略（离线正文／前置制作）';$('sourceOverview').disabled=!src;$('sourceStep').textContent='详细中文攻略与制作目录';$('sourceNote').textContent=src?`本图含 ${src.paragraphs} 项中文操作／点位说明，按章节离线阅读。开始解密后按具体细项推进；需要选择的弓或随机挑战可在当前阶段切换。`:'此图保留生存／支线说明；没有传统主线的地图不编造解谜流程。';renderTeamMode();}
function renderStepExtras(){const box=$('stepDetails');box.hidden=true;box.innerHTML='';const r=$('routeActions');r.innerHTML='';const b=document.createElement('button');b.textContent='地图／楼层';b.onclick=()=>openAtlas(false);r.append(b);$('sourceStep').disabled=!offlineDoc();const p=$('pointList');p.innerHTML='';$('pointListWrap').hidden=!photos.length;photos.forEach(im=>{const a=document.createElement('article');a.innerHTML=positionMarkup(im);p.append(a);});}
function showSourceIndex(){
 const doc=offlineDoc();if(!doc){toast('此图暂无已关联的主线正文。');return;}
 galleryCleanup();showModal('详细中文攻略 · '+D[state.map].name,'sources');
 const p=document.createElement('p');p.className='notice';p.textContent=sourceCoverageNotice();$('modalBody').append(p);
 const input=document.createElement('input');input.type='search';input.placeholder='查找制作、机关、挑战或关键词';input.setAttribute('aria-label','搜索详细攻略');$('modalBody').append(input);
 const list=document.createElement('div');list.className='bookList';$('modalBody').append(list);
 const render=()=>{list.innerHTML='';const q=input.value.trim().toLowerCase();for(const s of bookSections()){if(q&&!`${ZhDisplay.heading(s.heading)} ${s.heading} ${s.texts.join(' ')}`.toLowerCase().includes(q))continue;const b=document.createElement('button');b.className='sourceChapter';b.dataset.sectionId=s.id;b.innerHTML=`<b>${esc(ZhDisplay.heading(s.heading))}</b><small>${s.texts.length?'正文 '+s.texts.length+' 项':'分组目录'} · ${s.images.length} 张配图</small>`;b.onclick=()=>openSourceSection(s.id);list.append(b);}};input.oninput=render;render();
 if(state.map==='bo3_gorod'){const b=document.createElement('button');b.className='wide';b.textContent='离线阀门计算器';b.onclick=openValve;list.prepend(b);}
 const detail=document.createElement('details');detail.className='card';detail.innerHTML='<summary>来源核对与参考资料</summary>'+externalLink(sourceDoc().url,'核对原作者网页（联网）')+'<p>保留原有社区配图；正文用中文重新说明操作。配置推荐、视频与鸣谢不计入主线操作条数。</p>';$('modalBody').append(detail);
}
function openSourceSection(id){
 const doc=offlineDoc(),sec=doc?.sections[id];if(!sec)return;galleryCleanup();activeSourceSection=id;showModal(ZhDisplay.heading(sec.heading),'source-section');
 const tools=document.createElement('div');tools.className='readerTools';tools.innerHTML='<button id="readerIndex">全部章节</button><button id="readerCurrent">返回当前步骤</button>';$('modalBody').append(tools);$('readerIndex').onclick=showSourceIndex;$('readerCurrent').onclick=hideModal;
 if(sec.texts.length){const ol=document.createElement('ol');ol.className='actionList completeText';for(const t of sec.texts){const li=document.createElement('li');li.textContent=zh(t);ol.append(li);}$('modalBody').append(ol);}
 const children=Object.values(doc.sections).filter(s=>s.parent===id&&(s.texts.length||s.kind==='group'));
 if(children.length){const h=document.createElement('h2');h.textContent='制作／候选位置子章节';$('modalBody').append(h);for(const s of children){const b=document.createElement('button');b.className='detailJump';b.textContent=ZhDisplay.heading(s.heading)+' · '+s.texts.length+'项';b.onclick=()=>openSourceSection(s.id);$('modalBody').append(b);}}
 if(!sec.texts.length&&!children.length){const p=document.createElement('p');p.textContent='此条为目录或参考信息，不是额外必做机关。';$('modalBody').append(p);}
 if(id==='love-and-war-5'){const b=document.createElement('button');b.className='primary wide';b.textContent='打开离线阀门计算器';b.onclick=openValve;$('modalBody').append(b);}
 const ims=(guide()?.images||[]).filter(p=>sec.images.includes(p.index));
 ims.forEach(im=>{const c=document.createElement('article');c.className='sourcePoint';c.innerHTML=positionMarkup(im)+`<img src="${esc(im.file)}" loading="lazy" width="${im.width}" height="${im.height}" alt="${esc(im.caption)}">`;c.querySelector('img').onclick=()=>{openImage(im,true);viewerSection=id;viewerAtlas=false;viewerList=ims.slice();viewerPos=ims.findIndex(p=>p.index===im.index);drawImage();};$('modalBody').append(c);});
 const visible=bookSections(),n=visible.findIndex(s=>s.id===id),nav=document.createElement('div');nav.className='readerTools';
 for(const [label,offset] of [['上一节',-1],['下一节',1]]){const b=document.createElement('button');b.textContent=label;b.disabled=n+offset<0||n+offset>=visible.length;b.onclick=()=>openSourceSection(visible[n+offset].id);nav.append(b);}$('modalBody').append(nav);
 const provenance=document.createElement('details');provenance.className='sourceDetails';provenance.innerHTML='<summary>查证来源（无需打开才能读正文）</summary>'+(sec.extraSources||[sourceLink(sec)]).filter(Boolean).map(u=>externalLink(u,'查看社区来源')).join('');$('modalBody').append(provenance);
}
const valvePlaces={'Armory':'军械库','Infirmary':'医务室','Department Store':'百货商店','Supply Depot':'补给站','Dragon Command':'龙指挥部','Tank Factory':'坦克工厂'};
function openValve(){
 showModal('血色城堡 · 离线阀门计算器','valve');const b=$('modalBody');
 b.innerHTML='<p class="notice">本局绿灯阀门为起点，带粉色圆筒且有哨声的阀门为终点。两处必须不同。只设置其余五阀，粉色圆筒阀不用转；五分钟到期先回孵化场重启发电机。</p><label class="recordField"><span>绿灯阀门</span><select id="valveFrom"></select></label><label class="recordField"><span>粉色圆筒阀门</span><select id="valveTo"></select></label><div id="valveAnswer" aria-live="polite"></div><button id="valveBack" class="wide">返回阀门教程</button>';
 const opts='<option value="">请选择本局位置</option>'+Object.entries(valvePlaces).map(([en,cn])=>`<option value="${en}">${cn}（${en}）</option>`).join('');$('valveFrom').innerHTML=opts;$('valveTo').innerHTML=opts;
 $('valveFrom').value=state.rec.bo3_gorod.valveFrom||'';$('valveTo').value=state.rec.bo3_gorod.valveTo||'';
 const update=()=>{const from=$('valveFrom').value,to=$('valveTo').value;state.rec.bo3_gorod.valveFrom=from;state.rec.bo3_gorod.valveTo=to;save();const out=$('valveAnswer');out.innerHTML='';if(!from||!to){out.textContent='选好起点与终点后显示五个阀门数值。';return;}if(from===to){out.textContent='起点与终点不能是同一处，重新检查本局绿灯和粉色圆筒。';return;}const route=OFF.valves[from+' to '+to];if(!route){out.textContent='没有匹配组合，未显示猜测数值。';return;}for(const [en,cn]of Object.entries(valvePlaces)){const p=document.createElement('p');p.className='valveRow';p.innerHTML=`<span>${cn}</span><b>${route[en]===null?'不要转动（圆筒）':route[en]}</b>`;out.append(p);}};
 $('valveFrom').onchange=update;$('valveTo').onchange=update;$('valveBack').onclick=()=>openSourceSection('love-and-war-5');update();
}
