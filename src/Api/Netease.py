#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - Netease.py
#  @修改时间    : 2023-03-02 07:38:37
#  @上次修改    : 2023/3/2 下午7:38
import base64
import json
import os
import cv2
from src.Api.BaseApi import BaseApi
from src.Common import Http
from src.Types.Types import Songs


class Netease(BaseApi):
    __baseUrl = 'http://cloud-music.pl-fe.cn'

    def __init__(self):
        self.__userInfo = None
        self.__httpServer = Http.HttpRequest()

    def http(self, url, method=0, data={}):
        return self.__httpServer.getHttp2Json(self.__baseUrl + url, method, data)

    def search(self, searchKey: str) -> list[Songs]:
        pass

    def cookie(self):
        dt = self.__httpServer.getSession().cookies.get_dict()
        return dt

    def set_cookie(self, ck: dict):
        self.__httpServer.setCookie(ck)

    def checkQrState(self, key: str):
        u = '/login/qr/check?key=' + key
        return self.http(u)

    def getUserDetail(self):
        u = '/user/account'
        if self.__userInfo is not None and self.__userInfo['code'] == 200:
            return self.__userInfo
        self.__userInfo = self.http(u).json()
        return self.__userInfo

    __likeList = []

    def getUserLikeList(self):
        u = f'/likelist?uid={self.__userInfo["account"]["id"]}'
        res = self.http(u).json()
        self.__likeList = res['ids']
        return self.__likeList

    userPlaylist = []

    def getUserPlaylist(self):
        global userPlaylist
        u = f'/user/playlist?uid={self.__userInfo["account"]["id"]}'
        res = self.http(u).json()
        userPlaylist = [
            {
                'userId': l['userId'],
                'trackCount': l['trackCount'],
                'name': l['name'],
                'id': l['id'],
                'coverImgUrl': l['coverImgUrl']
            } for l in res['playlist']
        ]
        # print("用户所有歌单")
        return userPlaylist

    def getPlayListAllMusic(self, playId, size=1000, offset=0):
        u = f'/playlist/track/all?id={playId}&limit={size}&offset={offset}'
        res = self.http(u)
        if res.status_code != 200:
            return None
        if res.text.find(":400}") != -1:
            return None
        js = res.json()
        return [
            {
                "name": li['name'],
                "id": li['id'],
                'author_simple': li['ar'][0]['name'],  # li['ar'][0]['name'] if len(li['ar']) == 1 else
                "author": li['ar'],  # 数组[{'id': 472822, 'name': 'JJD', 'tns': [], 'alias': []}]
                'publishTime': li['publishTime'],
                'album': li['al']
            } for li in js['songs']
        ]

    def qrLogin(self):
        u = '/login/qr/key'
        res = self.http(u)
        unikey = res.json()['data']['unikey']

        u = '/login/qr/create?key=' + unikey + "&qrimg=1"
        res = self.http(u).json()['data']
        b64 = res['qrimg']
        url = res['qrurl']

        img = base64.b64decode(b64.split(",")[1])
        with open("./login.png", "wb+") as p:
            p.write(img)
            p.flush()

        img = cv2.imread("./login.png")
        cv2.imshow("", img)
        cv2.waitKey(0)

        res = self.checkQrState(unikey)
        res = res.json()['code']
        if res == 803:
            # Login Success
            return True
        print("登录失败。")
        return False

    def save_local(self, reinit=False):
        """
        保存cookie到本地 避免重复登录造成账户异常
        Args:
            reinit: True则清空本地cookie重置。

        Returns:

        """
        with open("./NetEase.cfg", 'wb+') as p:
            p.write(json.dumps({
                'cookie': '' if reinit else self.cookie()
                # 'likes': mySubCount
            }).encode())
            p.flush()

    def read_local(self):
        """
        登录成功返回True 否则返回False
        Returns:

        """
        if os.path.exists("./NetEase.cfg"):
            with open("./NetEase.cfg", 'r') as p:
                s = p.read()
                dt = json.loads(s)
                if dt['cookie'] == '':
                    return False
                self.set_cookie(dt['cookie'])
                isLogin = self.getUserDetail()['code'] == 200
                return isLogin
        return False
