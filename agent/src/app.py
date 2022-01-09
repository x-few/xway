import os
import sys
import redis
import ujson as json
from timer_task import TimerTask


def get_my_path():
    return os.path.dirname(os.path.realpath(__file__))


def load_config():
    my_path = get_my_path()
    config_path = "{}/../conf/config.json".format(my_path)

    with open(config_path) as f:
        cfg = json.load(f)
    print(cfg)
    return cfg


gdata = False


def redis_comsumer(item):
    global gdata
    gdata = True
    print(item)
    print(gdata)


def notifier():
    global gdata
    if gdata:
        gdata = False
        print("notifier...")


if __name__ == '__main__':
    config = load_config()
    redis_config = config['redis']
    channels = config['channels']
    interval = config['interval']
    tk = TimerTask(interval, notifier)
    rds = None
    pubsub = None

    try:
        tk.start()
        rds = redis.Redis(**redis_config)
        pubsub = rds.pubsub()
        pubsub.subscribe(channels)
        for item in pubsub.listen():
            redis_comsumer(item)
    except KeyboardInterrupt:
        print("except:", sys.exc_info()[0])
    finally:
        print("finally...")
        tk.cancel()
        if pubsub:
            pubsub.unsubscribe(channels)
            pubsub.close()
        if rds:
            rds.close()
    # Timer(3, notifier, ()).start()
