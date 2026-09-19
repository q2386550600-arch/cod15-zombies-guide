from pathlib import Path
import ast
p=Path('updates/v014/complete/native_test.py')
s=p.read_text()
old="APK=Path('output/COD_Zombies_Guide_v0.14.2-offline.apk')"
new="APK=Path('output/COD_Zombies_Guide_v0.15.1.apk')"
assert s.count(old)==1,(old,s.count(old))
s=s.replace(old,new)
ast.parse(s)
p.write_text(s)
print('Native QA targets the exact v0.15.1 APK filename')
