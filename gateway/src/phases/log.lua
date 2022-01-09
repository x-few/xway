local js = require("cjson.safe")

local function generate_attack_log(request, match_info)
    local rule = match_info["rule"]
    local attack_content = match_info["mctt"]
    local attack_log =  {
        rule_id = rule.id,
        rule_action = rule.action,
        method = request:get_method(),
        uri = request:get_uri(),
        http_version = request:get_http_version(),
        attack_ip = request:get_client_ip(),
        server_host = request:get_server_name(),
        server_port = request:get_server_port(),
        attack_time = request:get_request_time(),
        attack_content = attack_content,
        attack_category = rule.category,
        attack_severity = rule.severity,
    }
    return attack_log
end

local function log()
    --local config = iwaf:get_config()
    --ngx.log(ngx.DEBUG, "---isshe---: iwaf.config = ", js.encode(config) or "")
    if ngx.ctx.minfo then
        local attacl_log = generate_attack_log(ngx.ctx.request, ngx.ctx.minfo)
        -- local minfo = ngx.ctx.minfo
        -- TODO log match info
        local pd = iwaf:get_kafka_producer()
        local kafka = iwaf:get_config("kafka")
        local topic = kafka['topic']
        local ok, err = pd:send(topic, "key", js.encode(attacl_log))
        if not ok then
            ngx.log(ngx.INFO, "send err:", err)
            return
        end

        ngx.log(ngx.INFO, "send success, ok:", ok)
    end
end

local function except(msg)
    ngx.log(ngx.ERR, msg)
end
log()
-- xpcall(log, except)