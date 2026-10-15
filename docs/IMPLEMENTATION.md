# Implementation notes

Reviewed against the locally installed Don't Starve Together `data/databundles/scripts.zip`, build **756039** (15 October 2026). The game scripts are not copied into this repository.

## Vanilla flow

1. `scripts/components/trader.lua` checks `AbleToAccept`, removes one item from its owner (splitting a stack if needed), and calls the Queen's `onaccept` callback.
2. `scripts/prefabs/monkeyqueen.lua` rejects a trade while her state graph has `busy`. On acceptance it enters `getitem`.
3. `scripts/stategraphs/SGmonkeyqueen.lua`: `getitem` plays `receive_item`. On `animover`, the game either spawns and flings a blueprint before entering `happy`, or enters `removecurse`.
4. In `removecurse`, the game removes up to four Monkey Curse stacks and sets the right-of-passage timer before entering `removecurse_channel`. The channel ends through `stopcursechanneling`, leading to `removecurse_success` or `removecurse_fail`. Vanilla clears `busy` in these result states after 15 frames.

## Change

`modmain.lua` uses `AddStategraphPostInit("monkeyqueen", ...)` to remove the `busy` tag from `happy`, `removecurse_success`, and `removecurse_fail`. It does not touch `getitem`, `removecurse`, or `removecurse_channel`. Thus another Banana cannot enter while its predecessor's reward or curse logic is still pending. The original event handlers, animation calls, item removal, loot selection, and timers remain in place. The state graph runs with the same patch on server and clients because `all_clients_require_mod = true`.

## Compatibility boundary

This patch depends on those three vanilla state names and on the ordering described above. If a future game update moves rewards or curse changes into a result state, reassess the patch before publishing an update. `tools/verify_upstream.py` checks these assumptions against a local game archive; it does not replace in-game testing.
