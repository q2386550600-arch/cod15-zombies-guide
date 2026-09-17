from pathlib import Path
import base64, hashlib, lzma
ROOT=Path(__file__).resolve().parent
P=Path('app/src/main/assets')
def replace(s,old,new):
    if old not in s:raise ValueError('Expected source marker is missing: '+old[:100])
    return s.replace(old,new)
blob=lzma.decompress(base64.b64decode(''.join((ROOT/f'image-help.xz.b64.part{i}').read_text().strip() for i in (1,2))))
assert hashlib.sha256(blob).hexdigest()=='7f51fbfe249f51ad5844a13240d5ef9b9c3a521d88113e1f08a656d1077fe14f','Image help transfer integrity failure'
(P/'image-help.js').write_bytes(blob)
s=(P/'v09.js').read_text()
a=s.index('function openGallery(');b=s.index('const REC=',a)
s=s[:a]+(ROOT/'viewer-block.js').read_text()+'\n'+s[b:]
s=replace(s,"$('photoLocation').textContent=photoLabel(p);$('photoCaption').textContent='原作者图注：'+p.caption;", "$('photoLocation').textContent=annotate(p.caption);$('photoCaption').textContent=annotate(imageHelp(p).action);")
s=replace(s,"$('closeModal').onclick=()=>modalKind==='image-gallery'?openGallery():hideModal();", "$('closeModal').onclick=closeAnyModal;")
s=replace(s,"if(modalKind==='image-gallery')openGallery();else hideModal();return true;", "closeAnyModal();return true;")
s=replace(s,"document.addEventListener('keydown',e=>{if(e.key==='Escape')window.guideBack();});", "document.addEventListener('keydown',e=>{if(e.key==='Escape')window.guideBack();else if(['image','image-gallery'].includes(modalKind)&&['ArrowLeft','ArrowRight'].includes(e.key)){e.preventDefault();moveImage(e.key==='ArrowLeft'?-1:1);}});")
s=replace(s,"function hideModal(){$('modal').hidden=true;", "function hideModal(){galleryCleanup();$('modal').hidden=true;")
s=replace(s,"media:()=>M,currentPhotos:()=>photos", "media:()=>M,currentPhotos:()=>photos,imageHelp:(p)=>imageHelp(p),viewer:()=>({index:viewerPos,count:viewerList.length,zoom,fromGallery:viewerFromGallery}),moveImage")
(P/'v010.js').write_text(s)
css=(P/'v09.css').read_text()
css=replace(css,'.thumbGrid{display:grid;grid-template-columns:1fr 1fr;', '.thumbGrid{display:grid;grid-template-columns:minmax(0,1fr) minmax(0,1fr);align-items:start;')
css=replace(css,'.thumb{display:block;width:100%;', '.thumb{display:flex;flex-direction:column;justify-content:flex-start;align-self:start;min-width:0;min-height:0;width:100%;')
css=replace(css,'.thumb img{display:block;width:100%;aspect-ratio:16/9;', '.thumb img{display:block;width:100%;height:auto;aspect-ratio:auto;min-height:0;flex:none;')
css=replace(css,'height:auto;aspect-ratio:16/9;', 'height:auto;aspect-ratio:auto;')
css+='''
/* Auto height overrides the original HTML pixel-height attribute without cropping. */
.thumb span{width:100%;padding:9px;min-width:0}.thumb span b{display:-webkit-box;-webkit-line-clamp:4;-webkit-box-orient:vertical;overflow:hidden;font-size:12px;line-height:1.5;font-weight:550}.thumb small{display:block;color:var(--accent);font-size:10px;margin-bottom:4px}
.gallerySection{margin:16px 0 22px}.gallerySection h2{font-size:14px;line-height:1.5;color:#cad4e2}.galleryIntro{font-size:12px;line-height:1.5;margin:0 0 15px;color:var(--dim)}
#modal.imageMode #modalBody{padding:12px 14px 20px;max-width:900px}#modal.imageMode .modalHead{flex:none}#modal.imageMode .modalHead b{font-size:16px}.viewerToolbar{gap:7px;margin-bottom:10px;display:grid;grid-template-columns:44px 44px 1fr 1.2fr}.viewerToolbar button{font-size:13px;min-width:0;padding:8px 5px}.viewerPane{position:relative;max-height:52vh;max-height:52dvh;min-height:0;width:100%;overflow:auto;border-radius:10px;overscroll-behavior:contain;background:#080b0f}.viewerPane img{height:auto;aspect-ratio:auto;display:block;min-height:0;width:100%;max-width:none;touch-action:pan-x pan-y pinch-zoom}.imageInfo{padding:14px 2px 0}.imageMeta{color:var(--dim);font-size:11px;line-height:1.5;margin:0 0 6px}.imageTitle{font-size:19px;line-height:1.5;color:var(--accent);margin:0 0 10px}.imagePurpose{margin:14px 0 10px;padding:13px;background:var(--card);border-radius:12px}.imagePurpose h3{font-size:13px;margin:0;color:var(--dim);font-weight:600}.imagePurpose h3 small{font-size:11px}.imagePurpose p{font-size:15px;line-height:1.75;margin:6px 0 0}.branchBadge{display:inline-block;border:1px solid #566c83;border-radius:7px;padding:4px 7px;font-size:12px;color:#cddbec;margin:0 0 5px}.sourceDetails{border-top:1px solid var(--line);padding-top:11px;margin-top:14px}.sourceDetails summary{font-size:12px;font-weight:450;color:var(--dim)}.sourceDetails p{font-size:12px;overflow-wrap:anywhere;white-space:pre-line}.sourceDetails .footnote{margin-top:7px}.viewerNav{flex:none;display:grid;grid-template-columns:1fr 1fr 1fr;align-items:center;gap:8px;background:var(--bg);border-top:1px solid var(--line);padding:9px 14px max(11px,env(safe-area-inset-bottom));z-index:110}.viewerNav button{line-height:1.25;font-size:14px;padding:8px 4px;min-height:48px}.viewerNav button small{font-size:10px}.viewerNav>div{text-align:center}.viewerNav b{display:block;font-size:15px}.viewerNav>div small{display:block;font-size:10px;margin-top:4px}#imageLoadError{padding:18px;font-size:14px;color:#ffc2c2}.modalHead{flex:none}.photoLocation{line-height:1.6}.caption{overflow-wrap:anywhere}
'''
(P/'v010.css').write_text(css)
s=(P/'index.html').read_text()
s=replace(s,'v0.9 · 实机图版','v0.10 · 图片修复版')
s=replace(s,'href="v09.css"','href="v010.css"')
s=replace(s,'<script src="v09.js"></script>','<script src="image-help.js"></script><script src="v010.js"></script>')
(P/'index.html').write_text(s)
f=Path('app/build.gradle');s=f.read_text();s=replace(s,'versionCode 9','versionCode 10');s=replace(s,"versionName '0.9'","versionName '0.10'");f.write_text(s)
print('Applied v0.10; existing application ID, signing configuration and localStorage key preserved.')
