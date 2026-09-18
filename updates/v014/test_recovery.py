import json,tempfile,unittest
from pathlib import Path
from recovery_state import Journal,split_exact,mechanical_flags,make_plan
class RecoveryTests(unittest.TestCase):
 def test_exact_partition(self):
  for source in ['', 'one', 'Hello. Next sentence!  A third?', 'w'*900, '\n'.join(['Original row 1; row 2.']*140)]:
   chunks=split_exact(source,80);self.assertEqual(source,''.join(c[2] for c in chunks));self.assertTrue(all(b-a<=80 for a,b,_ in chunks))
 def test_resume(self):
  with tempfile.TemporaryDirectory() as d:
   path=Path(d)/'journal.sqlite';j=Journal(path)
   for i in range(3):
    s=f'original {i}';j.put(s,'v1',[{'start':0,'end':len(s),'source':s,'zh':f'原文 {i}'}])
   j.close();j=Journal(path)
   for i in range(3):self.assertIsNotNone(j.get(f'original {i}','v1'))
   self.assertIsNone(j.get('original 3','v1'));self.assertIsNone(j.get('original 1','new-engine'))
   j.export(Path(d)/'checkpoint.json');self.assertEqual(len(json.loads((Path(d)/'checkpoint.json').read_text())),3);j.close()
 def test_missing_tail_rejected(self):
  with tempfile.TemporaryDirectory() as d:
   j=Journal(Path(d)/'j.db')
   with self.assertRaises(ValueError):j.put('abcdef','v',[{'start':0,'end':3,'source':'abc','zh':'甲'}])
   self.assertIsNone(j.get('abcdef','v'));j.close()
 def test_flags_not_release(self):
  with tempfile.TemporaryDirectory() as d:
   j=Journal(Path(d)/'j.db');s='Open 4 doors';c=[{'start':0,'end':len(s),'source':s,'zh':'打开3扇门<unk>'}]
   r=j.put(s,'v',c);self.assertEqual(r['status'],'needs-review')
   with self.assertRaises(ValueError):j.put(s,'v',c,reviewed=True)
   j.close()
 def test_no_draft_autoapproval(self):
  with tempfile.TemporaryDirectory() as d:
   j=Journal(Path(d)/'j.db');s='Open the door';r=j.put(s,'v',[{'start':0,'end':len(s),'source':s,'zh':'开门'}]);self.assertEqual(r['status'],'draft');self.assertFalse(r['reviewed']);j.close()
 def test_plan_no_loss(self):
  units=[{'id':str(i),'en':('paragraph '*i) if i%3 else 'Repeated'} for i in range(137)];p=make_plan(units,9)
  self.assertEqual(sorted(x for b in p['shards'] for item in b for x in item['unitIds']),sorted(u['id'] for u in units));self.assertEqual(p['uniqueTexts'],len({u['en'] for u in units}))
if __name__=='__main__':unittest.main(verbosity=2)
