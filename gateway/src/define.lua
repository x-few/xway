
local _M = { _VERSION = "1.0.0" }

_M.ACTIONS = {
    deny = "deny",              -- 拒绝/黑名单
    allow = "allow",            -- 允许/白名单
    log = "log",                -- 记录日志
    frequency = "frequency",    -- 限制访问频率
    captcha = "captcha",        -- 验证码
    default = "default",
}

function _M.is_action(action, target_action)
    if string.lower(action) == target_action then
        return true
    end
    return false
end

function _M.is_valid_action(action)
    if _M.ACTIONS[action] then
        return true
    end
    return false
end

function _M.is_action_deny(action)
    return _M.is_action(action, "deny")
end

function _M.is_action_allow(action)
    return _M.is_action(action, "allow")
end

function _M.is_action_log(action)
    return _M.is_action(action, "log")
end

function _M.is_action_frequency(action)
    return _M.is_action(action, "frequency")
end

_M.SEVERITY = {
    high = "high",
    normal = "normal",
    low = "low",
}

_M.RELATIONSHIP = {}
_M.RELATIONSHIP["and"] = "and"
_M.RELATIONSHIP["or"] = "or"


function _M.is_valid_relationship(relationship)
    if _M.RELATIONSHIP[relationship] then
        return true
    end
    return false
end

function _M.is_and_relationship(relationship)
    if "and" == relationship then
        return true
    end
    return false
end

function _M.is_or_relationship(relationship)
    if "or" == relationship then
        return true
    end
    return false
end


_M.LOGIC = {
    equal = "equal",
    contain = "contain",
    in_area = "in_area", -- 在区域中
    regex = "regex",    -- 正则表达式
}

_M.CONDITION_TYPE = {
    ip = true,
    area = true,
    uri = true,
    request_uri = true,
    -- uri_raw = true,     -- equal to request_uri
    -- uri_arg_raw = true,     -- eq request_uri
    uri_arg = true,
    uri_arg_keys = true,
    post_arg = true,
    post_arg_keys = true,
    -- post_arg_values = true,
    header = true,
    header_keys = true,
    -- header_values = true,
    cookie = true,
    cookie_keys = true,
    -- cookie_values = true,
}

_M.CATEGORY = {
    CC = "CC攻击",
    IP_BLACK = "IP黑名单",
    IP_WHITE = "IP白名单",
    AREA = "地域封禁",
    SQL_INJECTION = "SQL注入攻击",
    XSS = "跨站脚本攻击",
    CSRF = "跨站请求伪造",
    UNKNOWN = "未知攻击"
}

function _M.is_cc_category(category)
    if string.upper(category) == "CC" then
        return true
    end
    return false
end

return _M

