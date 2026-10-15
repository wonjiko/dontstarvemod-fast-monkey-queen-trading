-- Speed up the two Queen animations that gate the vanilla trade result. Their
-- animover handlers still award the blueprint or remove the curse exactly once.
local QUEEN_ANIMATION_SPEED = 8
local CURSE_PROP_EXTRA_SPEED = 60

-- The Queen's vanilla trade is complete before entering any of these states:
-- getitem grants the blueprint before happy, and the curse channel finishes
-- before removecurse_success/removecurse_fail. Keep those processing states busy.
AddStategraphPostInit("monkeyqueen", function(sg)
    for _, name in ipairs({ "getitem", "removecurse" }) do
        local state = sg.states[name]
        if state ~= nil and state.onenter ~= nil then
            local original_onenter = state.onenter
            local original_onexit = state.onexit
            state.onenter = function(inst, ...)
                original_onenter(inst, ...)
                if inst.sg.currentstate == state then
                    inst.AnimState:SetDeltaTimeMultiplier(QUEEN_ANIMATION_SPEED)
                end
            end
            state.onexit = function(inst, ...)
                inst.AnimState:SetDeltaTimeMultiplier(1)
                if original_onexit ~= nil then
                    original_onexit(inst, ...)
                end
            end
        end
    end

    for _, name in ipairs({ "happy", "removecurse_success", "removecurse_fail" }) do
        local state = sg.states[name]
        if state ~= nil and state.tags ~= nil then
            state.tags.busy = nil
        end
    end
end)

-- The vanilla curse prop still reaches the Queen and sends the original
-- stopcursechanneling event. Move it faster only while returning to her.
AddPrefabPostInit("cursed_monkey_token_prop", function(inst)
    if GLOBAL.TheWorld == nil or not GLOBAL.TheWorld.ismastersim
        or inst.components.updatelooper == nil then
        return
    end

    inst.components.updatelooper:AddOnUpdateFn(function(prop, dt)
        local queen = prop.target
        if queen == nil or not queen:IsValid() or not queen:HasTag("monkeyqueen")
            or queen.sg == nil or not queen.sg:HasStateTag("channel") then
            return
        end

        local x, _, z = queen.Transform:GetWorldPosition()
        local px, py, pz = prop.Transform:GetWorldPosition()
        local dx, dz = x - px, z - pz
        local distance = math.sqrt(dx * dx + dz * dz)
        if distance > 2 then
            local step = math.min(CURSE_PROP_EXTRA_SPEED * dt, distance - 1.9)
            prop.Transform:SetPosition(px + dx / distance * step, py, pz + dz / distance * step)
        end
    end)
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
