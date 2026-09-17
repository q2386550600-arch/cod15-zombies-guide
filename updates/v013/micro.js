// Keep v0.12 macro-step identifiers so older progress and notes stay valid.
if(!state.detailPositions||typeof state.detailPositions!=='object')state.detailPositions={};
if(!state.detailChoices||typeof state.detailChoices!=='object')state.detailChoices={};
if(!state.detailCompletedChoices||typeof state.detailCompletedChoices!=='object')state.detailCompletedChoices={};
function completedChoices(){return state.detailCompletedChoices[stageKey()]||[];}
function stageKey(){return state.map+':'+state.step;}
function stageSpec(){return OFF.stages[state.map]?.[state.step]||null;}
function detailFrames(){const s=stageSpec();if(!s)return[];const choice=Number(state.detailChoices[stageKey()]);return s.frames.concat(Number.isInteger(choice)&&s.choices[choice]?s.choices[choice].frames:[]);}
function detailPos(){const max=detailFrames().length-1;return Math.max(0,Math.min(Number(state.detailPositions[stageKey()])||0,max));}
function currentFrame(){return detailFrames()[detailPos()]||null;}
function stepPhotos(){const doc=guide(),frame=currentFrame();if(frame)return doc?.images.filter(p=>frame.images.includes(p.index))||[];return legacyStepPhotos();}
function renderTeamMode(){
 let box=$('partyMode');if(!box){box=document.createElement('label');box.id='partyMode';box.className='recordField';box.innerHTML='<span>亡者召唤：选择对局人数</span><select id="cotdMode"><option value="coop">合作（两人或以上）</option><option value="solo">单人（替身演员路线）</option></select>';$('requirements').after(box);}
 box.hidden=state.map!=='bo1_cotd';$('cotdMode').value=state.cotdMode||'coop';$('cotdMode').onchange=e=>{state.cotdMode=e.target.value;clamp();save();renderOverview();};
}
function renderStep(){
 legacyRenderStep();const f=currentFrame(),list=detailFrames(),pos=detailPos(),spec=stageSpec();
 $('detailControls')?.remove();$('detailJumpMenu')?.remove();if(!f)return;
 const colon=f.text.indexOf('：'),title=colon>0&&colon<45?f.text.slice(0,colon):'当前细项';
 $('stageLabel').textContent='第 '+(active().indexOf(state.step)+1)+' 阶段 · '+zh(D[state.map].steps[state.step].title);
 $('stepNo').textContent='细项 '+(pos+1)+' / '+list.length+' · 第 '+(active().indexOf(state.step)+1)+' / '+active().length+' 阶段';
 $('stepTitle').textContent=title;$('stepPlace').textContent='本节：'+ZhDisplay.heading(offlineDoc()?.sections[f.section]?.heading||'');
 $('stepAction').innerHTML='<p>'+esc(zh(colon>0&&colon<45?f.text.slice(colon+1):f.text))+'</p>';
 $('prev').disabled=pos===0&&active().indexOf(state.step)===0;
 if(spec.mustCompleteAll){$('toggleDone').hidden=!isDone(state.step);}else{$('toggleDone').hidden=false;}
 const needsChoice=spec.choices.length&&!Number.isInteger(state.detailChoices[stageKey()]);
 $('next').textContent=pos<list.length-1?'下一项 →':needsChoice?'先选择本局任务':active().indexOf(state.step)===active().length-1?'标记路线完成':'完成本阶段 →';
 $('next').disabled=!!needsChoice&&pos===list.length-1;
 $('stepSuccess').closest('section').hidden=pos<list.length-1||(spec.mustCompleteAll&&completedChoices().length<spec.choices.length);
 if(spec.mustCompleteAll&&!needsChoice&&pos===list.length-1)$('next').textContent='确认本项挑战完成';
 const controls=document.createElement('section');controls.id='detailControls';controls.className='detailControls';
 const buttons=document.createElement('div');buttons.className='readerTools';
 const full=document.createElement('button');full.textContent='本节全部操作／候选点';full.onclick=()=>openSourceSection(f.section);buttons.append(full);
 const jump=document.createElement('button');jump.textContent='跳到细项 '+(pos+1)+'/'+list.length;jump.onclick=openDetailIndex;buttons.append(jump);controls.append(buttons);
 if(spec.choices.length){const label=document.createElement('label');label.className='recordField';label.innerHTML='<span>'+esc(spec.choiceTitle)+'</span><select id="detailChoice"><option value="">请选择，不预设随机结果</option>'+spec.choices.map((o,i)=>`<option value="${i}">${completedChoices().includes(i)?'✓ ':''}${esc(o.title)}</option>`).join('')+'</select>';controls.append(label);}
 if(state.map==='bo3_gorod'&&f.section==='love-and-war-5'){const b=document.createElement('button');b.className='primary wide';b.textContent='本局阀门数值（离线计算）';b.onclick=openValve;controls.append(b);}
 $('stepAction').closest('section').after(controls);
 if(spec.choices.length){$('detailChoice').value=Number.isInteger(state.detailChoices[stageKey()])?String(state.detailChoices[stageKey()]):'';$('detailChoice').onchange=e=>{if(e.target.value==='')delete state.detailChoices[stageKey()];else state.detailChoices[stageKey()]=Number(e.target.value);state.detailPositions[stageKey()]=spec.frames.length;save();renderStep();};}
 $('toggleDone').textContent=isDone(state.step)?'✓ 本阶段已标记完成 · 点击撤销':'手动标记整个阶段完成（不是下一细项）';
 $('tutorialBody').scrollTop=0;requestAnimationFrame(()=>$('tutorialBody').scrollTop=0);
}
function openDetailIndex(){
 const list=detailFrames();showModal('本阶段细项目录','detail-index');list.forEach((f,i)=>{const b=document.createElement('button');b.className='detailJump';b.textContent=(i+1)+' · '+f.text.split('：')[0];b.onclick=()=>{state.detailPositions[stageKey()]=i;save();hideModal();renderStep();};$('modalBody').append(b);});
}
function next(){const list=detailFrames(),pos=detailPos();if(list.length&&pos<list.length-1){state.detailPositions[stageKey()]=pos+1;save();renderStep();return;}const spec=stageSpec();if(spec?.choices.length&&!Number.isInteger(state.detailChoices[stageKey()])){toast('先选择本局的弓／随机挑战。');return;}if(spec?.mustCompleteAll){const c=state.detailChoices[stageKey()];state.detailCompletedChoices[stageKey()]=[...new Set([...completedChoices(),c])];if(completedChoices().length<spec.choices.length){delete state.detailChoices[stageKey()];state.detailPositions[stageKey()]=0;save();renderStep();toast('已记录该项完成，请按新的光束选择下一挑战。');return;}}const a=active(),n=a.indexOf(state.step);setDone(state.step,true);if(n<a.length-1){state.step=a[n+1];state.detailPositions[stageKey()]=0;}save();renderStep();}
function prev(){const pos=detailPos();if(pos>0){state.detailPositions[stageKey()]=pos-1;save();renderStep();return;}const a=active(),n=a.indexOf(state.step);if(n>0){state.step=a[n-1];state.detailPositions[stageKey()]=Math.max(0,detailFrames().length-1);save();renderStep();}}
