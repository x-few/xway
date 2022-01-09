
local shm_user_rules = require("shm.user_rules")
local chkrule = require("check.rule")

local _M = { _VERSION = "1.0.0" }

function _M.check(request)
    -- 读取地域封禁规则
    local rules, err = shm_user_rules.get_host_rules_json(request:get_server_name())
    if not rules then
        return nil, err
    end
    -- 规则匹配
    return chkrule.match(request, rules)
end

return _M