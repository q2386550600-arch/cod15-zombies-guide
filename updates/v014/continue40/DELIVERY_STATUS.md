# Verified delivery checkpoint — 2026-09-18

## Resume here, not from the earlier failed machine-translation pilots

The installed artifact for this checkpoint is `COD_Zombies_Guide_v0.14.0-preview3.apk`.

- Package: `com.openai.cod15guide`
- versionCode: 17
- versionName: `0.14.0-preview3`
- APK bytes: 166820804
- APK SHA-256: `1088ae95c23c79bb6400ccc321df35b00dd14bd6b89460ae60a6ecda2e4dcb4c`
- Source commit: `25dbb88846dadca31c72c54ef4e7c4410e799cc6`
- Workflow: `.github/workflows/reader40-v014.yml`
- Run: 35362047962; build and Android jobs both SUCCESS.
- Build artifact: 10554896837 (`COD-source-reader-v0.14-preview3`). Contains APK, exact generated sources, all 40 reviewed translations, completeness and signature reports.
- Browser artifact: 10555051920 (`source-reader40-browser-tests`).
- Native artifact: 10554596598 (`source-reader40-android-tests`). Native report APK hash matches the delivered file.

## Actual completion scope

40 complete fixed-revision source articles have 4027 aligned Chinese text units in the APK. Units include original paragraphs, headings, table cells and captions, not 4027 separate gameplay instructions. 182 original articles are archived, with 54189 total original text units. 142 articles still have original English only. Do not label the entire corpus or all optional quests fully translated.

The 40 complete reviews include the major quest pages, Origins staff articles, crafting articles, Cold War Remedy, full Classified, Classified/Ciphers, Winter's Howl, Guillotine, KT-4/Masamune and the completed Revelations quest. Full-article translation preserves source tables, loadout advice, lore, ending prose, notes, repeated source units, image slots and links. Linked pages are separate sources; a complete parent article is not a claim that every dependency is translated.

Article text is attributed to Call of Duty Wiki contributors with fixed revision/history URLs and CC BY-SA 3.0 links. Chinese translations use that same license. Images/videos/game audio have separate rights. New wiki image pixels remain original remote references and need network; 613 image slots are retained in translated articles. This is NOT a claim that 613 new images have been bundled offline. Existing 1148 screenshots and 134 map/floorplan files are unchanged and remain offline. All 1313 old non-index asset files were compared byte-for-byte.

## App entry

Map overview -> `来源全文 · 逐段对应` -> `开始逐节阅读完整译文`.
Library -> `全部来源／额外彩蛋／制作` -> `完整译文` or `待翻译`.
The former rewritten guide remains explicitly separate and keeps its old progress. Do not direct the user into it and call it the full-source translation.

## Tests that actually passed

Browser: all 182 trees preserve the original text-unit ordering, tables/rows/cells, image slots, embedded-media records and external links; translated visible units equal the approved translations. Whole-article vs section reading, linked local prerequisite navigation, bilingual display and the repaired TOC/next-section state all pass.

Android API 36 emulator: v0.13.1 in-place update preserves notes and detail positions; source reader works with radios disabled; full text and tables render offline; G-Strike dependency resolves locally; native whole-view swipe at zoom changes one image record; back preserves old guide state; full Voyage loadout, KT-4 and Classified units render; TOC-to-next navigation passes. Remote image pixel loading is NOT validated by the offline test. Physical Samsung device and full in-game quest runs have not been tested.

## Exact source recovery

`updates/v014/continue40/prepare.py` reconstructs the saved 30-article bundles, salvages only five complete CRC-verified ZIP entries from the truncated 36-article archive, then uses separately committed complete reviews for the formerly truncated sixth and four additional articles. It validates exactly 40 reviews and 4027 units before building. Never blindly unzip the incomplete `continue36` archive or accept its partial sixth entry.

Prefer the generated-sources and reviewed-translations ZIPs in artifact 10554896837 for the next version. Do not restore the old checked-in v0.9 app assets, and do not redo the translation model experiments. Preserve source revision and digest checks. The new reader has a corrected anchor-to-section resolver; do not regress it.

## Remaining work

Translate the remaining source articles fully without summarizing, including standalone optional quests, map pages, transcripts and dependencies. Preserve every source clause and table, marking original conflicts in separate translator notes rather than silently editing. Check media rights and actual loading; retain unresolved references explicitly. Integrate only complete matching reviews and update the completeness inventory honestly. Re-run the actual compiled APK tests for subsequent deliveries.
