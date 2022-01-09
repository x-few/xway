--[[
存cc规则的中间状态
]]

local js = require("cjson.safe")

local _M = {
    _VERSION = "1.0.0",
    SHM_DICT_NAME = "frequency",
    SHM_CC_PUNISHMENT_KEY = "punishment"
}

function _M.get(key)
    return ngx.shared[_M.SHM_DICT_NAME]:get(key)
end

function _M.set(key, value)
    return ngx.shared[_M.SHM_DICT_NAME]:set(key, value)
end

function _M.get_punishment_key(key)
    if not key then
        return nil, "invalid key"
    end
    return string.format("%s-%s", key, _M.SHM_CC_PUNISHMENT_KEY)
end

function _M.set_punishment(key, value)
    return ngx.shared[_M.SHM_DICT_NAME]:set(_M.get_punishment_key(key), value)
end

function _M.get_punishment(key)
    return ngx.shared[_M.SHM_DICT_NAME]:get(_M.get_punishment_key(key))
end

function _M.del_punishment(key)
    ngx.shared[_M.SHM_DICT_NAME]:delete(_M.get_punishment_key(key))
end

function _M.set_punishment_exptime(key, exptime)
    return ngx.shared[_M.SHM_DICT_NAME]:expire(_M.get_punishment_key(key), exptime)
end

function _M.rpush(key, value)
    return ngx.shared[_M.SHM_DICT_NAME]:rpush(key, value)
end

function _M.lpush(key, value)
    return ngx.shared[_M.SHM_DICT_NAME]:lpush(key, value)
end

function _M.lpop(key)
    return ngx.shared[_M.SHM_DICT_NAME]:lpop(key)
end

function _M.del(key)
    ngx.shared[_M.SHM_DICT_NAME]:delete(key)
end

function _M.length(key)
    return ngx.shared[_M.SHM_DICT_NAME]:llen(key)
end

function _M.expire(key, exptime)
    return ngx.shared[_M.SHM_DICT_NAME]:expire(key, exptime)
end

return _M