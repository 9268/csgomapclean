
import requests
import json
import time
from xmltodict import parse
from collections import OrderedDict

import os

ENABLE_WORKER=os.environ.get("ENABLE_WORKER",False)
workers=None
if ENABLE_WORKER:
    from WorkersKV import WorkersKV
    workers = WorkersKV(
        account=os.environ['WORKER_ACCOUNT'],
        namespace=os.environ['WORKER_NAMESPACE']
    )
HEADER_ADD="made_by:mapCleaner_83506876@qq.com"

def set_fys():
    header = {
        'User-Agent': 'Fys Client v1.6.55.0 '+HEADER_ADD}
    r = requests.get('https://1mgou.com/client/api/IGetMaps/', headers=header)
    js = json.loads(r.text)
    conf = [{'name': j['file'],  'size':j['size'],
             'verify':j['hash'],  'verifyer':'crc32'} for j in js['array']]
    if ENABLE_WORKER:
        workers.put("风云社_maps", json.dumps({"maps": conf, "time": time.time()}))
    return conf


jsly = {
    "kz": {
        "api": "https://api.zombieden.cn/zedex_dl.php?map={prefix}{word}",
        "prefix": ["kz_"],
        "type": "round",
        "words": "1234567890qwertyuiopasdfghjklzxcvbnm"
    },
    "僵尸感染": {
        "api": "https://api.zombieden.cn/zedex_dl.php?map={prefix}{word}",
        "prefix": ["zm_"],
        "type": "round",
        "words": "1234567890qwertyuiopasdfghjklzxcvbnm"
    },
    "僵尸逃跑": {
        "api": "https://api.zombieden.cn/zedex_dl.php?map={prefix}{word}",
        "prefix": ["ze_"],
        "type": "round",
        "words": "1234567890qwertyuiopasdfghjklzxcvbnm"
    },
    "匪镇谍影": {
        "api": "https://api.zombieden.cn/zedex_dl.php?map=ttt_",
        "type": "once"
    },
    "娱乐对抗": {
        "api": "https://api.zombieden.cn/zedex_dl.php?map={prefix}{word}",
        "prefix": ["mg_"],
        "type": "round",
        "words": "1234567890qwertyuiopasdfghjklzxcvbnm"
    },
    "死跑": {
        "api": "https://api.zombieden.cn/zedex_dl.php?map=deathrun",
        "type": "once"
    },
    "滑翔": {
        "api": "https://api.zombieden.cn/zedex_dl.php?map=surf",
        "type": "once"
    },
    "连跳": {
        "api": "https://api.zombieden.cn/zedex_dl.php?map=bhop",
        "type": "once"
    }
}

def set_jsly():
    header = {'User-Agent': HEADER_ADD}
    maps = []
    for tp in jsly:
        r = None
        if jsly[tp]['type'] == "once":
            r = requests.get(jsly[tp]["api"], headers=header)
            maps.extend(parse_jsly(r.text))
        else:
            words = list(jsly[tp]["words"])
            prefixs = jsly[tp]["prefix"]
            for prefix in prefixs:
                for work in words:
                    r = requests.get(jsly[tp]["api"].format(
                        prefix=prefix, word=work), headers=header)
                    maps.extend(parse_jsly(r.text))
                    time.sleep(1)
    if ENABLE_WORKER:
        workers.put("僵尸乐园_maps", json.dumps({"maps": maps, "time": time.time()}))
    return maps


def parse_jsly(text):
    maps = []
    # print(text)
    text = text.replace("mg_blue_&_withe_course", "mg_blue_&amp;_withe_course")
    js = parse(text)['MapList']
    if js != None and 'csgo' in js.keys():
        try:
            if isinstance(js['csgo'], list):
                for j in js['csgo']:
                    maps.append({'name': j['mapname'],
                             'size': -1,  'verify': None,  'verifyer': ''})
            else:
                j = js['csgo']
                maps.append({'name': j['mapname'],
                         'size': -1,  'verify': None,  'verifyer': ''})
        except Exception as e:
            print(e)
            print(js)
    return maps

def set_93x():
    maps = []
    urls = [
        "https://xnetsoft2.93x.net/mapdata/ze.html",
        "https://xnetsoft2.93x.net/mapdata/kz.html",
        "https://xnetsoft2.93x.net/mapdata/surf.html",
        "https://xnetsoft2.93x.net/mapdata/bhop.html",
        "https://xnetsoft2.93x.net/mapdata/deathrun.html",
        "https://xnetsoft2.93x.net/mapdata/ttt.html",
        "https://xnetsoft2.93x.net/mapdata/hns.html",
        "https://xnetsoft2.93x.net/mapdata/mgdk.html"
    ]
    for url in urls:
        r = requests.get(url, headers={'User-Agent': HEADER_ADD})
        js = json.loads(r.text)
        maps.extend([{'name': j['mapname'],  'size':j['size'],
                    'verify':j['crc_32'],  'verifyer':'crc32'} for j in js])
    if ENABLE_WORKER:
        workers.put("93x_maps", json.dumps({"maps": maps, "time": time.time()}))
    return maps



def set_ub():
    header = {'User-Agent': HEADER_ADD}
    r = requests.get(
        "https://game.moeub.cn/api/maps?current=1&pageSize=10000&page=1", headers=header)
    maps = [{'name': j['name'],  'size':-1,  'verify':None,  'verifyer':""}
            for j in r.json()['data']['data']]
    if ENABLE_WORKER:
        workers.put("UB社区_maps", json.dumps({"maps": maps, "time": time.time()}))
    return maps

def set_default():
    maps=[{'name': 'ar_baggage.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'ar_dizzy.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'ar_lunacy.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'ar_monastery.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'ar_shoots.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'cs_agency.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'cs_assault.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'cs_climb.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'cs_italy.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'cs_militia.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'cs_office.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_ancient.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_bank.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_cache.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_canals.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_cbble.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_crete.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_dust2.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_hive.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_inferno.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_iris.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_lake.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_mirage.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_nuke.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_overpass.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_safehouse.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_shortdust.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_shortnuke.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_stmarc.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_sugarcane.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_train.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'de_vertigo.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'dz_blacksite.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'dz_ember.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'dz_sirocco.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'dz_vineyard.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'gd_cbble.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'lobby_mapveto.bsp', 'size': -1, 'verify': None, 'verifyer': ''}, {'name': 'training1.bsp', 'size': -1, 'verify': None, 'verifyer': ''}]
    if ENABLE_WORKER:
        workers.put("官方地图_maps", json.dumps({"maps": maps, "time": time.time()}))
    return maps

def main():
    conf = {}
    t=int(time.time())
    conf["官方地图"] = {"maps":set_default(),"update":t,"icons":"https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/730/69f7ebe2735c366c65c0b33dae00e12dc40edbe4.jpg"}
    conf["风云社"] =  {"maps":set_fys(),"update":t,"icons":"https://fyscs.com/favicon.ico"}
    conf["UB社区"] = {"maps":set_ub(),"update":t,"icons":"https://csgo.moeub.cn/moeub_logo.svg"}
    conf["93X"] =  {"maps":set_93x(),"update":t,"icons":"https://bbs.upkk.com/favicon.ico"}
    conf["僵尸乐园"] = {"maps":set_jsly(),"update":t,"icons":"https://bbs.zombieden.cn/favicon.ico"}
    f = open("maps.json", 'w', encoding='utf-8')
    f.write(json.dumps(conf, ensure_ascii=False))
    f.close()


if __name__ == "__main__":
    main()
