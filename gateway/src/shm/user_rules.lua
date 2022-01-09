--[[
存所有的用户规则
]]

local js = require("cjson.safe")

local _M = {
    _VERSION = "1.0.0",
    SHM_DICT_NAME = "user_rules",
}

-- host 的有效性在外部进行校验
function _M.get_host_rules_string(host)
    return ngx.shared[_M.SHM_DICT_NAME]:get(host)
end

function _M.set_host_rules_string(host, rules_str)
    return ngx.shared[_M.SHM_DICT_NAME]:set(host, rules_str)
end

function _M.get_host_rules_json(host)
    local rules_str = _M.get_host_rules_string(host)
    return js.decode(rules_str)
end

function _M.set_host_rules_json(host, rules)
    local rules_str = js.encode(rules)
    return _M.set_host_rules_string(host, rules_str)
end


return _M