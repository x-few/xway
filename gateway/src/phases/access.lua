
local js = require("cjson.safe")
local request = require("http.request")
local base = require("check.base")
local user = require("check.user")
local actions = require("actions")

local function access()
    -- 获取请求、解析请求——方便提取字段&比较
    local reqobj = ngx.ctx.request

    if request:is_local_request() then
        return
    end

    -- host需要和 server 相同
    if not request:is_valid_request() then
        return actions.forbidden()
    end

    -- 检查是否在防护host列表
--    if not iwaf:in_protection_list(reqobj:get_server_name()) then
--        return actions.not_found()
--    end

    -- 匹配用户规则
    local minfo, err = nil, nil
    minfo, err = minfo or user.check(reqobj)
    if not minfo and err then
        ngx.log(ngx.ERR, "check user white rule error: ", err)
    end
    
    -- 匹配基础规则
    minfo, err = minfo or base.check(reqobj)
    if not minfo and err then
        ngx.log(ngx.ERR, "check base rule error: ", err)
    end

    -- do action
    if minfo then
        ngx.log(ngx.DEBUG, "matched info: ", js.encode(minfo))
        ngx.ctx.minfo = minfo
        actions.do_action(minfo)
    else
        ngx.log(ngx.DEBUG, "No rules match.")
    end
end

local function except(msg)
    ngx.log(ngx.ERR, "except message: ", msg)
    ngx.log(ngx.ERR, "except traceback: ", debug.traceback())
end

access()
--xpcall(access, except)
