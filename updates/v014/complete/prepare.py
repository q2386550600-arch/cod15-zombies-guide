"""Restore the exact reviewed UTF-8 implementation from its transport checkpoint."""
from pathlib import Path
import base64,hashlib,json,lzma
root=Path('updates/v014/complete')
raw=base64.b64decode(''.join((root/f'payload{i:02d}.b64').read_text().strip() for i in range(6)),validate=True)
assert hashlib.sha256(raw).hexdigest()=='4a3e81904ed0e332f446241be37cbeb69e158a47e316e39c23f289ffc4fce14c','Checkpoint transfer integrity mismatch'
files=json.loads(lzma.decompress(raw));assert len(files)==18
for name,content in files.items():
    p=Path(name)
    assert not p.is_absolute() and '..' not in p.parts and name.startswith('updates/v014/complete/')
    assert p.suffix in ['.py','.json'] and isinstance(content,str)
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf-8')
print('Restored 18 verified source, test and translation files')
