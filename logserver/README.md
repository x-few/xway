# log-converter
log converter for iwaf

# 需求
* 使用消费者组，支持高可用。（起多个容器）

# 参考
* https://faust.readthedocs.io/en/latest/userguide/index.html


# DONE
* 订阅 kafka
* 写入 es
* 策略：批次获取 kafkka 信息，写入 es。
* 初始化 es：当没有索引模板时，就创建。


# TODO


# Faust目录结构
```
+ proj/
    - setup.py
    - MANIFEST.in
    - README.rst
    - setup.cfg

    + proj/
        - __init__.py
        - __main__.py
        - app.py

        + users/
        -   __init__.py
        -   agents.py
        -   commands.py
        -   models.py
        -   views.py

        + orders/
            -   __init__.py
            -   agents.py
            -   models.py
            -   views.py
```