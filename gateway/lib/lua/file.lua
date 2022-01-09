local js = require("cjson.safe")

local _M = {_VERSION = "1.0.0"}

function _M.size(fd)
    local current_pos = fd:seek()   -- 保存当前位置
    local size = fd:seek("end")     -- 获取文件大小
    fd:seek("set", current_pos)     -- 恢复当前位置
    return size
end

function _M.read(path, func)
    func = func and func or io.open
    local fp, err = func(path, "r")
    if not fp then
        return nil, err
    end
    local s = fp:read("*a")
    fp:close()
    return s
end

function _M.readall(path, func)
    return _M.read(path, func)
end

function _M.write(path, s)
    local fp, err = io.open(path, "w") 	assert(fp, err)
    fp:write(s)
    fp:flush()
    fp:close()
end

function _M.read_json(path)
    local json_str = _M.read(path)
    return js.decode(json_str)
end

function _M.write_json(path, json)
    local json_str = js.encode(json)
    _M.write(path, json_str)
end

return _M

