# Fast Monkey Queen Trading

![Fast Monkey Queen Trading preview](preview.png)

A small, independent **Don't Starve Together** mod. After the Queen of Moon Quay finishes processing a Banana or Cooked Banana, you can offer the next one immediately instead of waiting for her happy or curse-result animation to finish. Erasing a Blueprint into Papyrus at the Cartographer's Desk also uses a short action.

The Queen's normal trade logic remains in charge. Each accepted trade still consumes one item. Blueprint selection and drops, removal of up to four Monkey Curse stacks, and the right-of-passage timer follow the game's original code. The receiving animation and curse channel still run. A new trade can interrupt the final reaction animation, as it normally transitions the Queen into the receiving state.

Blueprint erasing still uses the game's original `ERASE_PAPER` action and `ErasablePaper` component: one Blueprint is consumed and the normal Papyrus output is given. The faster timing applies only to Blueprints used on a Cartographer's Desk. Other erasable papers keep their usual timing.

## Install

Copy this repository folder into the game's `mods` folder. Enable **Fast Monkey Queen Trading** in the world settings before starting the world. In multiplayer, the server and every joining client need the mod enabled.

## Scope

- Speeds up Queen of Moon Quay (`monkeyqueen`) repeat trading and Blueprint erasing at the Cartographer's Desk.
- No configuration or dependency on another mod.
- Does not alter Banana acceptance rules, rewards, curse removal, or the grace period.
- Does not skip the receive animation or the curse channel; those steps must finish before the next trade.
- Does not change the Blueprint-to-Papyrus output or affect other paper-erasing actions.

## Verification

The implementation was checked against installed DST scripts build **756039**. See [Implementation notes](docs/IMPLEMENTATION.md), [test plan](docs/TESTING.md), and [publishing checklist](docs/PUBLISHING.md). In-game multiplayer testing remains to be completed before publishing to the Steam Workshop.

## License

MIT. See [LICENSE](LICENSE).

한국어 안내: [README.ko.md](README.ko.md)
