local js = require("cjson.safe")
local common = require("common")


local _M = { _VERSION="1.0.0" }
local mt = { __index = _M }

function _M.get(self, key, value)
    if not self[key] then
        self[key] = value
    end
    return self[key]
end

function _M.get_http_version(self)
    return self:get("http_version", ngx.req.http_version())
end

function _M.get_method(self)
    return self:get("method", ngx.req.get_method())
end

function _M.get_scheme(self)
    return self:get("scheme", ngx.var.scheme)
end

function _M.get_uri_args(self, key)
    local args = self:get("uri_args", ngx.req.get_uri_args())
    if not common.is_empty(key)
    and common.is_string(key)
    and common.is_table(args) then
        return args[key]
    end

    return args
end

function _M.get_post_args(self, key)
    if not self.post_args then
        ngx.req.read_body()     -- TODO think about this
        local post_args, err = ngx.req.get_post_args()
        if err then
            ngx.log(ngx.ERR, "get uri args error: ", err)
            return nil, err
        end
        self.post_args = post_args
    end

    if not common.is_empty(key)
    and common.is_string(key)
    and common.is_table(self.post_args) then
        return self.post_args[key]
    end

    return self.post_args
end

-- "/"
function _M.get_uri(self)
    return self:get("uri", ngx.var.uri)
end

-- "/?a=abc&b=bcd"
function _M.get_request_uri(self)
    return self:get("request_uri", ngx.var.request_uri)
end

function _M.get_client_ip(self)
    return self:get("client_ip", ngx.var.remote_addr)
end

function _M.get_host(self)
    ngx.log(ngx.DEBUG, "get header host = ", ngx.var.host)
    return self:get("host", ngx.var.host)
end

function _M.get_server_name(self)
    return self:get("server_name", ngx.var.server_name)
end

function _M.get_server_port(self)
    return self:get("server_port", ngx.var.server_port)
end

function _M.get_request_time(self)
    return self:get("request_time", ngx.req.start_time())
end

function _M.get_headers(self, key)
    local headers = self:get("headers", ngx.req.get_headers())
    if not common.is_empty(key)
    and common.is_string(key)
    and common.is_table(headers) then
        key = string.lower(key)
        return headers[key]
    end
    return headers
end

function _M.new(self)
    local obj = {
        request_time = nil,
        http_version = nil,
        method = nil,
        scheme = nil,
        headers = nil,
        raw_header = nil,
        uri_args = nil,
        post_args = nil,
        uri = nil,
        request_uri = nil,
        escape_uri = nil,
        unescape_uri = nil,
        server_name = nil,
        host = nil,
        server_port = nil,
        client_ip = nil,
        body = nil,
        body_file = nil,
    }

    return setmetatable(obj, mt)
end

function _M.parse(self)
    self:get_request_time()
    self:get_http_version()
    self:get_method()
    self:get_scheme()
    self:get_uri()
    self:get_uri_args()
    self:get_client_ip()
    self:get_host()
    self:get_server_name()
    self:get_server_port()
    self:get_headers()
    self:get_request_uri()
end

function _M.parse_all(self)
    self:get_post_args()
end

function _M.print(self)
    local str = ""
    for k, v in pairs(self.obj) do
        if v then
            str = string.format("%s%s = %s\n", str, k, v)
        end
    end

    return str
end

function _M.is_valid_request(self)
    local server_name = self:get_server_name()
    local host = self:get_host()
    if not (server_name and host) then
        return false
    end

    if server_name ~= host then
        return false
    end

    return true
end

function _M.is_local_request(self)
    local host = self:get_host()
    local client_ip = self:get_client_ip()
    if (host == "127.0.0.1" or host == "localhost") and client_ip == "127.0.0.1" then
        return true
    end

    return false
end

return _M
