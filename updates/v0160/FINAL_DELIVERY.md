# COD Zombies Guide v0.16.0 — final delivery

Final state: all fixed-revision source pages are source-by-source reviewed.

## Deliverable

- APK: `COD_Zombies_Guide_v0.16.0.apk`
- GitHub Actions run: `35427728692`
- Main artifact: `COD-Zombies-Guide-v0.16.0-review182`
- Main artifact ID: `10579742459`
- APK size: `1,013,573,741 bytes`
- APK SHA-256: `054008dca1e91b29fea93b5bafc97e27e3871b053b5c6f53663c49da708b762c`
- Signing certificate SHA-256: `bdcaf7695c4a7bc250b289e8e4dbe1c8a3a0d63696aef4be619ffd79af2a4fc4`

The main Actions artifact also includes the source/QA checkpoint and update notes.

Because the APK is about 1 GB, the workflow also uploaded the raw APK as transfer chunks:

- `v0160-apk-part00` — artifact ID `10579622697`
- `v0160-apk-part01` — artifact ID `10579432828`
- `v0160-apk-part02` — artifact ID `10579292962`
- `v0160-apk-part03` — artifact ID `10579577686`
- `v0160-apk-part04` — artifact ID `10579492822`

The chunk manifests contain per-part SHA-256 values and the expected final APK SHA-256.

## Final corpus

- Fixed-revision archived sources: `182 / 182`
- Source-by-source reviewed Chinese articles: `182 / 182`
- Original text units reviewed: `54,189 / 54,189`
- Automatic full-text drafts remaining: `0`
- Unique original-size offline source images: `3,308`

Original English text, source order, tables, captions, embedded links, prerequisite links, image slots and source attribution are retained.

## QA

Final workflow run `35427728692` is green.

- build job `105857323733`: success
- browser job `105857324027`: success
- Android 16 / API 36 job `105857323144`: success

Browser QA verified all 182 source trees, 54,189 translated units, bilingual equality, source ordering, TOC/section resume, local prerequisite navigation and original-size image loading.

Android QA verified the exact APK SHA above, including upgrade from v0.14.0-preview3, offline article rendering, local source links, native image swipe/pan behavior and retained guide state.

No physical Samsung device test was performed. The Android test target was an API 36 emulator.
