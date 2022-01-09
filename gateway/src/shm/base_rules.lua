--[[
存基础/内置规则
]]

local js = require("cjson.safe")

local _M = {
    _VERSION = "1.0.0",
    SHM_DICT_NAME = "base_rules",
    SHM_BR_KEY = "base"
}

function _M.get()
    return ngx.shared[_M.SHM_DICT_NAME]:get(_M.SHM_BR_KEY)
end

function _M.get_json()
    local rules = _M.get()
    return js.decode(rules)
end


function _M.set(rules_str)
    return ngx.shared[_M.SHM_DICT_NAME]:set(_M.SHM_BR_KEY, rules_str)
end

function _M.set_json(rules)
    return _M.set(js.encode(rules))
end

return _M