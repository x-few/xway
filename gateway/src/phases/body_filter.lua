
local function body_filter()

end

local function except(msg)
    ngx.log(ngx.ERR, msg)
end

xpcall(body_filter, except)