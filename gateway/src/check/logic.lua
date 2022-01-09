local js = require("cjson.safe")

local common = require("common")

local _M = { _VERSION = "1.0.0" }

function _M.equal(content, pattern)
    if content == pattern then
        return content
    end
    return nil
end

function _M.contain(content, pattern)
    return string.match(content, pattern)
end


--[[
规则|客户IP  C存c存    C存c不    C不c存    C不c不
C存c存        配     空配/非不    -        -
C存c不        配       配        -        -
C不c存        -        -         -        -
C不c不        -        -         -        -
]]

function _M.in_area(content, pattern)
    local rule_area_map = js.decode(pattern)
    if not (rule_area_map and content) then
        return nil, "invalid content/pattern"
    end

    ngx.log(ngx.DEBUG, "logic_in_area content = ", js.encode(content))
    ngx.log(ngx.DEBUG, "logic_in_area pattern = ", pattern)
    local client_country = content.country
    if not client_country
            or common.is_empty(client_country)
            or not rule_area_map[client_country] then
        ngx.log(ngx.WARN, "area ban rule invalid or get client ip failed")
        return nil
    end

    -- 国家已匹配上，下面匹配城市
    local provinces = rule_area_map[client_country]
    if common.is_empty(provinces) then
        -- 没有指定城市，那就封国家
        return client_country
        -- return true
    end

    -- 指定了城市
    -- 检查城市是否空
    local client_city = content.city
    if common.is_empty(client_city) then
        -- 获取客户IP的城市失败了，为了避免误判，就不封
        return nil
    end

    -- 一个一个对比
    for _, city in ipairs(provinces) do
        if city == client_city then
            return string.format("%s-%s", client_country, client_city)
            -- return true
        end
    end

    return nil
end


function _M.regex(content, pattern)
    local url_decode_content = ngx.unescape_uri(content)
    ngx.log(ngx.INFO, "---isshe---: content = " .. content .. " pattern = " .. (pattern or ""))
    local from,to,err = ngx.re.find(url_decode_content, pattern, "io")
    if from then
        local hit_data = string.sub(url_decode_content, from, to)
        ngx.log(ngx.INFO, "attack data = " .. (hit_data or ""))
        --[[
        if #hit_data >= 512 then
            hit_data = string_sub(url_decode_content,from,to)
        end
        ]]
        return hit_data
    end
    return nil
end


function _M.do_match(content, logic, pattern)
    logic = string.lower(logic)
    local func = _M[logic]
    if not func then
        estr = "unsupport logic operation: " .. (logic or "")
        ngx.log(ngx.ERR, estr)
        return nil, estr 
    end

    if common.is_table(content) then
        for _, ctt in pairs(content) do
            local res, err = func(ctt, pattern)
            if not res and err then
                return res, err
            end
            if res then
                return res
            end
            -- else continue
        end
    else
        return func(content, pattern)
    end
    return nil
end

return _M