"""
+---+-----------+----------------+-----------+-------------+
| 0 | timestamp | data center id | worker id | sequence id |
+---+-----------+----------------+-----------+-------------+
| 1 |    41     |        5       |     5     |     12      |

"""

import time


# class InvalidSystemClock(Exception):
#     pass


WORKER_ID_BITS = 5
DATACENTER_ID_BITS = 5
SEQUENCE_BITS = 12
MAX_WORKER_ID = -1 ^ (-1 << WORKER_ID_BITS)  # 2**5-1 0b11111
MAX_DATACENTER_ID = -1 ^ (-1 << DATACENTER_ID_BITS)
WORKER_ID_SHIFT = SEQUENCE_BITS
DATACENTER_ID_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS
TIMESTAMP_LEFT_SHIFT = SEQUENCE_BITS + WORKER_ID_BITS + DATACENTER_ID_BITS
SEQUENCE_MASK = -1 ^ (-1 << SEQUENCE_BITS)

# 2021-01-01
TWEPOCH = 1609430400000


class IdWorker(object):
    def __init__(self, datacenter_id=1, worker_id=1, sequence=0):
        if worker_id > MAX_WORKER_ID or worker_id < 0:
            raise ValueError('bad worker_id')

        if datacenter_id > MAX_DATACENTER_ID or datacenter_id < 0:
            raise ValueError('bad datacenter_id')

        self.worker_id = worker_id
        self.datacenter_id = datacenter_id
        self.sequence = sequence

        self.last_timestamp = -1

    def get_timestamp(self):
        return int(time.time() * 1000)

    def until_next_millis(self, last_timestamp):
        timestamp = self.get_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self.get_timestamp()
        return timestamp

    def get_id(self):
        """
        获取新ID
        :return:
        """
        timestamp = self.get_timestamp()

        if timestamp < self.last_timestamp:
            # raise InvalidSystemClock
            timestamp = self.last_timestamp + 1
            # self.last_timestamp = timestamp

        elif timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & SEQUENCE_MASK
            if self.sequence == 0:
                # All sequence are used
                timestamp = self.until_next_millis(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        return ((timestamp - TWEPOCH) << TIMESTAMP_LEFT_SHIFT) | \
            (self.datacenter_id << DATACENTER_ID_SHIFT) | \
            (self.worker_id << WORKER_ID_SHIFT) | self.sequence


id_worker = None


def get_id():
    if id_worker is None:
        id_worker = IdWorker(1, 1)

    return id_worker.get_id()


if __name__ == '__main__':
    worker = IdWorker(1, 1)
    print(worker.get_id())
