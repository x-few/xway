import ujson as json


def convert_attack_log(log):
    res = {}
    for k, v in log.items():
        res[k] = v
    # res["attack_content"] = log['attack_content']
    res['from_country'] = "中国"
    res['from_city'] = "北京",
    res['to_country'] = "中国"
    res['to_city'] = "深圳",

    return res