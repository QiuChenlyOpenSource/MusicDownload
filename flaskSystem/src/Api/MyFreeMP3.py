#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - MyFreeMP3.py
#  @修改时间    : 2023-07-24 06:21:40
#  @上次修改    : 2023/7/24 上午4:33
import time
from typing import Dict

from flaskSystem.src.Common import Http
from flaskSystem.src.Common.Http import HttpRequest


class MyFreeMP3():
    httpClient: HttpRequest = None

    def __init__(self):
        self.httpClient = Http.HttpRequest()

    def getUrl(self, url: str, method=0, data=None):
        res = self.httpClient.getHttp2Json(url, method, data, {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://tools.liumingye.cn",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
        })
        return res

    def search(self, data):
        u = f'https://api.liumingye.cn/m/api/search'
        res = self.getUrl(u, 1, data)
        res = res.json()
        if res['code'] != 200:
            res['data'] = {
                'list': [],
                'total': -1
            }
        _data = res['data']
        lst = []
        for li in _data['list']:
            kbpsList = li['quality']
            lastKbps = -1
            for kbps in kbpsList:
                if type(kbps) is dict:
                    kbs = int(kbps['name'])
                else:
                    kbs = int(kbps)
                if kbs > lastKbps:
                    lastKbps = kbs

            extra = "flac" if lastKbps >= 1000 else "mp3"

            album = li.get("album")
            mid = li.get('hash')
            if mid is None:
                mid = li.get("id")

            if mid is None:
                print("")
            it = {
                'prefix': lastKbps,
                'extra': extra,
                'notice': "FLAC 无损音质" if extra == 'flac' else f'{extra.upper()} {lastKbps}Kbps',
                'mid': mid,
                'musicid': li['name'],
                'songmid': li['name'],
                'size': "无",
                'title': li['name'],
                'singer': "/".join([
                    it['name'] for it in li['artist']
                ]),
                'album': "" if album is None else album['name'],
                'time_publish': "无",
            }
            lst.append(it)
        return {
            'data': lst,
            'page': {
                'size': _data['total'],
                'next': -1 if _data['total'] == 0 else data['page'] + 1,
                'cur': data['page'],
                'searchKey': data['text']
            }
        }
