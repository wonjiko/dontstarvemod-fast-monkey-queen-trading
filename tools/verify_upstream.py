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
        actions = archive.read("scripts/actions.lua").decode("utf-8")
        wilson = archive.read("scripts/stategraphs/SGwilson.lua").decode("utf-8")
        wilson_client = archive.read("scripts/stategraphs/SGwilson_client.lua").decode("utf-8")
        blueprint = archive.read("scripts/prefabs/blueprint.lua").decode("utf-8")
        desk = archive.read("scripts/prefabs/cartography_prototyper.lua").decode("utf-8")
        erasable = archive.read("scripts/components/erasablepaper.lua").decode("utf-8")
        curse_prop = archive.read("scripts/prefabs/cursed_monkey_token.lua").decode("utf-8")

    require('inst.sg:HasStateTag("busy")' in queen, "Queen no longer gates trading on busy")
    require('inst.sg:GoToState("getitem"' in queen, "Queen no longer enters getitem")
    require('item.components.inventoryitem:RemoveFromOwner(true)' in trader, "Trader ownership flow changed")
    require('item.components.stackable:Get(count)' in trader, "Trader stack split flow changed")

    getitem = state_block(sg, "getitem")
    require('tags = {"busy"}' in getitem, "getitem must remain busy")
    require('PlayAnimation("receive_item")' in getitem, "Receive animation changed")
    require('EventHandler("animover"' in getitem, "Receive completion event changed")
    require('FlingItem(loot)' in getitem, "Blueprint reward flow changed")
    require('GoToState("happy"' in getitem, "Blueprint completion boundary changed")

    remove = state_block(sg, "removecurse")
    channel = state_block(sg, "removecurse_channel")
    require('tags = {"busy"}' in remove, "Curse removal must remain busy")
    require('RemoveCurse("MONKEY", 4)' in remove, "Curse removal amount changed")
    require('EventHandler("animover"' in remove, "Curse preparation completion event changed")
    require('"right_of_passage"' in remove, "Right-of-passage timer changed")
    require('GoToState("removecurse_channel")' in remove, "Curse channel boundary changed")
    require('tags = {"busy","channel"}' in channel, "Curse channel must remain busy")
    require('EventHandler("stopcursechanneling"' in sg, "Curse channel completion changed")
    require('inst.target:PushEvent("stopcursechanneling",{success=true})' in curse_prop,
            "Curse prop arrival event changed")
    require('inst.components.updatelooper:AddOnUpdateFn(OnUpdateProp)' in curse_prop,
            "Curse prop movement hook changed")

    for name in ("happy", "removecurse_success", "removecurse_fail"):
        block = state_block(sg, name)
        require('tags = {"busy"}' in block, f"Expected busy reaction state: {name}")
        require('PlayAnimation(' in block, f"Expected vanilla animation: {name}")

    require('ActionHandler(ACTIONS.ERASE_PAPER, "dolongaction")' in wilson,
            "Server paper erasing no longer uses dolongaction")
    require('ActionHandler(ACTIONS.ERASE_PAPER, "dolongaction")' in wilson_client,
            "Client paper erasing no longer uses dolongaction")
    short_action = state_block(wilson, "doshortaction")
    require('TimeEvent(6 * FRAMES' in short_action and 'PerformBufferedAction()' in short_action,
            "Server short action timing changed")
    require('inst.scrapbook_proxy = "blueprint"' in blueprint,
            "Blueprint identification changed")
    require('Prefab("cartographydesk"' in desk and 'inst:AddComponent("papereraser")' in desk,
            "Cartographer's Desk eraser changed")
    require('ACTIONS.ERASE_PAPER.fn' in actions and 'papereraser:DoErase' in actions,
            "ERASE_PAPER action no longer delegates to papereraser")
    require('self.erased_prefab = "papyrus"' in erasable and 'self.inst:Remove()' in erasable,
            "Blueprint consumption or Papyrus result changed")

    print("PASS: Queen animation, curse flow, trade boundaries, and Blueprint action match the mod's assumptions")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit(__doc__)
    main(sys.argv[1])
