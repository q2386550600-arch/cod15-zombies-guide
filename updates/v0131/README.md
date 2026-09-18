# v0.13.1 gesture-only hotfix

The user rejected abridgment and demands faithful, complete source translation including loadouts, lore, videos and optional quests. This hotfix does not fulfill or claim to fulfill that content request. No new publisher prose is copied or translated, and the previously delivered content is unchanged byte-for-byte.

Before translating an entire third-party corpus for redistribution, establish applicable permission/licensing, or work from source documents the user supplies for translation. Do not substitute another summary and call it a complete translation. Preserve the user's stated scope in future content work.

Old behavior explicitly ignored image-area swipes at zoom > 1. New default is single-finger horizontal paging over the entire viewer, at every zoom factor; an explicit image-move mode handles panning. On Android the asset-only WebView reports mode to a minimal native gesture layout. WebView page-level zoom is disabled; image zoom buttons remain. A browser pointer fallback exists but is not enabled alongside native handling.

No claim of testing on the user's physical Samsung phone. Android runtime reports, when successful, apply only to the emulator tested.
