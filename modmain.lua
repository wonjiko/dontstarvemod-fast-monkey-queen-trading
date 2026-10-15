-- The Queen's vanilla trade is complete before entering any of these states:
-- getitem grants the blueprint before happy, and the curse channel finishes
-- before removecurse_success/removecurse_fail. Keep those processing states busy.
AddStategraphPostInit("monkeyqueen", function(sg)
    for _, name in ipairs({ "happy", "removecurse_success", "removecurse_fail" }) do
        local state = sg.states[name]
        if state ~= nil and state.tags ~= nil then
            state.tags.busy = nil
        end
    end
end)

-- Erasing a blueprint at the Cartographer's Desk uses the generic one-second
-- long action in vanilla. Select the existing short action on both the server
-- and the predicting client; the original ERASE_PAPER action still consumes the
-- blueprint and grants Papyrus. Other erasable paper keeps its vanilla timing.
local function BlueprintEraseState(inst, action)
    local item = action ~= nil and action.invobject or nil
    local target = action ~= nil and action.target or nil
    if item ~= nil and item.scrapbook_proxy == "blueprint"
        and target ~= nil and target.prefab == "cartographydesk" then
        return "doshortaction"
    end
    return "dolongaction"
end

local erase_paper = GLOBAL.ACTIONS.ERASE_PAPER
local ActionHandler = GLOBAL.ActionHandler
AddStategraphActionHandler("wilson", ActionHandler(erase_paper, BlueprintEraseState))
AddStategraphActionHandler("wilson_client", ActionHandler(erase_paper, BlueprintEraseState))
