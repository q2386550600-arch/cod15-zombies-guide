"""Verify retained assets and package self-contained, non-secret deliverables."""
import hashlib, html, json, re, zipfile
from pathlib import Path

A=Path('app/src/main/assets');O=Path('output');O.mkdir(exist_ok=True)
apk=O/'COD_Zombies_Guide_v0.14.1.apk';previous=Path('.previous/COD_Zombies_Guide_v0.14.0-preview3.apk')
with zipfile.ZipFile(previous) as old,zipfile.ZipFile(apk) as new:
    assert new.testzip() is None
    changed={'assets/index.html','assets/entry-faithful.js','assets/faithful.html','assets/faithful.js','assets/faithful.css'}
    retained=[n for n in old.namelist() if n.startswith('assets/') and not n.endswith('/') and not n.startswith('assets/faithful/') and n not in changed]
    assert all(old.read(n)==new.read(n) for n in retained),'A legacy asset changed unexpectedly'
    images=[n for n in retained if n.startswith(('assets/images/','assets/atlas/'))]
    assert len(images)==1282,(len(images),'Expected 1148 source screenshots + 134 floor maps')
    for n in old.namelist():
        if re.fullmatch(r'assets/faithful/p\d+\.js',n):
            def parse(b):
                s=b.decode();return json.loads(s[s.index('(')+1:s.rfind(')')])
            x=parse(old.read(n));y=parse(new.read(n))
            for k in ['metadata','tree','images','headings','sourceUnitDigest','structureCounts','attribution']:assert x[k]==y[k],(n,k)
            assert [{k:v for k,v in u.items() if k!='zh'} for u in x['units']]==[{k:v for k,v in u.items() if k!='zh'} for u in y['units']]
            if x['translated']:assert [u['zh'] for u in x['units']]==[u['zh'] for u in y['units']]
            assert all(u['zh'].strip() for u in y['units'])
