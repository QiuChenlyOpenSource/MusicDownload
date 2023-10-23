#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - Http.py
#  @修改时间    : 2023-07-24 02:07:51
#  @上次修改    : 2023/7/24 上午2:07

import json
from http.cookiejar import Cookie

import requests
from requests import Request, Session


class HttpRequest:
    __session = None

    def __init__(self):
        # 全局唯一Session
        self.__session = requests.Session()

    def getHttp(self,
                url: str,
                method: int = 0,
                data: bytes = r'',
                header: dict[str, str, str] = {},
                params: dict[str, str] = {}
                ) -> requests.Response:
        """
        Http请求-提交二进制流
        Args:
            params: url后面的网址参数
            url: url网址
            method: 0 表示Get请求 1 表示用POST请求. 默认值为 0.
            data: 提交的二进制流data数据. 默认值为 r''.
            header: 协议头. 默认值为 {}.

        Returns:
            requests.Response: 返回的http数据
        """
        if method == 0:
            d = self.__session.get(url, headers=header, params=params)
        else:
            d = self.__session.post(url, data, headers=header, params=params)
        return d

    def getHttp2Json(self, url: str, method: int = 0, data: dict = {}, header: dict = {}):
        """Http请求-提交json数据

        Args:
            url (str): url网址
            method (int): 0 表示Get请求 1 表示用POST请求. 默认值为 0.
            data (bytes): 提交的json对象数据. 默认值为 {}.
            header (dict): 协议头. 默认值为 {}.

        Returns:
            requests.Response: 返回的http数据
        """
        d = json.dumps(data, ensure_ascii=False)
        d = d.encode('utf-8')
        return self.getHttp(url, method, d, header)

    def getSession(self) -> Session:
        return self.__session

    def setCookie(self, ck):
        for a in ck:
            self.__session.cookies.set(a, ck[a])
        print("cookie set.")
