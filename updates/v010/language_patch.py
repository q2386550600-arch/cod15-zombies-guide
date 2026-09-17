"""Add a persisted Chinese/English explanation toggle without replacing the v0.10 gallery or its source-image context."""
from pathlib import Path
P=Path('app/src/main/assets')
s=(P/'v010.js').read_text()
old='<button id="glossaryToggle" aria-pressed="true">EN + 中文</button>'
assert old in s
s=s.replace(old,old+'<button id="imageLanguage">中文</button>')
old=" $('glossaryToggle').onclick=()=>{state.glossary=!state.glossary;save();renderImageInfo();};"
assert old in s
s=s.replace(old,old+"\n $('imageLanguage').onclick=()=>{const language=read('cod-guide-image-language','en')==='en'?'zh':'en';try{localStorage.setItem('cod-guide-image-language',JSON.stringify(language));}catch(e){}renderImageInfo();};")
old=" $('fullAction').textContent=annotate(help.action);"
assert old in s
s=s.replace(old,old+"\n const lang=read('cod-guide-image-language','en');$('imageLanguage').textContent=lang==='en'?'中文':'English';if(lang==='zh'){const text=ImageHelp.info(state.map,im);$('fullPlace').textContent=text.titleZH;$('fullAction').textContent=text.taskZH;}")
(P/'v010.js').write_text(s)
p=P/'index.html';s=p.read_text()
old='<script src="image-help.js"></script>'
assert old in s
p.write_text(s.replace(old,old+'<script src="image-bilingual.js"></script><script src="image-goals.js"></script>'))
p=P/'v010.css';p.write_text(p.read_text()+'\n.viewerToolbar{display:flex;flex-wrap:wrap;gap:7px}.viewerToolbar button{min-width:44px;padding:9px 11px}.viewerToolbar #imageLanguage{color:var(--accent);margin-left:auto}\n')
print('Added an independent persistent EN/Chinese image-explanation toggle; English remains the default.')
