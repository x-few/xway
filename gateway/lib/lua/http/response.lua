local _M = {
    _VERSION="1.0.0",
    HTTP_FORBIDDEN = ngx.HTTP_FORBIDDEN,
    HTTP_NOT_FOUND = ngx.HTTP_NOT_FOUND,
}

function _M.response(status, content, headers)
    ngx.status = status

    if type(content) == "string" then
        ngx.header.content_type = 'text/html; charset=utf-8';
        ngx.header.content_length = string.len(content) -- + 1
    end

    for k, v in pairs(headers or {}) do
        ngx.header[k] = v
    end

    local _ = content and ngx.say(content)
    return ngx.exit(status)
end


return _M