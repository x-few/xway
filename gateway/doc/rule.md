[TOC]

规则
---

# json结构
```json
    {
      "id": 2,
      "version": "1.0.0",
      "category": "cc",
      "desc": "IP黑名单",
      "action": "frequency",
      "expire": 1588574006,
      "frequency": {
        "count": 3,
        "interval": 30,
        "desc": "60s内可以访问10次",
        "punishment": 60,
        "punishment_desc": "惩罚时间，单位秒"
      },      
      "priority": 2,
      "conditions": [
        {
          "key": "",
          "pattern": "/abc",
          "logic": "contain",
          "type": "uri"
        }
      ],
      "relationship": "or",
      "severity": "high",
      "owner": "user",
      "magic": 3,
      "magic_desc": "cc规则依赖这个，因此编辑规则下发要自增这个值"
    }
```
* id: 规则ID，唯一。
    * 用户规则：小于`100,000,000`。
    * 基础规则：大于等于`100,000,000`。
* version: 规则版本。
* desc：规则描述
* action：规则的动作，预期`deny/allow/frequency/log`
* expire：规则过期时间
    * 未实现，可以在下发规则时实现，过期后的规则不下发。规则过期后重新发下新规则。
* frequency：`frequency`动作被指定时，需要这里的数据。
    * count/interval：interval秒内访问次数达到count次后，将被限制访问。
    * punishment：惩罚时间，单位`秒`
* priority: 优先级，优先级相同，则ID小的优先级高。
* conditions: 匹配条件
    * key: 匹配内容的键值。
    * pattern：匹配模式。
    * logic：匹配逻辑关系。
    * type：匹配的内容类型。
* relationship：条件间的关系。
* severity：严重程度。
* owner：规则所属，用户规则还是基础规则，`user/base`。
* magic：魔法数，每次配置下发时更新。
