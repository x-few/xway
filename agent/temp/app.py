import asyncio
import aioredis
import os
import ujson as json
from aioredis.pubsub import Receiver
from aioredis.abc import AbcChannel

mpsc = Receiver()

def get_my_path():
    return os.path.dirname(os.path.realpath(__file__))


def load_config():
    my_path = get_my_path()
    config_path = "{}/../conf/config.json".format(my_path)

    with open(config_path) as f:
        config = json.load(f)
    print(config)
    return config



async def sync():
    while True:
        await asyncio.sleep(1)
        print(1)


async def sync2():
    while True:
        await asyncio.sleep(2)
        print(2)


async def sync3(ch):
    lst = []
    async for msg in ch.iter():
        lst.append(msg)
    print(lst)





async def subscribe_redis(redis, channels):
    res = await redis.subscribe(*channels)
    tsk = asyncio.ensure_future(sync3(ch))
    print(res)


async def main():
    # read config
    config = load_config()
    channels = config['redis']['channels']
    # create redis pool
    # redis = await aioredis.create_redis_pool('redis://localhost')
    redis = await aioredis.create_redis(config['redis']['address'])


    try:
        task1 = asyncio.create_task(subscribe_redis(redis, channels))
        task2 = asyncio.create_task(sync())

        await task1
        await task2
    except:
        if redis.in_pubsub:
            await redis.unsubscribe(*channels)
        redis.close()
        await redis.wait_closed()


if __name__ == '__main__':
    # thread.start_new_thread(sync, ())
    asyncio.run(main())
