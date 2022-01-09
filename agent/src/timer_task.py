import threading
import time
import sys


class TimerTask(threading.Thread):
    def __init__(self, interval, callback, args=None):
        threading.Thread.__init__(self)
        if args is None:
            args = {}
        self.interval = interval
        self.callback = callback
        self.args = args
        self.stop = False

    def cancel(self):
        self.stop = True

    def run(self):
        if not self.callback:
            return
        try:
            while not self.stop:
                time.sleep(self.interval)
                self.callback(**self.args)
        except:
            print("timer task error:", sys.exc_info()[0])
