#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - Kuwo.py
#  @修改时间    : 2023-03-02 09:54:20
#  @上次修改    : 2023/3/2 上午9:54
import uuid

from src.Api.BaseApi import BaseApi
from src.Common.Http import getHttp2Json
from src.Common.Tools import subString
from src.Types.Types import Songs


class KwApi(BaseApi):
    __csrf = ''

    def getUrl(self, url: str, method=0, data=None):
        res = getHttp2Json(url, method, data, {
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

    def __init__(self):
        self.generateCSRFToken()

    def getReqId(self):
        return uuid.uuid4().__str__()

    def generateCSRFToken(self):
        """
        由于网页端的限制 需要先生成csrf的值
        Returns:

        """
        res = self.getUrl("https://www.kuwo.cn/search/list?key=%E5%91%A8")

    def search(self, searchKey: str, page_num: int = 1) -> list[Songs]:
        url = f"https://www.kuwo.cn/api/www/search/searchMusicBykeyWord?key={searchKey}" \
              f"&pn={page_num}&rn=100&httpsStatus=1&reqId={self.getReqId()}"
        res = self.getUrl(url)
        res = res.json()
        lst = [
            Songs(
                **li
            ) for li in res['data']['list']
        ]
        return lst

    def getDownloadUrl(self, mid: int):
        # "N_MINFO": "level:ff,bitrate:2000,format:flac,size:29.97Mb;level:pp,bitrate:1000,format:ape,
        # size:29.74Mb;level:p,bitrate:320,format:mp3,size:10.29Mb;level:h,bitrate:128,format:mp3,
        # size:4.11Mb;level:s,bitrate:24,format:aac,size:816.79Kb;level:zp,bitrate:20000,format:zp,size:zpMb",
        url = f"https://www.kuwo.cn/api/v1/www/music/playUrl?mid={mid}" \
              "&type=flac&httpsStatus=1&reqId=" + self.getReqId()
        res = self.getUrl(url)
        res = res.json()
        return res['data']['url']
