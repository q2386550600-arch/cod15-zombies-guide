# v0.9 recovery build

Overview and step tutorial are separate screens. The bottom step navigation is pinned. Each step resets only its own scroll area.

Image corpus: 22 source articles, 1170 image references, 1148 original files. Source commit 575948e073432d59019ee030db2201e0a8157efb in PlagueFPS/cod-zombies. All image references are retained in per-map full galleries, including prerequisites. Remaster variants may share the author's source images. Not all map entries have a source article. Some captions and section titles retain original English; Chinese navigation labels are supplemental. No claim of in-game testing of every location or completeness of every community source.

Build inputs are the source-assets Actions artifacts from run 35232916091. tools/prepare_media.py validates every source article and every included image against its recorded SHA-256. It aborts on missing or changed files. These build-input artifacts expire; APKs already containing the images work offline independently.

The existing published signing key is a test key, not a secure production signing credential.
