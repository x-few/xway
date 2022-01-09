-- 没有行号，考虑如何解决？

local _M = {_VERSION = "1.0.0"}

function _M.info(...)
    ngx.log(ngx.INFO, ...)
end

function _M.error(...)
    ngx.log(ngx.ERR, ...)
end

function _M.debug(...)
    ngx.log(ngx.DEBUG, ...)
end

return _M