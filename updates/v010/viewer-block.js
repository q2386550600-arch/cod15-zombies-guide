// v0.10: one viewer for both the filtered step gallery and full source gallery.
let viewerList=[],viewerPos=0,viewerFromGallery=false,galleryScroll=0,gesture=null;
const terms=Object.assign({},M.placeNames||{},window.IMAGE_HELP?.terms||{});
const termLookup=new Map(Object.entries(terms).map(([a,b])=>[a.toLowerCase(),b]));
const termRx=new RegExp('\\b('+Object.keys(terms).sort((a,b)=>b.length-a.length).map(x=>x.replace(/[.*+?^${}()|[\]\\]/g,'\\$&')).join('|')+')(?![A-Za-z])','gi');
if(typeof state.glossary!=='boolean')state.glossary=true;
function annotate(text){
 if(!state.glossary)return String(text||'');
 const seen=new Set();return String(text||'').replace(termRx,(match)=>{const k=match.toLowerCase();if(seen.has(k))return match;seen.add(k);return match+' ('+termLookup.get(k)+')';});
}
function imageHelp(im){
 const key=M.maps[state.map]?.guide;
 const rules=window.IMAGE_HELP?.notes?.[key]||[];
 const item=rules.find(n=>im.index>=n.first&&im.index<=n.last);
 return item||{action:'No verified action note is attached to this image. Refer to its source section before treating it as a required target.',branch:''};
}
function galleryCleanup(){document.querySelector('#viewerNav')?.remove();$('modal').classList.remove('imageMode');}
function openGallery(restore=false){
 const doc=guide();if(!doc){toast('此图暂无接入的社区主线图片。');return;}
 galleryCleanup();showModal('Image library · '+D[state.map].english,'gallery');
 const p=document.createElement('p');p.className='galleryIntro';
 p.textContent=`${doc.images.length} source images · Tap to inspect · Original image proportions preserved.`;
 $('modalBody').append(p);
 const groups=new Map();doc.images.forEach(im=>{if(!groups.has(im.last_heading))groups.set(im.last_heading,[]);groups.get(im.last_heading).push(im);});
 for(const [heading,imgs] of groups){
  const box=document.createElement('section');box.className='gallerySection';
  const title=document.createElement('h2');title.textContent=annotate(heading);box.append(title);
  const grid=document.createElement('div');grid.className='thumbGrid';
  imgs.forEach(im=>{const b=document.createElement('button');b.className='thumb';b.dataset.imageIndex=im.index;
   b.innerHTML=`<img loading="lazy" decoding="async" src="${esc(im.file)}" width="${im.width}" height="${im.height}" alt="${esc(im.caption)}"><span><small>#${im.index+1}</small><b>${esc(annotate(im.caption))}</b></span>`;
   b.onclick=()=>openImage(im,true);grid.append(b);
  });box.append(grid);$('modalBody').append(box);
 }
 if(restore===true){$('modalBody').scrollTop=galleryScroll;requestAnimationFrame(()=>$('modalBody').scrollTop=galleryScroll);}
}
function openImage(im,fromGallery=false){
 viewerFromGallery=fromGallery===true;
 if(viewerFromGallery)galleryScroll=$('modalBody').scrollTop;
 viewerList=viewerFromGallery?guide().images.slice():photos.filter(p=>!currentGroup||p.last_heading===currentGroup);
 viewerPos=viewerList.findIndex(p=>p.index===im.index);if(viewerPos<0){viewerList=[im];viewerPos=0;}
 galleryCleanup();showModal('Image viewer',viewerFromGallery?'image-gallery':'image');$('modal').classList.add('imageMode');
 $('modalBody').innerHTML=`<div class="viewerToolbar"><button id="zoomOut" aria-label="Zoom out">−</button><button id="zoomIn" aria-label="Zoom in">＋</button><button id="zoomFit">Fit / 适应</button><button id="glossaryToggle" aria-pressed="true">EN + 中文</button></div><div class="viewerPane" id="viewerPane"><img id="fullImage" alt=""><div id="imageLoadError" hidden>Image could not be decoded. Use Previous / Next or return to the gallery.</div></div><div class="imageInfo"><div class="imageMeta" id="imageMeta"></div><h2 id="fullPlace" class="imageTitle"></h2><div id="imageBranch" class="branchBadge" hidden></div><div id="branchWarning" class="notice" hidden></div><section class="imagePurpose"><h3>Purpose / Action <small>（用途／操作）</small></h3><p id="fullAction"></p></section><p id="fullCaption" class="caption"></p><details class="sourceDetails"><summary>Original caption &amp; source（原图注与来源）</summary><p id="originalCaption"></p><p id="provenance" class="footnote"></p></details><button id="imageBack" class="wide"></button></div>`;
 const footer=document.createElement('footer');footer.id='viewerNav';footer.className='viewerNav';
 footer.innerHTML='<button id="viewerPrev">‹ Previous<br><small>上一张</small></button><div><b id="viewerNumber" aria-live="polite"></b><small id="viewerScope"></small></div><button id="viewerNext">Next ›<br><small>下一张</small></button>';
 $('modal').append(footer);
 $('viewerPrev').onclick=()=>moveImage(-1);$('viewerNext').onclick=()=>moveImage(1);
 $('zoomIn').onclick=()=>applyZoom(Math.min(5,zoom+.5));$('zoomOut').onclick=()=>applyZoom(Math.max(1,zoom-.5));
 $('zoomFit').onclick=()=>applyZoom(1);
 $('glossaryToggle').onclick=()=>{state.glossary=!state.glossary;save();renderImageInfo();};
 $('fullImage').ondblclick=()=>applyZoom(zoom===1?2:1);
 $('fullImage').onerror=()=>{$('imageLoadError').hidden=false;};
 $('fullImage').onload=()=>{$('imageLoadError').hidden=true;};
 $('imageBack').onclick=closeImage;
 const pane=$('viewerPane');
 pane.addEventListener('touchstart',e=>{gesture=e.touches.length===1&&zoom===1?{x:e.touches[0].clientX,y:e.touches[0].clientY}:null;},{passive:true});
 pane.addEventListener('touchmove',e=>{if(e.touches.length!==1||zoom!==1){gesture=null;return;}if(gesture){const dx=e.touches[0].clientX-gesture.x,dy=e.touches[0].clientY-gesture.y;if(Math.abs(dx)>18&&Math.abs(dx)>Math.abs(dy)*1.4)e.preventDefault();}},{passive:false});
 pane.addEventListener('touchend',e=>{if(gesture&&e.changedTouches.length===1){const dx=e.changedTouches[0].clientX-gesture.x,dy=e.changedTouches[0].clientY-gesture.y;if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.4)moveImage(dx<0?1:-1);}gesture=null;},{passive:true});
 pane.addEventListener('touchcancel',()=>gesture=null,{passive:true});
 drawImage();
}
function applyZoom(n){zoom=n;const img=$('fullImage');if(!img)return;img.style.width=(n*100)+'%';$('zoomOut').disabled=n<=1;$('zoomIn').disabled=n>=5;if(n===1){$('viewerPane').scrollTop=0;$('viewerPane').scrollLeft=0;}}
function renderImageInfo(){
 const im=viewerList[viewerPos],help=imageHelp(im);currentImage=im;
 $('imageMeta').textContent=D[state.map].english+' · '+im.last_heading;
 $('fullPlace').textContent=annotate(im.caption);
 $('fullAction').textContent=annotate(help.action);
 $('fullCaption').textContent='Swipe left / right at Fit size to browse. Zoomed images pan without switching.（适应尺寸时滑动切图，放大后滑动查看细节。）';
 $('imageBranch').hidden=!help.branch;$('imageBranch').textContent=help.branch==='Both paths'?'Both paths（两条路线共用）':annotate(help.branch)+' path';
 const selected=state.branches[state.map]||'Richtofen';
 const different=branches.includes(state.map)&&['Maxis','Richtofen'].includes(help.branch)&&help.branch!==selected;
 $('branchWarning').hidden=!different;$('branchWarning').textContent=`This image belongs to the ${help.branch} path. Your selected tutorial is ${selected}.（此图路线与当前教程不同，请勿混用。）`;
 $('originalCaption').textContent=im.caption;
 $('provenance').textContent='COD Zombies Guides / PlagueFPS · '+guide().sourceFile+' · source line '+im.line+'\n'+im.source_path;
 $('glossaryToggle').textContent=state.glossary?'EN + 中文':'English';$('glossaryToggle').setAttribute('aria-pressed',String(state.glossary));
 $('imageBack').textContent=viewerFromGallery?'Back to image library（返回原位置）':'Back to this step（返回当前步骤）';
}
function drawImage(){
 const im=viewerList[viewerPos];if(!im)return;zoom=1;gesture=null;
 $('modalTitle').textContent=`Image ${viewerPos+1} / ${viewerList.length}`;
 $('fullImage').src=im.file;$('fullImage').alt=im.caption;$('fullImage').width=im.width;$('fullImage').height=im.height;
 $('imageLoadError').hidden=true;applyZoom(1);renderImageInfo();
 $('viewerPrev').disabled=viewerPos===0;$('viewerNext').disabled=viewerPos===viewerList.length-1;
 $('viewerNumber').textContent=(viewerPos+1)+' / '+viewerList.length;$('viewerScope').textContent=viewerFromGallery?'Full library（全图库）':'This stage（本阶段）';
 $('modalBody').scrollTop=0;
 if(!viewerFromGallery)photoIndex=viewerPos;
}
function moveImage(delta){const n=viewerPos+delta;if(n<0||n>=viewerList.length)return;viewerPos=n;drawImage();}
function closeImage(){const from=viewerFromGallery;galleryCleanup();if(from)openGallery(true);else{hideModal();renderPhoto();}}
function closeAnyModal(){if(['image','image-gallery'].includes(modalKind))closeImage();else{galleryCleanup();hideModal();}}