cert=lambda p:re.search(r'Signer #1 certificate SHA-256 digest: (\w+)',Path(p).read_text()).group(1)
assert cert(O/'signature.txt')==cert(O/'previous-signature.txt')=='bdcaf7695c4a7bc250b289e8e4dbe1c8a3a0d63696aef4be619ffd79af2a4fc4'
m=json.loads((A/'faithful/completeness.json').read_text());assert (m['articlesTranslated'],m['reviewedArticles'],m['machineDraftArticles'],m['translatedUnits'])==(182,53,129,54189)
status={'apk':apk.name,'bytes':apk.stat().st_size,'sha256':hashlib.sha256(apk.read_bytes()).hexdigest(),'version':'0.14.1','versionCode':18,'sameSigningCertificate':True,'unchangedLegacyAssets':len(retained),'unchangedOfflineImageFiles':len(images),'originalSourceEnglishTreesTablesImagesLinksUnchanged':True,'previous40ReviewedTranslationsUnchanged':True,'allArchivedSourceUnitsHaveChinese':True,'reviewedArticles':53,'machineDraftArticles':129,'newReviewedArticles':13,'allSourcesSemanticallyReviewed':False,'newWikiImages':'remote references; not packaged offline','physicalSamsungTested':False}
(O/'build-verification.json').write_text(json.dumps(status,ensure_ascii=False,indent=2))
(O/'completeness.json').write_text(json.dumps(m,ensure_ascii=False,indent=2))
rows=[]
for p in m['checks']:
    state='逐段对照已校对' if p['reviewStatus']=='source-aligned-reviewed' else '机器翻译初稿／尚未逐句校对'
    rows.append('<tr><td>'+html.escape(p['titleZh'])+'<br><small>'+html.escape(p['title'])+'</small></td><td>'+str(p['revision'])+'</td><td>'+str(p['units'])+'</td><td>'+state+'</td><td><a href="'+html.escape(p['source'],quote=True)+'">原文固定版本</a> · <a href="'+str(p['pageid'])+'.txt">全部中英对照文字</a></td></tr>')
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>COD v0.14.1 全文收录与校对状态</title><style>body{margin:0;background:#111720;color:#edf2f8;font:16px/1.7 system-ui,sans-serif}main{max-width:1200px;margin:auto;padding:24px}h1{font-size:27px}.note{background:#263244;padding:18px;border-radius:12px}.scroll{overflow:auto}table{border-collapse:collapse;width:100%}td,th{border-bottom:1px solid #3c4a60;text-align:left;padding:12px;vertical-align:top}small{color:#adbdd2}a{color:#9ed4fc}input{font:inherit;width:100%;box-sizing:border-box;padding:12px;margin:16px 0;background:#1d2735;color:inherit;border:1px solid #56677f;border-radius:8px}</style><main><h1>COD v0.14.1 · 全文与校对状态</h1><p class="note">182篇固定版本来源、54189个文字单元均有中英对照。53篇已有逐段校对，129篇为机器翻译初稿，尚未逐句校对。文字齐全不代表语义正确；单篇齐全不代表所有关联子页都已收录。旧版1282张离线图片保留，新维基图片仍需联网。未在用户三星实体机或游戏内逐图实测。</p><p>正文、标题、表格单元格、图注和来源链接按原单元顺序保留；没有用摘要替换。原文章本身的缺口和冲突单独标注。原文作者：Call of Duty Wiki contributors。文字与译文按CC BY-SA 3.0共享，媒体权利另属原权利人。</p><input id="q" placeholder="搜索地图、武器或校对状态"><div class="scroll"><table><thead><tr><th>文章</th><th>固定版本</th><th>文字单元</th><th>状态</th><th>完整文字与来源</th></tr></thead><tbody>'''+''.join(rows)+'''</tbody></table></div></main><script>document.getElementById('q').oninput=function(){const q=this.value.toLowerCase();document.querySelectorAll('tbody tr').forEach(r=>r.hidden=!r.textContent.toLowerCase().includes(q));};</script></html>'''
Path('text-export/index.html').write_text(page)
for folder,name in [('text-export','COD_Guide_v0.14.1_全文对照.zip')]:
    with zipfile.ZipFile(O/name,'w',zipfile.ZIP_DEFLATED) as z:
        for p in Path(folder).rglob('*'):
            if p.is_file():z.write(p,p.relative_to(folder))
with zipfile.ZipFile(O/'COD_Guide_v0.14.1_源代码与断点.zip','w',zipfile.ZIP_DEFLATED) as z:
    for root in ['app/src','updates/v0141','ci']:
        for p in Path(root).rglob('*'):
            if p.is_file() and '__pycache__' not in p.parts:z.write(p,str(p))
    for n in ['app/build.gradle','app/proguard-rules.pro','build.gradle','settings.gradle','gradle.properties','.github/workflows/fulltext-v0141.yml']:
        p=Path(n)
        if p.exists():z.write(p,n)
    for p in Path('.drafts').rglob('*.json'):z.write(p,'draft-checkpoint/'+str(p.relative_to('.drafts')))
    z.writestr('README-RESUME.txt','COD guide v0.14.1 source checkpoint. Contains all packaged assets, 13 newly reviewed article translations, 142 source-bound machine-draft checkpoints, and tests. The app source is already integrated: do not run integrate.py on it twice. Original signing key intentionally excluded. Use the authorized existing repository CI/signing setup for compatible update builds; a different local key cannot overwrite the previously installed app. 53 articles are reviewed, 129 remain machine drafts. This is not a claim of fully verified gameplay content.\n')
with zipfile.ZipFile(O/'COD_Guide_v0.14.1_验收记录.zip','w',zipfile.ZIP_DEFLATED) as z:
    for name in ['build-verification.json','signature.txt','previous-signature.txt','completeness.json']:
        z.write(O/name,name)
    z.write('updates/v0141/content-integrity.json','content-integrity.json')
    for root in ['test-results','.drafts']:
        for p in Path(root).rglob('*'):
            if p.is_file() and (root=='test-results' or p.name in ['draft-manifest.json','review-flags.json']):z.write(p,str(p))
(O/'SHA256SUMS.txt').write_text(''.join(hashlib.sha256(p.read_bytes()).hexdigest()+'  '+p.name+'\n' for p in sorted(O.iterdir()) if p.suffix in ['.apk','.zip']))
print(json.dumps(status,ensure_ascii=False,indent=2))
