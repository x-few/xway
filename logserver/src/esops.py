import logging
import ujson as json
import os
import traceback
from aioelasticsearch import Elasticsearch

def get_my_path():
    """
    获取当前文件所在的路径
    :return:
    """
    return os.path.dirname(os.path.realpath(__file__))

def gen_v6_template(info):
    if 'doc_type' not in info \
            or 'index_patterns' not in info \
            or 'properties' not in info:
        return False, "Invalid info"

    pt = {
        "index_patterns": info['index_patterns'],
        "settings": info['settings'],
        "mappings": {
            info['doc_type']: {
                "properties": info['properties']
            }
        }
    }
    return pt

def gen_v7_template(info):
    if 'index_patterns' not in info \
            or 'properties' not in info:
        return False, "Invalid info"

    settings = {}
    if 'setting' in info:
        settings = info['settings']
    aliases = {}
    if 'aliases' in info:
        settings = info['aliases']

    pt = {
        "index_patterns": info['index_patterns'],
        "template": {
            "settings": settings,
            "mappings": {
                "properties": info['properties']
            },
            "aliases": aliases
        }
    }

    if 'others' in info:
        for k, v in info['others'].items():
            pt[k] = v

    return pt

async def get_es_version(es):
    """
    获取 es 服务器的大版本，当前只支持两个版本
    :param es: es 对象
    :return: 6 或 7
    """
    esinfo = await es.info()
    if isinstance(esinfo, dict) \
            and 'version' in esinfo \
            and esinfo['version']['number'].startswith('7.'):
        return 7
    return 6

async def create_es():
    """
    后续测试一下，使用一个 es 实例好还是每次都开好。
    :return:
    """
    # TODO
    pass

async def destroy_es(es):
    # TODO
    pass


async def create_update_index_templates(config, tpfile):
    """
    创建或者是更新索引模板。
    :param config: es 的配置
    :param tpfile: 模板文件
    :return: 无
    """
    try:
        async with Elasticsearch(**config) as es:
            print(await es.info())
            template_file = "{}/../{}".format(get_my_path(), tpfile)
            with open(template_file) as f:
                infos = json.load(f)
            version = await get_es_version(es)
            for name, info in infos.items():
                print(name, info)
                if version == 6:
                    print("generating es6 tamplate: {}".format(name))
                    pt = gen_v6_template(info)
                else:
                    print("generating es7 tamplate: {}".format(name))
                    pt = gen_v7_template(info)
                if not pt:
                    return False, "generate index template failed"
                print("create index template: {}, {}".format(name, pt))
                res = await es.indices.put_template(name=name, body=pt) #, create=True)
                print("create index template result: {}".format(res))
    except Exception as e:
        traceback.print_exc()
    finally:
        pass