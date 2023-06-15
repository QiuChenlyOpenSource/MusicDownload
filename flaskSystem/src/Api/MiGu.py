#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - MiGu.py
#  @修改时间    : 2023-03-13 11:07:40
#  @上次修改    : 2023/3/13 下午11:07
from flaskSystem.src.Common import Http
from flaskSystem.src.Common.Http import HttpRequest


class MiGu():
    httpClient: HttpRequest = None

    def __init__(self):
        self.httpClient = Http.HttpRequest()

    def getUrl(self, url: str, method=0, data=None):
        res = self.httpClient.getHttp2Json(url, method, data, {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50",
        })
        return res

    def search(self, searchKey="周杰伦", pageNum=1, pageSize=100):
        u = f'https://api.dog886.com/v1/getMiGuSearch?text={searchKey}&pageNo={pageNum}&pageSize={pageSize}'
        res = self.getUrl(u).json()
        data = res['data']
        lst = []
        for li in data['items']:
            kbpsList = li['kbpsList']
            _kbps = {}
            lastKbps = -1
            for kbps in kbpsList:
                kbs = int(kbps['kbps'].replace("kbps", ''))
                if kbs > lastKbps:
                    _kbps = kbps
                    lastKbps = kbs

            extra = _kbps['suffix']
            bitrate = _kbps['kbps']
            it = {
                'prefix': _kbps['type'],
                'extra': extra,
                'notice': "FLAC 无损音质" if extra == 'flac' else f'{extra.upper()} {bitrate}Kbps',
                'mid': li['id'],
                'musicid': li['id'],
                'songmid': li['id'],
                'size': "无",
                'title': li['name'],
                'singer': li['singer'],
                'album': "无专辑",
                'time_publish': "无",
                # 'hasLossless': li['hasLossless'],
                'readableText': f"{li['singer']} - {li['name']}"
            }
            lst.append(it)
        return {
            'data': lst,
            'page': {
                'size': data['total'],
                'next': pageNum + 1,
                'cur': pageNum,
                'searchKey': searchKey
            }
        }

    def getDownloadLink(self, _id="0", _type="4"):
        u = f'https://api.dog886.com/v1/getMiGuSong?id={_id}&type={_type}'
        res = self.getUrl(u).json()
        if res['code'] == '200':
            return "https:" + res['data']['url']
        else:
            return None
