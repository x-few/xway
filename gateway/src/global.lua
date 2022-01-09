--[[
if IWAF then
    return IWAF
end
]]

local js = require("cjson.safe")
local common = require("common")

local _M = { _VERSION = "1.0.0" }
local mt = { __index = _M }

function _M:new()
    local obj = {
        root_dir = nil,
        protection_list = nil,
        config = nil,
        ipdb = nil,
        htmls = nil,
        kafka_producers = {},
    }

    return setmetatable(obj, mt)
end

function _M:set_root_dir(dir)
    self.root_dir = dir
end

function _M:get_root_dir()
    return self.root_dir
end

function _M:set_config(config)
    self.config = config
end

function _M:get_config(key)
    if not key then
        return self.config
    end
    return self.config[key]
end

function _M:set_ipdb(db)
    self.ipdb = db
end

function _M:get_ipdb()
    return self.ipdb
end

function _M:set_protection_list(list)
    self.protection_list = list
end

function _M:add_protection_list(host)
    if not self.protection_list then
        self.protection_list = {}
    end
    table.insert(self.protection_list, host)
end

function _M:in_protection_list(target_host)
    ngx.log(ngx.INFO, "target_host = ", target_host)
    ngx.log(ngx.INFO, "protection_list = ", js.encode(self.protection_list))
    if not target_host then
        return nil, "invalid host"
    end

    if not common.is_table(self.protection_list) then
        return nil, "protection_list is invalid"
    end

    for _, host in ipairs(self.protection_list) do
        if host == target_host then
            return true
        end
    end
    return false
end

function _M:set(key, value)
    if not common.is_string(key) or common.is_empty(key) then
        return nil, "key is not string or empty"
    end

    self[key] = value
end

function _M:get(key)
    return self[key]
end

function _M:set_html(key, content)
    if not self.htmls then
        self.htmls = {}
    end
    self.htmls[key] = content
end

function _M:get_html(key)
    if not key then
        return self.htmls
    end
    return self.htmls[key]
end

-- 预期是每个 worker 一个
function _M:get_kafka_producer()
    local worker_id = ngx.worker.id()
    ngx.log(ngx.INFO, "----isshe---: get kafka producer: " .. (js.encode(worker_id) or ""))
    return self.kafka_producers[worker_id]
end

function _M:set_kafka_producer(pd)
    local worker_id = ngx.worker.id()
    ngx.log(ngx.INFO, string.format("----isshe---: set kafka producer: %s", js.encode(worker_id) or "???"))
    self.kafka_producers[worker_id] = pd
end

return _M