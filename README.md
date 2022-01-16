# xway

A complete gateway solution.

# Feature

- Cloud Native
- Management Console
- Load Balancer
- API Gateway
- WAF

# Component Structure

- Console
    - frontend: vue3
    - backend: fastapi(python)
- Gateway
    - gateway: openresty
    - agent: golang
    - logclient: filebeat, send logs to `msgqueue` or `Log Center`.
- Log Center
    - logserver: gin(golang), save logs to database.
- Cache
    - cache: etcd/redis, caching configuration.
- Message Queue (Optional)
    - msgqueue: kafka, caching logs.

# Others

- github project: https://github.com/orgs/x-few/projects/3
- structure diagram: https://www.processon.com/view/link/5f20e0db1e08533a628cdec6
- detailed design: https://docs.qq.com/doc/DRWZ3eG9aTlFWS2tj
- web ui: https://app.mockplus.cn/s/pMpk9FZDqWv