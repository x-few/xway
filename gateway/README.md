
[TOC]

iwaf
---
基于 OpenResty 的 waf 防护引擎。

# 规则
## 用户规则
* 动作：频率、拦截、放行、观察、重定向、人机识别（验证码）
* 识别位置：
  * HTTP 头部
  * HTTP 参数
  * 源 IP
  * 目的 IP
  * 地域
  * ...
* 攻击类型：（下拉框选择，靠用户自觉）
    * CC攻击
    * 地域封禁
    * SQL 注入
    * XSS
    * ...
    * 其他

## 内置规则
* 动作：拦截
* 识别位置：同上
* 攻击类别：
  * sql 注入
  * xss
  * ...

# TODO
* 规则匹配——核心。
    * 用户自定义白名单
    * CC规则
    * 地域规则
    * 用户自定义黑名单
    * 内置规则

# DOING
* protection_list下发保存。

# DONE
* 规则优先级
* CC规则
* 基础规则匹配

# Others
* 优先级
   * 数值越小优先级越高
   * 数值相同，旧的优先级高——规则ID小。

# 疑问
* 如何处理CC规则？如何处理最近一段时间的问题？
  * 保存这段时间内的所有访问
    * OpenResty shared_dict 的 list
    * redis 的 list。
* 哪些东西需要加载到全局的共享内存？
  * 基础规则：独占
  * 防护域名列表：独占
  * 用户规则：独占
    * 如果放不下怎么办？
