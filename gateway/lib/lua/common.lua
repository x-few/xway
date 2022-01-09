

local function get_root_dir()
    local script_path = debug.getinfo(1,'S').source:sub(2)
    ngx.log(ngx.INFO, "script_path = ", script_path or "");
    return script_path:match("^(.*)/lib/lua/common.lua$")
end

local function is_table(var)
    if type(var) == "table" then
        return true
    end
    return false
end

local function is_string(var)
    if type(var) == "string" then
        return true
    end
    return false
end

local function is_number(var)
    if type(var) == "number" then
        return true
    end
    return false
end

local function is_empty(var)
    if is_table(var) and not next(var) then
        return true
    end

    if is_string(var) and var == "" then
        return true
    end

    if is_number(var) and var == 0 then
        return true
    end

    return false
end

local function length(var)
    local len = 0
    if is_table(var) then
        for _ in pairs(var) do
            len = len + 1
        end
    else
        len = #var
    end
    return len
end


return {
    get_root_dir = get_root_dir,
    is_table = is_table,
    is_string = is_string,
    is_number = is_number,
    is_empty = is_empty,
    length = length,
}
