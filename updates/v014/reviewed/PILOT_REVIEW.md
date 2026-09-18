# Recovery validation and semantic review — 2026-09-18

Recovery workflow 35308373297 completed successfully: source recovery and all six checkpoint unit tests passed. Its translation pilot produced 11 long source units in 55.3 seconds and retained each in SQLite and JSON. This validates the recovery mechanism, not translation quality.

## Pilot rejected for release

The OpenNMT NLLB-1.3B probe still produced unknown tokens in five of eleven units. Semantic inspection also found unflagged missing clauses. In the paragraph beginning `The Kino der Toten photograph is hidden`, the draft stops after `however to move the monitor` and omits the requirement to activate the DEFCON switches in a specific order. The War Room machine paragraph omits the four named maps and the number-entry method. `Pack-a-Punched` is mistranslated as ordinary packing. No pilot output is approved or inserted into the APK. A successful workflow does not override these defects.

Do not launch this engine over the entire corpus and call its output a complete faithful translation. Do not replace missing clauses with a summary.

## Actual source-aligned content progress

`cold-war-remedy-3017191.json` now contains a complete assistant-checked Chinese translation of the fixed Cold War Remedy source revision 3017191: all 42 original text units remain in original order, including image alt-text and captions. The original six image slots and three external video links remain associated. The source-unit digest rejects use against a different revision. This article contains no loadout table; none is invented and none is dropped.

This is one article, not a claim that the whole Classified map, its dependencies, or all 182 captured articles have been translated. It is not yet packaged into a v0.14 APK. Existing v0.13.1 APK and guide text remain unchanged.

## Current unresolved work

- Complete translation and semantic checking of the remaining fixed source articles, keeping tables, narrative, notes, extra quests, captions and links.
- Resolve the two missing requested titles (`Masamune`, `KT-4/Masamune`) without treating a failure as an empty article.
- Finish image/source-license checks and retain every media slot with its actual status.
- Integrate the aligned source reader into the app, then build and test the delivered APK.

The 64 balanced partitions are a scheduling plan only; they are not 64 running or completed translation jobs. The old end-of-shard-only translator remains unsuitable for re-run. New per-unit checkpoint infrastructure has been tested, but full production translation is not complete.
