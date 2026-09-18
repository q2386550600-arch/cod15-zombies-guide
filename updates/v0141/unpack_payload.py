"""Restore the reviewed translation checkpoint; fail closed on any changed byte."""
import base64, hashlib, json, lzma
from pathlib import Path

root = Path(__file__).resolve().parent
parts = [root / ('payload%02d.b64' % i) for i in range(6)]
assert all(p.is_file() for p in parts), 'Missing checkpoint chunk'
encoded = ''.join(p.read_text(encoding='ascii').strip() for p in parts)
assert len(encoded) == 43964
packed = base64.b64decode(encoded, validate=True)
assert len(packed) == 32972
assert hashlib.sha256(packed).hexdigest() == 'f4dc2d9e88b704489e78e0e05495c22bc118ddd6cc6e1b79f3dccc73b319862e', 'Compressed checkpoint mismatch'
raw = lzma.decompress(packed)
assert len(raw) == 97585
assert hashlib.sha256(raw).hexdigest() == 'e3bce082f34a434c1ad496b0c003f75079a094c532affb8f25634c2ffccb3ce1', 'Decoded checkpoint mismatch'
files = json.loads(raw)
assert isinstance(files, dict) and len(files) == 15
for name, text in files.items():
    p = Path(name)
    assert isinstance(text, str) and not p.is_absolute() and '..' not in p.parts
    assert name in ('integrate.py', 'prepare_tests.py') or (len(p.parts) == 2 and p.parts[0] == 'reviewed' and p.name.startswith('reviewed-') and p.suffix == '.json')
    target = root / p
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(text, encoding='utf-8')
print('Verified checkpoint restored:', len(files), 'UTF-8 files; 13 complete article reviews')
