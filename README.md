# Fast Monkey Queen Trading

![Fast Monkey Queen Trading preview](preview.png)

A small, independent **Don't Starve Together** mod for the Queen of Moon Quay. After she finishes processing a Banana or Cooked Banana, you can offer the next one immediately instead of waiting for her happy or curse-result animation to finish.

The Queen's normal trade logic remains in charge. Each accepted trade still consumes one item. Blueprint selection and drops, removal of up to four Monkey Curse stacks, and the right-of-passage timer follow the game's original code. The receiving animation and curse channel still run. A new trade can interrupt the final reaction animation, as it normally transitions the Queen into the receiving state.

## Install

Copy this repository folder into the game's `mods` folder. Enable **Fast Monkey Queen Trading** in the world settings before starting the world. In multiplayer, the server and every joining client need the mod enabled.

## Scope

- Works on the Queen of Moon Quay (`monkeyqueen`) only.
- No configuration or dependency on another mod.
- Does not alter Banana acceptance rules, rewards, curse removal, or the grace period.
- Does not skip the receive animation or the curse channel; those steps must finish before the next trade.

## Verification

The implementation was checked against installed DST scripts build **756039**. See [Implementation notes](docs/IMPLEMENTATION.md) and [test plan](docs/TESTING.md). In-game multiplayer testing remains to be completed before publishing to the Steam Workshop.

## License

MIT. See [LICENSE](LICENSE).

한국어 안내: [README.ko.md](README.ko.md)
