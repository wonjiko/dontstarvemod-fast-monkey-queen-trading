# In-game verification plan

Run these checks on the current game build before Steam Workshop publication. Record the game build, host type, and any errors from `client_log.txt` and `server_log.txt`.

| Case | Expected result |
| --- | --- |
| No curse: give two separate Bananas rapidly | One Banana consumed per accepted trade; one blueprint drops per trade; the next trade can begin during `happy`. |
| No curse: give two from a stack | Stack decreases by two; two blueprint drops. |
| Cursed player: give Bananas rapidly | The next trade is blocked during receive and curse channel; up to four curse stacks removed per completed trade. |
| Curse result animation | The next trade can begin immediately in success/fail; result animation remains visible if no new trade interrupts it. |
| Right of passage | Existing timer still starts or resets at the original duration. |
| Multiplayer: dedicated server, two clients | Both clients see the same Queen animation and rewards; no duplicate items or desync. |
| Multiplayer: host and joining client | Both can trade in succession; rewards and item counts agree on both sides. |
| Other NPCs | Their trading behavior is unchanged. |

These are manual checks, not claims of completed gameplay testing.
