# Recovery status — 2026-09-18

The user requires complete source-by-source translations, including loadouts, narrative, notes, optional Easter eggs, all tables, image slots and video links. Do not treat drafts or structural counts as completed translations. Do not substitute summaries.

The previous corpus run 35304272902 exceeded the configured 45-minute job window. Six translation shards were cancelled and produced no artifacts because translate_corpus.py wrote only after the entire shard. Two shards survived: 8,067 draft records, including 2,836 flagged with unknown tokens. None are approved. The parsed source corpus survives: 182 pages and 54,189 text units (32,264 unique texts). Two unresolved source titles are retained in the failure ledger; they are not silently omitted.

New recovery_state.py commits each finished unit with full source offsets and an engine-specific key. Its tests cover source reconstruction, restart recovery, stale engine rejection, missing tails, numeric/unknown-token review flags, and preservation of duplicate source occurrences. recover_report.py builds 64 length-balanced work partitions without selecting or deleting editorial material. The smaller partitions are a recovery plan, not a claim that translation has finished.

A bounded correct-tokenizer pilot uses OpenNMT's converted model and Transformers tokenizer as documented by CTranslate2. Pilot outputs are never auto-approved. Production-wide translation and APK release remain blocked on quality review; do not blindly re-run the old 45-minute jobs.

No new APK is claimed by this recovery commit. Existing v0.13.1 app, guide text and gesture handling are unchanged.
