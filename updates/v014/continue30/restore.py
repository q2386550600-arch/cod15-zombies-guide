from pathlib import Path
import base64,lzma,json,hashlib
P=Path('updates/v014/delivery')
for stem,count,digest,expected in [
 ('reader23',4,'e16b3096dd16b2e3d721a6a9fa4214cb5f007582c4c600022fdbac94efa609a8',17),
 ('reviews30',3,'730a5edb4897f29cc9bb2080f12be3d9700781b8e60be04cafc077904502bdfd',7)]:
 encoded=''.join((P/f'{stem}.xz.b64.part{i}').read_text().strip() for i in range(1,count+1))
 raw=lzma.decompress(base64.b64decode(encoded,validate=True))
 assert hashlib.sha256(raw).hexdigest()==digest,(stem,'checkpoint transfer mismatch')
 files=json.loads(raw);assert len(files)==expected
 for name,content in files.items():
  path=Path(name);assert not path.is_absolute() and '..' not in path.parts
  assert name.startswith(('updates/v014/reviewed/','updates/v014/full_reader/'))
  path.parent.mkdir(parents=True,exist_ok=True);path.write_text(content)
 print('Restored',stem,len(files),'hash-checked text files')
reviews=[json.loads(p.read_text()) for p in Path('updates/v014/reviewed').glob('*.json')]
assert len(reviews)==30 and len({r['pageid'] for r in reviews})==30
assert sum(len(r['translationsInUnitOrder']) for r in reviews)==2633
print('30 complete source-ordered translations, 2633 units; other pages remain explicitly untranslated.')
