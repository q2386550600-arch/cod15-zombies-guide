# Delivered checkpoint: v0.14.2-offline

Package `com.openai.cod15guide`, versionCode 19. The existing v0.14.0-preview3 signing certificate is unchanged.

APK filename: `COD_Zombies_Guide_v0.14.2-offline.apk`
APK size: 1,013,742,089 bytes.
APK SHA-256: `8ede25ef9cde9d16977928d605f7dacde88e91eed55f65cec641a7cd13666360`

## Content scope

182 fixed archived sources; all 54,189 original text units have Chinese counterparts. Original English units, order, tables, media slots, credits and links remain intact.
52 sources / 4,727 units are source-by-source reviewed. 130 sources are complete automatic drafts and remain explicitly unreviewed. Do not mark those reviewed merely because every unit has Chinese.
This continuation added 12 reviewed sources / 700 units: Navcard, Apothicon Sword, all four Der Eisendrache bows, all four Ancient Evil hands, Apollo's Will and Pegasus Strike.
3,308 unique source original-size images are offline, covering 6,754 image references. Downloaded original bytes are retained; no image resizing/recompression was used. All 1,148 legacy screenshots and 134 atlas assets are byte-identical to preview3.
Video and source hyperlinks remain; video files are not bundled offline. This is the current archived corpus, not a claim that every external community source has been collected.

## Successful actual checks

- Build run 35373097362, build job 105691449664: success; APK signatures, version, ZIP integrity and legacy asset invariants checked.
- Browser run 35374141222, browser job 105694740589: success; all 182 complete source trees and local resource/display invariants, offline original-image pixels, source-to-atlas/gallery round trip, Chinese and review-status filtering.
- Native run 35374671226, Android job 105696441744: success; same exact APK SHA-256, Android 16/API36 Pixel7 emulator, in-place upgrade preserving notes/detail positions, radios-off source reading and actual original-image pixels, real Android swipes at 100/150/250% and native pan without image switching.

Native test navigation activates existing DOM controls through the debugger; it is not a physical-button-tap test. Image gestures are real `adb input swipe` through the active native interception path. No physical Samsung device was tested. First automation failures are retained in the delivered QA history; no APK or CSP was changed to make retests pass.

## Continuation and recovery

The user-facing delivery includes `COD_Zombies_Guide_v0.14.2_Source_QA.zip`: Java/frontend source, all 182 bilingual source pages, original revision/unit IDs, per-page review checklist, JSON audits, tests and screenshots, and an offline `restore_assets.py` script. Combined with the APK, it restores the complete actual app assets without dependence on expiring Actions artifacts. The package excludes private signing keys and fonts.

Source checkpoint restoration in CI: run `prepare.py`, then `test_fixes.py` for CSP-safe browser waits; run `native_control_verification.py` before the final native verification. The application packaging scripts and 12 complete reviewed article files are preserved in the hash-verified payload and exported source bundle.

The next content task is genuine source-by-source semantic checking of the remaining 130 full drafts, preserving all source content rather than summarizing or auto-approving it. No recurring or background task was scheduled.
