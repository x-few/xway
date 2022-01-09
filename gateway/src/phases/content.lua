local http = require("resty.http")
local js = require("cjson.safe")


local function to_source()
    local httpc = http.new()
    local url = ngx.ctx.to_source_uri
    ngx.log(ngx.DEBUG, "---isshe---to source url = ", url or "")
    ngx.log(ngx.DEBUG, "---isshe---to source ngx.header = ", js.encode(ngx.header) or "")
    local res, err = httpc:request_uri(url, {
        method = "GET",
        -- body = "a=1&b=2",
        -- headers = ngx.header,
    })

    if not res then
        ngx.say("failed to request: ", err)
        return
    end

    ngx.log(ngx.DEBUG, "---isshe---to source res = ", js.encode(res))

    -- In this simple form, there is no manual connection step, so the body is read
    -- all in one go, including any trailers, and the connection closed or keptalive
    -- for you.

    ngx.status = res.status
    for k,v in pairs(res.headers) do
        ngx.header[k] = v
    end

    ngx.say(res.body)
end


local function content()
    to_source()
end

local function except(msg)
    ngx.log(ngx.ERR, msg)
end

content()
-- xpcall(content, except)