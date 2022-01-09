local function header_filter()

end

local function except(msg)
    ngx.log(ngx.ERR, msg)
end

xpcall(header_filter, except)
