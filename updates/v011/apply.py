from pathlib import Path
import subprocess
P=Path('app/src/main/assets');U=Path('updates/v011')
subprocess.run(['node',str(U/'export_locale.mjs')],check=True)
(P/'zh-display.js').write_text((U/'zh-display.js').read_text())
s=(P/'v010.js').read_text()
def swap(old,new):
 global s
 if old not in s:raise ValueError('Missing patch marker: '+old[:100])
 s=s.replace(old,new)
swap("let mode='overview'", "if(state.chineseDefaultRevision!==11){state.chineseDefaultRevision=11;state.showEnglishNames=true;}\nconst zh=s=>ZhDisplay.text(s,state.showEnglishNames!==false);\nconst imgZH=p=>ZhDisplay.info(state.map,p,state.showEnglishNames!==false);\nlet mode='overview'")
swap("$('photoLocation').textContent=annotate(p.caption);$('photoCaption').textContent=annotate(imageHelp(p).action);", "$('photoLocation').textContent=imgZH(p).title;$('photoCaption').textContent=imgZH(p).action;")
swap("showModal('Image library · '+D[state.map].english,'gallery')", "showModal('完整图片库 · '+D[state.map].name,'gallery')")
swap('`${doc.images.length} source images · Tap to inspect · Original image proportions preserved.`', '`共 ${doc.images.length} 张来源配图 · 点击查看位置和操作 · 保留原图比例`')
swap('title.textContent=annotate(heading)', 'title.textContent=ZhDisplay.heading(heading)')
swap('${esc(annotate(im.caption))}', '${esc(imgZH(im).title)}')
swap("showModal('Image viewer'", "showModal('图片详情'")
swap('aria-label="Zoom out"','aria-label="缩小图片"');swap('aria-label="Zoom in"','aria-label="放大图片"')
swap('>Fit / 适应<','>适应宽度<');swap('>EN + 中文<','>英文名称：开<')
swap('<button id="imageLanguage">中文</button>','')
swap('Image could not be decoded. Use Previous / Next or return to the gallery.','图片暂时无法读取，可切换上一张、下一张，或返回图库。')
swap('<h2 id="fullPlace" class="imageTitle"></h2>', '<h2 id="fullPlace" class="imageTitle"></h2><p id="imageWhere" class="photoLocation"></p>')
swap('Purpose / Action <small>（用途／操作）</small>','这张图要做什么')
swap('Original caption &amp; source（原图注与来源）','查看英文原图注与来源')
swap('‹ Previous<br><small>上一张</small>','‹ 上一张');swap('Next ›<br><small>下一张</small>','下一张 ›')
swap("$('glossaryToggle').onclick=()=>{state.glossary=!state.glossary;save();renderImageInfo();};", "$('glossaryToggle').onclick=()=>{state.showEnglishNames=state.showEnglishNames===false;save();renderImageInfo();};")
a=s.index(" $('imageLanguage').onclick=");b=s.index('\n',a);s=s[:a]+s[b:]
a=s.index('function renderImageInfo(){');b=s.index('function drawImage(){',a)
s=s[:a]+'''function renderImageInfo(){
 const im=viewerList[viewerPos],help=imageHelp(im),cn=imgZH(im);currentImage=im;
 $('imageMeta').textContent=D[state.map].name+' · '+cn.heading;
 $('fullPlace').textContent=cn.title;
 $('imageWhere').textContent='位置：'+cn.where;$('imageWhere').hidden=cn.where===cn.title;
 $('fullAction').textContent=cn.action;
 $('fullCaption').textContent='适应宽度时左右滑动切图；放大后滑动查看细节，底部按钮仍可切图。';
 $('imageBranch').hidden=!help.branch;$('imageBranch').textContent=help.branch==='Both paths'?'两条路线共用':zh(help.branch)+'路线';
 const selected=state.branches[state.map]||'Richtofen';
 $('branchWarning').hidden=!(branches.includes(state.map)&&['Maxis','Richtofen'].includes(help.branch)&&help.branch!==selected);
 $('branchWarning').textContent='本图属于'+zh(help.branch)+'路线；当前教程为'+zh(selected)+'路线，请勿混用。';
 $('originalCaption').textContent=im.caption;
 $('provenance').textContent='原作者：COD Zombies Guides / PlagueFPS · '+guide().sourceFile+' · 原文第 '+im.line+' 行\\n'+im.source_path;
 $('glossaryToggle').textContent=state.showEnglishNames===false?'英文名称：关':'英文名称：开';$('glossaryToggle').setAttribute('aria-pressed',String(state.showEnglishNames!==false));
 $('imageBack').textContent=viewerFromGallery?'返回图片库原位置':'返回当前步骤';
}
''' +s[b:]
swap('`Image ${viewerPos+1} / ${viewerList.length}`','`图片 ${viewerPos+1} / ${viewerList.length}`')
swap("'Full library（全图库）':'This stage（本阶段）'","'完整图片库':'当前阶段'")
swap("$('stageLabel').textContent=branches.includes(state.map)?'当前路线 · '+(state.branches[state.map]||'Richtofen')", "$('stageLabel').textContent=branches.includes(state.map)?'当前路线 · '+zh(state.branches[state.map]||'Richtofen')")
swap("$('stepTitle').textContent=s.title", "$('stepTitle').textContent=zh(s.title)")
swap("$('stepPlace').textContent='去这里：'+s.place", "$('stepPlace').textContent='去这里：'+zh(s.place)")
swap("$('stepSuccess').textContent=s.success", "$('stepSuccess').textContent=zh(s.success)")
swap("$('stepTips').textContent=s.tips||", "$('stepTips').textContent=zh(s.tips)||")
swap('`<p>${esc(x)}</p>`','`<p>${esc(zh(x))}</p>`')
swap('${esc(s.title)}</b><small>${esc(s.place)}', '${esc(zh(s.title))}</b><small>${esc(zh(s.place))}')
swap('分组 ${i+1} · ${esc(s)}', '分组 ${i+1} · ${esc(ZhDisplay.heading(s))}')
(P/'v011.js').write_text(s)
s=(P/'index.html').read_text().replace('v0.10 · 图片修复版','v0.11 · 中文主导版').replace('<script src="v010.js"></script>','<script src="zh-locale.js"></script><script src="zh-display.js"></script><script src="v011.js"></script>')
(P/'index.html').write_text(s)
p=Path('app/build.gradle');s=p.read_text().replace('versionCode 10','versionCode 11').replace("versionName '0.10'","versionName '0.11'");p.write_text(s)
print('Chinese-first display applied. Source images, raw English captions and user-progress key preserved.')
