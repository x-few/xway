-- 进行一些针对每个worker的工作
local producer = require("resty.kafka.producer")
local common = require("common")
local js = require("cjson")

local function init_kafka_producer()
    local kafka = iwaf:get_config("kafka")
    local broker_list = kafka['brokers']
    if not common.is_table(broker_list) or not next(broker_list) then
        ngx.log(ngx.ERR, "init kafka producer error: invalid kafka config")
        return nil
    end
    ngx.log(ngx.INFO, string.format("kafka broker list: %s", js.encode(broker_list)))
    local kafka_config = {
        request_timeout = 20000,
        producer_type = "async",
    }
    local pd = producer:new(broker_list, kafka_config)
    if not pd then
        ngx.log(ngx.ERR, "init kafka producer error: new producer failed")
        return nil
    end
    
    iwaf:set_kafka_producer(pd)
end

local function subscribe_redis()
    local redis = require "resty.redis"
    local red = redis:new()
    red:set_timeouts(1000, 1000, 1000) -- 1 sec
    local ok, err = red:connect("35.194.129.162", 6379)
    if not ok then
        ngx.log(ngx.ERR, "1: failed to connect: ", err)
        return
    end
    local res, err = red:subscribe("dog")
    if not res then
        ngx.log(ngx.ERR, "1: failed to subscribe: ", err)
        return
    end

    ngx.log(ngx.ERR, "1: subscribe: ", js.encode(res))
    while true do
        res, err = red:read_reply()
        if not res then
            ngx.log(ngx.ERR, "1: failed to read reply: ", err)
            return
        end

        ngx.log(ngx.ERR, "1: receive: ", js.encode(res))
    end
    -- red:close()
    ngx.log(ngx.ERR, "---isshe---init redis finished...")
end


local function init_worker()
    init_kafka_producer()
    --subscribe_redis()
end

init_worker()