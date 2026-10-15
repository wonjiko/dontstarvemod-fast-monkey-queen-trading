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
