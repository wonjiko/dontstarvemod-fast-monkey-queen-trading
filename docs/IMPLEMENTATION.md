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

## Blueprint erasing at the Cartographer's Desk

In build 756039, `scripts/prefabs/blueprint.lua` marks every standard and specific Blueprint with `scrapbook_proxy = "blueprint"`. The Cartographer's Desk prefab is `cartographydesk` and has the `papereraser` component. `ACTIONS.ERASE_PAPER` calls that component, which delegates to `ErasablePaper:DoErase`. The component spawns Papyrus, consumes one Blueprint, and gives or drops the Papyrus.

The vanilla `ERASE_PAPER` handler sends both `wilson` and `wilson_client` to `dolongaction` (one-second server timeout). This mod adds a handler on both state graphs that chooses `doshortaction` only when the item is a Blueprint and the target is a Cartographer's Desk. The existing short action performs the buffered action after six frames. All other `ERASE_PAPER` uses keep `dolongaction`. The action and component themselves are unchanged, so conversion results and stack handling stay under vanilla control.
