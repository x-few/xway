-- 任务：全局的初始化、加载配置、加载WAF规则
-- 第三方库
local js = require("cjson.safe")
local lfs = require("lfs")
-- 自定义库
local common = require("common")
local file = require("file")
local shm_base_rules = require("shm.base_rules")
local shm_user_rules = require("shm.user_rules")
local global = require("global")
local ipdb_city = require("resty.ipdb.city")
local define = require("define")

-- 唯一的自定义全局变量
iwaf = global:new()

local function load_iwaf_config()
    local path = string.format("%s/conf/config.json", common.get_root_dir())
    iwaf:set_config( file.read_json(path))
    if not iwaf:get_config() then
        ngx.log(ngx.ERR, "load iwaf config failed!")
        return false
    end
    return true
end

local function cmp_rule_priority(ra, rb)
    if not (common.is_table(ra) and common.is_table(rb)) then
        return false
    end

    if ra.priority == rb.priority then
        -- compare id
        return (ra.id < rb.id)
    end

    return (ra.priority < rb.priority)
end

local function get_enabled_rules(rules)
    if not common.is_table(rules) then
        return nil
    end

    local res = {}
    for _, rule in ipairs(rules) do
        if rule.enable == 1 then
            table.insert(res, rule)
        end
    end

    return res
end

local function load_base_rules()
    -- 加载基础规则到nginx共享内存
    -- 注意：只加载有效的
    -- 当前读文件，后续如果存在其他地方，再去其他地方读取
    -- 多个规则文件，则遍历读。
    local path = string.format("%s/rules/base.json", common.get_root_dir())
    local rules = file.read_json(path)
    if not rules then
        ngx.log(ngx.ERR, "load base rules failed")
        return nil, "load base rules failed"
    end

    local enabled_rules = get_enabled_rules(rules)
    if not enabled_rules then
        local estr = "get enabled rules failed"
        ngx.log(ngx.ERR, estr)
        return nil, estr
    end

    -- 整理优先级，方便后面的匹配：根据ID及priority来整理。
    table.sort(enabled_rules, cmp_rule_priority)
    for _, rule in ipairs(enabled_rules) do
        ngx.log(ngx.DEBUG, string.format("rule id = %s, priority = %s", rule.id, rule.priority))
    end

    shm_base_rules.set_json(enabled_rules)
    return true
end



local function load_user_rules()
    -- 加载域名或者IP的规则
    -- 考虑要不要增加端口作为key
    -- 当前也存在文件，后续修改为下发的形式
    local path = string.format("%s/rules/user.json", common.get_root_dir())
    local all_host_rules = file.read_json(path)
    ngx.log(ngx.DEBUG, "---isshe--- load_user_rules rules = ", js.encode(all_host_rules))
    if not all_host_rules then
        ngx.log(ngx.ERR, "load base rules failed")
        return nil, "load base rules failed"
    end

    for host, rules in pairs(all_host_rules) do
        local enabled_rules = get_enabled_rules(rules)
        if not enabled_rules  then
            local estr = "get enabled rules failed"
            ngx.log(ngx.ERR, estr)
            return nil, estr
        end
        shm_user_rules.set_host_rules_json(host, enabled_rules)
    end

    return true
end

-- 当前还是使用ngx的log，后续需要再完善部分
local function load_iwaf_rules()
    -- TODO
    load_base_rules()
    load_user_rules()
end

-- load protection list
local function load_iwaf_host()
    -- TODO
    local test_host = "www.test.com"
    iwaf:add_protection_list(test_host)
end

local function load_iwaf_ipdb()
    local path = string.format("%s/%s",
            iwaf:get_root_dir(), iwaf:get_config('ipdb'))
    local ipdb, err = ipdb_city:new(path)
    if not ipdb then
        return nil, "load ipdb error: " .. err or ""
    end
    iwaf:set_ipdb(ipdb)
end

local function init_iwaf_global()
    iwaf:set_root_dir(common.get_root_dir())
end

-- 加载 html 界面
local function load_iwaf_html()
    local html_path = iwaf:get_config("html")
    if not html_path then
        ngx.log(ngx.ERR, "get html config failed")
        return nil, "get html config faild" 
    end

    if not lfs.attributes(html_path) then
        local estr = string.format("html path is not exist: %s", html_path or "")
        ngx.log(ngx.ERR, estr)
        return nil, estr
    end

    for html_file in lfs.dir(html_path) do
        local key = string.match(html_file, "(.+).html")
        if key and define.ACTIONS[key] then
            local abs_file = string.format("%s/%s", html_path, html_file)
            local content, err = file.read(abs_file)
            if not content then
                ngx.log(ngx.WARN, string.format("read %s error: %s", content, err or ""))
            else
                iwaf:set_html(define.ACTIONS[key], content)
            end
        end
    end
end


local function init()
    init_iwaf_global()
    load_iwaf_config()
    load_iwaf_host()
    load_iwaf_rules()
    load_iwaf_ipdb()
    load_iwaf_html()
end

local function except(msg)
    --ngx.log(ngx.ERR, msg)
    --log.error(msg)
end

init()

-- xpcall(init, except)


