#!/usr/local/services/python3/bin/python3
#encoding:utf-8
import asyncio
import faust
import ujson as json
import os
import sys
import tracemalloc
import traceback
import datetime
import converter
import logging
from aioelasticsearch import Elasticsearch
from esops import create_update_index_templates


def get_my_path():
    return os.path.dirname(os.path.realpath(__file__))


def load_config():
    my_path = get_my_path()
    config_path = "{}/../conf/config.json".format(my_path)

    with open(config_path) as f:
        config = json.load(f)
    print(config)
    return config


def is_valid_config(conf):
    if conf is None:
        return False, "invalid config"
    if "app" not in conf:
        return False, "invalid app config"
    if "es" not in conf:
        return False, "invalid es config"
    return True


config = load_config()
if not is_valid_config(config):
    print("invalid config: {}".format(config))
    sys.exit(0)

app_config = config['app']
app = faust.App(**app_config)
attack_log_topic = app.topic(config['attack_log_topic'], value_serializer='raw') # value_type=AttackLog) #

# concurrency：并发量
@app.agent(attack_log_topic) #, concurrency=config['concurrency'])
async def attack_log_converter(stream):
    """
    攻击日志转换器。批量进行。
    :param stream: kafka 流
    :return: 无
    """
    index_prefix = config['to_es']['index_prefix']
    doc_type = config['to_es']['doc_type']
    index = "{}{}".format(index_prefix, datetime.datetime.today().strftime("%Y%m%d"))

    # index 不用指定ID
    # create 需要指定ID
    metadata = {
        "index": {
            "_index": index,
            "_type": doc_type
        }
    }

    async for logs in stream.take(config['batch_size'], within=config['batch_second']):
        logging.info("length: {}, logs: {}".format(len(logs), logs))
        es_logs = []
        for log in logs:
            log = json.loads(log)
            logging.warning(log)

            es_log = converter.convert_attack_log(log)
            es_logs.append(metadata)
            es_logs.append(es_log)
        await log_to_es(es_logs, index, doc_type)
        del es_logs

# @app.timer(interval=config['to_es']['interval'])
async def log_to_es(logs, index, doc_type):
    """
    日志入库 ES。
    :param logs: 攻击日志
    :param index: 索引
    :param doc_type: 文档类型
    :return: True or False
    """
    if not list or not isinstance(logs, list):
        return False, "invalid logs"

    try:
        async with Elasticsearch(**config['es']) as es:
            logging.info("doc_type: {}, index: {}".format(doc_type, index))
            res = await es.bulk(body=logs, index=index, doc_type=doc_type)
            logging.info("result: {}".format(res))
    except Exception as e:
        traceback.print_exc()
    finally:
        pass
    return True


"""
@app.task
async def on_startup(app):
    print('STARTING UP: %r' % (app,))
"""


if __name__ == '__main__':
    if "debug" in config and config['debug']:
        tracemalloc.start(10)

    if 'templates' in config and 'es' in config:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(create_update_index_templates(config['es'], config['templates']))

    app.main()
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(app.start())

