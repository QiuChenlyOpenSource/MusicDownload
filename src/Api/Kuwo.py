#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - Kuwo.py
#  @修改时间    : 2023-03-05 10:22:34
#  @上次修改    : 2023/3/5 下午10:22
import json
import uuid

from src.Api.BaseApi import BaseApi
from src.Common import Http
from src.Common.Http import HttpRequest
from src.Common.Tools import subString
from src.Types.Types import Songs


class KwApi(BaseApi):
    __csrf = ''

    httpClient: HttpRequest = None

    def __init__(self):
        self.httpClient = Http.HttpRequest()
        self.generateCSRFToken()

    def search(self, searchKey: str) -> list[Songs]:
        pass

    def getUrl(self, url: str, method=0, data=None):
        res = self.httpClient.getHttp2Json(url, method, data, {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            'csrf': self.__csrf,
            "Referer": "https://www.kuwo.cn/search/list?key="  # 如果不设置来源就会403禁止访问
        })
        ck = res.headers.get("Set-Cookie")
        if ck is not None:
            kw_token = subString(
                ck, "kw_token=", ";"
            )
            self.__csrf = kw_token
            print(kw_token)
        return res

    def getReqId(self):
        return uuid.uuid4().__str__()

    def generateCSRFToken(self):
        """
        由于网页端的限制 需要先生成csrf的值
        Returns:

        """
        res = self.getUrl("https://www.kuwo.cn/search/list?key=%E5%91%A8")

    def search_kw(self, searchKey: str, page_num: int = 1, page_size=100):
        url = f"https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={searchKey}" \
              f"&pn={page_num}&rn={page_size}&httpsStatus=1&reqId={self.getReqId()}"
        res = self.getUrl(url)
        res = res.json()
        data = res['data']
        lst = [
            {
                'prefix': "无信息",
                'extra': "flac",
                'notice': "无信息",
                'mid': li['rid'],
                'musicid': li['musicrid'],
                'songmid': li['rid'],
                'size': "无信息",
                'title': li['name'],
                'singer': li['artist'],
                'album': li['album'],
                'time_publish': li['releaseDate'],
                'readableText': f"{li['releaseDate']} {li['artist']} - {li['name']}"
            } for li in data['list']
        ]
        return {
            'data': lst,
            'page': {
                'size': data['total'],
                'next': page_num + 1,
                'cur': page_num,
                'searchKey': searchKey
            }
        }

    def getDownloadUrl(self, mid: int):
        """
        网页端接口
        Args:
            mid:

        Returns:

        """
        # "N_MINFO": "level:ff,bitrate:2000,format:flac,size:29.97Mb;level:pp,bitrate:1000,format:ape,
        # size:29.74Mb;level:p,bitrate:320,format:mp3,size:10.29Mb;level:h,bitrate:128,format:mp3,
        # size:4.11Mb;level:s,bitrate:24,format:aac,size:816.79Kb;level:zp,bitrate:20000,format:zp,size:zpMb",
        url = f"https://www.kuwo.cn/api/v1/www/music/playUrl?mid={mid}" \
              "&type=flac&httpsStatus=1&reqId=" + self.getReqId()
        res = self.getUrl(url)
        res = res.json()
        return res['data']['url']

    def getDownloadUrlV2(self, mid: str, br='1000kape'):
        """
        下载地址解析
        Args:
            mid: 音乐id
            br: 波特率类型 1000kape 320kmp3 192kmp3 128kmp3

        Returns:
        # {
        # 	"code": 200,
        # 	"msg": "success",
        # 	"url": "https://sy-sycdn.kuwo.cn/7e43dfa6b7295af0e4257a59e5007f6b/6404949a/resource/s1/4/85/520276467.ape"
        # }
        # or 'failed' 表示搜索不到这个波特率的歌曲
        """
        # 1000kape 320kmp3 192kmp3 128kmp3
        url = f'https://antiserver.kuwo.cn/anti.s?type=convert_url3&rid={mid}&br=1000kape'
        res = self.getUrl(url)
        return res
