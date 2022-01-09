
local js = require("cjson.safe")

local shm_base_rules = require("shm.base_rules")
local common = require("common")
local chkrule = require("check.rule")


local _M = { _VERSION = "1.0.0" }

function _M.check(request)
    ngx.log(ngx.DEBUG, "checking base rules...")
    local rules = shm_base_rules.get_json()
    if not common.is_table(rules) then
        ngx.log(ngx.ERR, "check base rule error: get rules failed")
        return nil, "check base rule error: get rules failed"
    end

    return chkrule.match(request, rules)
end

return _M