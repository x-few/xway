import redis
import threading
import sys


class RedisListener(threading.Thread):
    def __init__(self, channels, callback, host, port=6379, password=None, db=0):
        threading.Thread.__init__(self)
        self.callback = callback
        self.redis = redis.Redis(host=host, port=port, password=password, db=db)
        self.pubsub = self.redis.pubsub()
        self.pubsub.subscribe(channels)
        self.channels = channels

    def __del__(self):
        print("---del---")
        self.pubsub.unsubscribe(self.channels)
        self.pubsub.close()
        self.redis.close()

    def run(self):
        if not self.callback:
            return
        print("running...")
        try:
            for item in self.pubsub.listen():
                self.callback(item)
        except:
            print("redis listener error:", sys.exc_info()[0])
