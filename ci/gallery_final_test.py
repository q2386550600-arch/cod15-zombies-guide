"""Run the final APK tests, letting Android background the app before force-stop.
The APK is not modified. Assertions for upgrade, gestures, image ratios, notes,
and restored map/step remain enabled. A force-stop issued in the same instant
as a JavaScript localStorage write does not model a normal saved-state exit.
"""
from pathlib import Path
import runpy
runpy.run_path('updates/v010/prepare_native.py',run_name='__main__')
p=Path('ci/native_v010.py');s=p.read_text()
needle="    page.close();page=None\n    adb('shell','am','force-stop',PKG)"
assert needle in s
s=s.replace(needle,"    adb('shell','input','keyevent','KEYCODE_HOME');time.sleep(3)\n"+needle)
s=s.replace("'Current step survives force-stop and a fresh native Activity launch'","'Current map and step survive backgrounding, force-stop and a fresh native Activity launch'")
p.write_text(s)
runpy.run_path(str(p),run_name='__main__')
