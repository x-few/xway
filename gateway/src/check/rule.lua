local js = require("cjson.safe")

local common = require("common")
local define = require("define")
local logic = require("check.logic")

local _M = { _VERSION = "1.0.0" }


-- TODO
-- 1. 支持IP段
-- 2. 支持IPv6
local function get_target_ip(request, key)
    return request:get_client_ip()
end

local function get_target_header(request, key)
    return request:get_headers(key)
end

local function get_target_uri_arg(request, key)
    return request:get_uri_args(key)
end

local function get_target_post_arg(request, key)
    ngx.log(ngx.INFO, "-----isshe----: get_target_post_arg---")
    return request:get_post_args(key)
end

local function get_target_keys(src_table)
    local res = {}
    if not common.is_table(src_table) then
        return res
    end
    for k, _ in pairs(src_table) do
        table.insert(res, k)
    end
    return res
end

local function get_target_header_keys(request, key)
    return get_target_keys(request:get_header())
end

local function get_target_uri_arg_keys(request, key)
    return get_target_keys(request:get_uri_args())
end

local function get_target_post_arg_keys(request, key)
    return get_target_keys(request:get_post_args())
end

local function get_target_method(request, key)
    return request:get_method()
end

local function get_target_uri(request, key)
    return request:get_uri()
end

local function get_target_request_uri(request, key)
    return request:get_request_uri()
end

local function get_target_area(request, key)
    local client_ip = request:get_client_ip()
    -- 获取client_ip的地域
    local ipdb = iwaf:get_ipdb()
    local info = ipdb:find(client_ip, "CN")
    local area = {
        country = info["country_name"],
        city = info["city_name"],
    }
    return area
end


local target_functions = {
    ip = get_target_ip,
    -- cookie = get_target_cookie,
    -- content_type = get_target_content_type,
    -- user_agent = get_target_user_agent,
    uri = get_target_uri,
    request_uri = get_target_request_uri,
    -- referer = get_target_refer,
    http_method = get_target_method,
    header = get_target_header,
    header_keys = get_target_header_keys,
    area = get_target_area,
    uri_arg_keys = get_target_uri_arg_keys,
    uri_arg = get_target_uri_arg,
    post_arg_keys = get_target_post_arg_keys,
    post_arg = get_target_post_arg,
}

local function get_target_function(type)
    return target_functions[string.lower(type)]
end

local function get_target_content(request, type, key)
    local func = get_target_function(type)
    return func(request, key)
end

local function is_supported_type(type)
    if type and get_target_function(type) then
        return true
    end
    return false
end

local function is_valid_condition(cond)
    if not common.is_table(cond) then
        return false, "condition info is not table"
    end

    if not common.is_table(cond.type) then
        return false, "invalid match type"
    end

    for _, type in ipairs(cond.type) do
        if not is_supported_type(type) then
            return false, "invalid match type: " .. (type or "")
        end
    end


    if not common.is_string(cond.pattern) then
        return false, "invalid condition pattern"
    end

    return true
end

local function is_valid_rule(rule)
    if not common.is_table(rule) then
        return false, "rule is not table"
    end

    if not common.is_table(rule.conditions) then
        return false, "condition is not table"
    end

    if not define.is_valid_relationship(rule.relationship) then
        return false, "invalid relationship"
    end
    -- TODO 检查其他参数

    return true
end


local function generate_match_info(request, rule, mctt)
    return {
        --[[
        client_ip = request:get_client_ip(),
        server_host = request:get_server_name(),
        server_port = request:get_server_port(),
        rule_id = rule.id,
        rule_type = rule.type,
        rule_action = rule.action,
        rule_severity = rule.severity,
        ]]
        --request = request,
        rule = rule,
        mctt = mctt,
    }
end

local function match_condition(request, condition)
    ngx.log(ngx.INFO, "condition = ", js.encode(condition))
    local res, err = is_valid_condition(condition)
    if not res then
        return nil, err
    end

    local mres, content, err
    for _, type in ipairs(condition.type) do
        content, err = get_target_content(request, type, condition.key)
        ngx.log(ngx.INFO, string.format("type = %s, content = %s", type, js.encode(content)))
        mres, err = content and logic.do_match(content, condition.logic, condition.pattern)
        if not mres and err then
            return nil, err
        end
        if mres then
            ngx.log(ngx.INFO, string.format("attack info = %s", js.encode(mres)))
            return mres
        end
    end

    return nil
end

local function match_and(request, rule)
    local mctt = {}
    for _, condition in ipairs(rule.conditions) do
        local mres, err = match_condition(request, condition)
        if not mres then
            if err then
                ngx.log(ngx.ERR, "match rule error: ", err)
                return nil, err
            end
            -- and的关系，直接返回不匹配
            return false
        end
        table.insert(mctt, mres)
    end
    return mctt
end

local function match_or(request, rule)
    for _, condition in ipairs(rule.conditions) do
        local mres, err = match_condition(request, condition)
        if mres then
            return { mres }
        end

        if not mres and err then
            ngx.log(ngx.ERR, "match rule error: ", err)
            return nil, err
        end
    end
    return false
end


function _M.match_rule(request, rule)
    -- TODO 考虑规则校验放到规则加载/下发的地方，减轻匹配的负担。
    local res, err = is_valid_rule(rule)
    if not res then
        ngx.log(ngx.ERR, "match rule error: ", err or "")
        return nil, err or "invalid rule"
    end

    -- 当前只支持and和or两种关系，如果
    local mctt, err = nil, nil
    if define.is_and_relationship(rule.relationship) then
        mctt, err = match_and(request, rule)
    else
        mctt, err = match_or(request, rule)
    end

    return mctt, err
end

function _M.match(request, rules)
    for _, rule in ipairs(rules) do
        local mctt, err = _M.match_rule(request, rule)
        if not mctt and err then
            return nil, err
        end

        if mctt then
            return generate_match_info(request, rule, mctt)
        end
    end
    return nil
end

return _M