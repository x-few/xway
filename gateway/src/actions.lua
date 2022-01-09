
local js = require("cjson.safe")

local shm_cc_limit = require("shm.frequency")
local resp = require("http.response")
local define = require("define")

local _M = { _VERSION = "1.0.0" }

function _M.not_found(content, headers)
    return resp.response(ngx.HTTP_NOT_FOUND, content, headers)
end

function _M.forbidden(content, headers)
    return resp.response(ngx.HTTP_FORBIDDEN, content, headers)
end

-- 也可以计算匹配条件的 md5 来生成唯一的 key，但是感觉会更耗性能，因此加个参数 magic。
local function get_rule_key(request, rule)
    -- host-port-client_ip-rule_id-rule_magic
    return string.format("%s-%s-%s-%s-%s",
            request:get_server_name(),
            request:get_server_port(),
            request:get_client_ip(),
            rule.id, rule.magic)
end

function _M.frequency(minfo)
    -- 如果mres存在，就意味着规则合法性什么都检测通过了，
    -- 下面不用检查规则的信息，直接用即可。
    local limit_key = get_rule_key(minfo.request, minfo.rule)
    ngx.log(ngx.DEBUG, "cc check: limit_key = ", limit_key)
    -- 检查是否正在惩罚中。是，检查是否惩罚完了。
    local now = ngx.now()
    local punishment, err = shm_cc_limit.get_punishment(limit_key)
    if punishment then
        if punishment > now then
            -- 还在惩罚中
            return minfo
        end

        -- 惩罚完了，删除记录
        shm_cc_limit.del_punishment(limit_key)
    elseif err then
        ngx.log(ngx.ERR, "get punishment error: ", err)
        return nil, err
    end

    -- 匹配，读取最近一段时间的请求次数
    -- 没有请求记录，就添加一个；有请求记录，就+1
    local limit_list_len, err = shm_cc_limit.length(limit_key)
    if not limit_list_len then
        ngx.log(ngx.ERR, "get shm_cc_limit item len failed")
        return nil, err
    end
    ngx.log(ngx.DEBUG, "cc check: limit_list_len = ", limit_list_len)

    local interval = minfo.rule.frequency.interval
    while limit_list_len > 0 do
        local time = shm_cc_limit.lpop(limit_key)
        if time > now - interval then
            shm_cc_limit.lpush(limit_key, time)
            break
        end
        limit_list_len = limit_list_len - 1
    end

    -- 没到达限制
    local rule_limit = minfo.rule.frequency.count
    if limit_list_len < rule_limit then
        shm_cc_limit.rpush(limit_key, now)
        if limit_list_len == 0 then
            -- 设置过期时间
            ngx.log(ngx.DEBUG, "cc check: set expire = ", interval)
            shm_cc_limit.expire(limit_key, interval)
        end
        return false
    end

    -- 设置惩罚
    local punishment_time = minfo.rule.frequency.punishment
    shm_cc_limit.set_punishment(limit_key, now + punishment_time)
    shm_cc_limit.set_punishment_exptime(limit_key, punishment_time)
    ngx.log(ngx.DEBUG, "cc check: set punishment expire = ", punishment_time)

    -- 删除记录
    shm_cc_limit.del(limit_key)

    return minfo
end

function _M.log(minfo)

end

function _M.do_action(minfo)
    local action = minfo.rule and minfo.rule.action
    ngx.log(ngx.DEBUG, "---isshe---: action = ", action or "")
    if not define.is_valid_action(action) then
        return _M.not_found(minfo)
    end

    if define.is_action_allow(action) then
        return true     -- do nothing
    elseif define.is_action_deny(action) then
        local content = iwaf:get_html(define.ACTIONS.deny)
        return _M.forbidden(content)
    elseif define.is_action_frequency(action) then
        if _M.frequency(minfo) then
            local content = iwaf:get_html(define.ACTIONS.frequency)
            return _M.forbidden(content)
        end
    elseif define.is_action_log(action) then
        return _M.log(minfo)
    else
        return _M.not_found(minfo)
    end
end


return _M