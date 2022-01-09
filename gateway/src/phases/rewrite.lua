local js = require("cjson.safe")
local request = require("http.request")

local function rewrite()
    --ngx.log(ngx.ERR, "---isshe---rewrite---")
    local reqobj = request:new()
    reqobj:parse()
    ngx.log(ngx.INFO, "new request: ", js.encode(reqobj))
    ngx.ctx.request = reqobj
end

local function except(msg)
    ngx.log(ngx.ERR, msg)
end

xpcall(rewrite, except)