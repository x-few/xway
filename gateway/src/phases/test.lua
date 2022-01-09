
local js = require("cjson.safe")
local request = require("http.request")

local function test()
    -- 获取请求、解析请求——方便提取字段&比较
    local reqobj = request:new()
    reqobj:parse()
    ngx.say("request: ", js.encode(reqobj))
end

test()
