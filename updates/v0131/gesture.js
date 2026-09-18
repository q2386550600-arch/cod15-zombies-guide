// Browse mode pages horizontally even at zoom > 1. Panning is explicitly selected.
let viewerPanMode=false;
function syncViewerGestureMode(){
 const host=$('modal'),active=!host.hidden&&host.classList.contains('imageMode');
 host.classList.toggle('imagePanMode',active&&viewerPanMode);
 const button=$('viewerTouchMode');
 if(button){button.textContent=viewerPanMode?'正在移动图片 · 点此恢复左右切图':'左右切图已开启 · 点此移动图片';button.setAttribute('aria-pressed',String(viewerPanMode));}
 if(active&&$('fullCaption'))$('fullCaption').textContent=viewerPanMode?'当前为移动图片：拖动可查看放大细节。点上方按钮恢复整页左右切图；底部翻图按钮始终可用。':'当前为左右切图：图片、文字、空白处均可单指横滑，放大后也一样。上下滑动阅读；要移动图片局部，请点“移动图片”。';
 try{window.LocalViewerGesture?.setMode(active,viewerPanMode);}catch(e){console.warn('Viewer gesture bridge unavailable',e);}
}
function installFullPageSwipe(){
 const host=$('modal'),native=!!window.LocalViewerGesture&&typeof window.LocalViewerGesture.setMode==='function';
 window.guideGestureBackend=native?'android':'pointer';
 window.guideViewerSwipe=delta=>{if(host.hidden||!host.classList.contains('imageMode')||viewerPanMode||![-1,1].includes(delta))return false;const before=viewerPos;moveImage(delta);return viewerPos!==before;};
 new MutationObserver(syncViewerGestureMode).observe(host,{attributes:true,attributeFilter:['hidden','class']});
 if(native)return;
 let start=null,blockClickUntil=0;const pointers=new Set();
 host.addEventListener('pointerdown',e=>{pointers.add(e.pointerId);if(pointers.size!==1||host.hidden||!host.classList.contains('imageMode')||viewerPanMode||e.button>0){start=null;return;}if(e.target.closest('input,textarea,select,[contenteditable=true]')){start=null;return;}start={id:e.pointerId,x:e.clientX,y:e.clientY,time:performance.now(),horizontal:false};});
 host.addEventListener('pointermove',e=>{if(!start||start.id!==e.pointerId||viewerPanMode)return;const dx=e.clientX-start.x,dy=e.clientY-start.y;if(!start.horizontal&&Math.abs(dy)>12&&Math.abs(dy)>Math.abs(dx)*1.15){start=null;return;}if(Math.abs(dx)>12&&Math.abs(dx)>Math.abs(dy)*1.25){start.horizontal=true;if(e.cancelable)e.preventDefault();}},{passive:false});
 host.addEventListener('pointerup',e=>{pointers.delete(e.pointerId);const s=start;start=null;if(!s||s.id!==e.pointerId)return;const dx=e.clientX-s.x,dy=e.clientY-s.y,dt=performance.now()-s.time;if((Math.abs(dx)>=44||(dt<280&&Math.abs(dx)>=24))&&Math.abs(dx)>Math.abs(dy)*1.25){blockClickUntil=performance.now()+400;window.guideViewerSwipe(dx<0?1:-1);}});
 host.addEventListener('pointercancel',e=>{pointers.delete(e.pointerId);start=null;});
 host.addEventListener('click',e=>{if(performance.now()<blockClickUntil){e.preventDefault();e.stopImmediatePropagation();}},{capture:true});
}
