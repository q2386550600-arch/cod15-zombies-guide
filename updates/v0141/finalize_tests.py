from pathlib import Path
p=Path('updates/v0141/test_complete.py');s=p.read_text()
a="page.wait_for_function('FaithfulDebug.getDoc()?.metadata.pageid===330385')"
b="page.wait_for_function('window.FaithfulDebug?.getDoc()?.metadata.pageid===330385')"
assert s.count(a)==1;s=s.replace(a,b);p.write_text(s)
print('Map-overview test waits for the destination script context before reading its document')
