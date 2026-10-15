"""Check the vanilla trade boundaries this small state-graph patch relies on.

Usage: python tools/verify_upstream.py PATH_TO_DSTSCRIPTS_ZIP
"""

import re
import sys
import zipfile


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def state_block(source, name):
    match = re.search(
        r'State\s*\{\s*name\s*=\s*"' + re.escape(name) + r'"(.*?)(?=\n\s*State\s*\{|\n\s*return StateGraph)',
        source,
        re.S,
    )
    require(match is not None, f"Missing state: {name}")
    return match.group(1)


def main(archive_path):
    with zipfile.ZipFile(archive_path) as archive:
        queen = archive.read("scripts/prefabs/monkeyqueen.lua").decode("utf-8")
        sg = archive.read("scripts/stategraphs/SGmonkeyqueen.lua").decode("utf-8")
        trader = archive.read("scripts/components/trader.lua").decode("utf-8")

    require('inst.sg:HasStateTag("busy")' in queen, "Queen no longer gates trading on busy")
    require('inst.sg:GoToState("getitem"' in queen, "Queen no longer enters getitem")
    require('item.components.inventoryitem:RemoveFromOwner(true)' in trader, "Trader ownership flow changed")
    require('item.components.stackable:Get(count)' in trader, "Trader stack split flow changed")

    getitem = state_block(sg, "getitem")
    require('tags = {"busy"}' in getitem, "getitem must remain busy")
    require('PlayAnimation("receive_item")' in getitem, "Receive animation changed")
    require('FlingItem(loot)' in getitem, "Blueprint reward flow changed")
    require('GoToState("happy"' in getitem, "Blueprint completion boundary changed")

    remove = state_block(sg, "removecurse")
    channel = state_block(sg, "removecurse_channel")
    require('tags = {"busy"}' in remove, "Curse removal must remain busy")
    require('RemoveCurse("MONKEY", 4)' in remove, "Curse removal amount changed")
    require('"right_of_passage"' in remove, "Right-of-passage timer changed")
    require('GoToState("removecurse_channel")' in remove, "Curse channel boundary changed")
    require('tags = {"busy","channel"}' in channel, "Curse channel must remain busy")
    require('EventHandler("stopcursechanneling"' in sg, "Curse channel completion changed")

    for name in ("happy", "removecurse_success", "removecurse_fail"):
        block = state_block(sg, name)
        require('tags = {"busy"}' in block, f"Expected busy reaction state: {name}")
        require('PlayAnimation(' in block, f"Expected vanilla animation: {name}")

    print("PASS: vanilla trade and curse processing still finish before patched reaction states")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
