"""Gesture-only hotfix. Guide data and all media remain byte-identical."""
from pathlib import Path
import shutil
R=Path(__file__).resolve().parent
P=Path('app/src/main/assets');J=Path('app/src/main/java/com/openai/cod15guide')
s=(P/'v013.js').read_text()
a=s.index('function installFullPageSwipe(){');b=s.index('function pointPlans(',a)
s=s[:a]+(R/'gesture.js').read_text()+'\n'+s[b:]
s=s.replace("function galleryCleanup(){", "function galleryCleanup(){viewerPanMode=false;try{window.LocalViewerGesture?.setMode(false,false);}catch(e){}")
s=s.replace('<div class="viewerPane" id="viewerPane">','<button id="viewerTouchMode" type="button" aria-pressed="false" class="wide gestureMode">左右切图已开启 · 点此移动图片</button><div class="viewerPane" id="viewerPane">',1)
s=s.replace("$('imageBack').onclick=closeImage;", "$('imageBack').onclick=closeImage;$('viewerTouchMode').onclick=()=>{viewerPanMode=!viewerPanMode;syncViewerGestureMode();};")
s=s.replace('if(!im)return;zoom=1;gesture=null;', 'if(!im)return;viewerPanMode=false;zoom=1;gesture=null;')
s=s.replace('applyZoom(1);renderImageInfo();','applyZoom(1);renderImageInfo();syncViewerGestureMode();')
s=s.replace('renderImageInfo();};','renderImageInfo();syncViewerGestureMode();};')
(P/'v0131.js').write_text(s)
css=(P/'v013.css').read_text()+'''
#modal.imageMode{touch-action:pan-y}#modal.imageMode .viewerPane{overflow-x:hidden;touch-action:pan-y}#modal.imageMode .viewerPane img{touch-action:pan-y;user-select:none;-webkit-user-drag:none}#modal.imageMode .imageInfo{touch-action:pan-y}#modal.imageMode.imagePanMode{touch-action:pan-x pan-y}#modal.imageMode.imagePanMode .viewerPane{overflow:auto;touch-action:pan-x pan-y}#modal.imageMode.imagePanMode .viewerPane img{touch-action:pan-x pan-y}.gestureMode{margin:0 0 10px;font-size:13px;color:var(--accent)}.gestureMode[aria-pressed=true]{border-color:var(--accent)}
'''
(P/'v0131.css').write_text(css)
f=P/'index.html';h=f.read_text().replace('v013.js','v0131.js').replace('v013.css','v0131.css').replace('v0.13 · 详细教程版','v0.13.1 · 手势修复');f.write_text(h)
j=(J/'MainActivity.java').read_text().replace('FrameLayout root = new FrameLayout(this);','ViewerGestureLayout root = new ViewerGestureLayout(this);').replace('settings.setBuiltInZoomControls(true);','settings.setSupportZoom(false);\n        settings.setBuiltInZoomControls(false);').replace('webView.setWebChromeClient(new WebChromeClient());','root.attach(webView);\n        webView.setWebChromeClient(new WebChromeClient());')
(J/'MainActivity.java').write_text(j);shutil.copyfile(R/'ViewerGestureLayout.java',J/'ViewerGestureLayout.java')
f=Path('app/build.gradle');g=f.read_text().replace('versionCode 13','versionCode 14').replace("versionName '0.13'","versionName '0.13.1'");f.write_text(g)
print('Applied gesture-only patch; content JSON, media, descriptions and progress keys unchanged.')
