#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - QQMusic.py
#  @修改时间    : 2023-07-30 09:53:12
#  @上次修改    : 2023/7/30 下午9:53

import json
import uuid

from flaskSystem.src.Api.BaseApi import BaseApi
from flaskSystem.src.Common import EncryptTools, Http
from flaskSystem.src.Types.Types import Songs
from flask import current_app
import base64


class QQMusicApi(BaseApi):
    QQHttpServer = Http.HttpRequest()

    mQQCookie = ""

    def getCookie(self):
        return self.mQQCookie

    def setQQCookie(self, ck: str):
        self.mQQCookie = ck

    def getHead(self):
        return {
            "authority": "u6.y.qq.com",
            "User-Agent": "QQ音乐/73222 CFNetwork/1406.0.2 Darwin/22.4.0".encode("utf-8"),
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh-Hans;q=0.9",
            "Referer": "http://y.qq.com",
            "Content-Type": "application/json; charset=UTF-8",
            "Cookie": self.getCookie(),
        }

    def getQQServersCallback(self, url: str, method: int = 0, data: dict = {}):
        """重新设计了Http接口

        参数:
            url (str): _description_
            method (int): _description_. Defaults to 0.
            data (dict): _description_. Defaults to {}.

        返回:
            requests.Response: 返回的http数据
        """

        return self.QQHttpServer.getHttp2Json(url, method, data, self.getHead())

    def getQQMusicLyricByWeb(self, songID: str) -> dict:
        """用QQ音乐网页端的接口获取歌词

        参数:
            songID (str): 歌曲数字序列id

        返回值:
            dict: 返回一个json结构, 通过['lyric']来获取base64后的歌词内容
        """
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        payload = {
            "comm": {
                "cv": 4747474,
                "ct": 24,
                "format": "json",
                "inCharset": "utf-8",
                "outCharset": "utf-8",
                "notice": 0,
                "platform": "yqq.json",
                "needNewCode": 1,
            },
            "PlayLyricInfo": {
                "module": "music.musichallSong.PlayLyricInfo",
                "method": "GetPlayLyricInfo",
                "param": {
                    # "songMID": "003AUKFs2S1Kwi",
                    "songID": songID
                },
            },
        }
        d = self.getQQServersCallback(url, 1, payload)
        d = d.json()
        d = d["PlayLyricInfo"]["data"]
        return d

    def getQQMusicLyricByMacApp(self, songID: str) -> dict:
        """从QQ音乐电脑客户端接口获取歌词

        参数:
            songID (str): 音乐id

        返回值:
            dict: 通过['lyric']来获取base64后的歌词内容
        """
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        payload = {
            "music.musichallSong.PlayLyricInfo.GetPlayLyricInfo": {
                "module": "music.musichallSong.PlayLyricInfo",
                "method": "GetPlayLyricInfo",
                "param": {
                    "trans_t": 0,
                    "roma_t": 0,
                    "crypt": 0,  # 1 define to encrypt
                    "lrc_t": 0,
                    "interval": 208,
                    "trans": 1,
                    "ct": 6,
                    "singerName": "",  # 576K576K
                    "type": 0,
                    "qrc_t": 0,
                    "cv": 80600,
                    "roma": 1,
                    "songID": songID,  # 391938242
                    "qrc": 0,  # 1 define base64 or compress Hex
                    "albumName": "",  # 55m96bi9
                    "songName": "",  # 55m96bi9
                },
            },
            "comm": {
                "wid": "",
                "tmeAppID": "qqmusic",
                "authst": "",
                "uid": "",
                "gray": "0",
                "OpenUDID": "",
                "ct": "6",
                "patch": "2",
                "psrf_qqopenid": "",
                "sid": "",
                "psrf_access_token_expiresAt": "",
                "cv": "80600",
                "gzip": "0",
                "qq": "",
                "nettype": "2",
                "psrf_qqunionid": "",
                "psrf_qqaccess_token": "",
                "tmeLoginType": "2",
            },
        }
        res = self.getQQServersCallback(url, 1, payload)
        d = res.json()
        d = d["music.musichallSong.PlayLyricInfo.GetPlayLyricInfo"]["data"]
        if d['lyric'] != '':
            # "retcode": 0,
            # "code": 0,
            # "subcode": 0,
            # {'retcode': -1901, 'code': -1901, 'subcode': -1901}
            # 外语歌曲有翻译 但是👴不需要！
            lyric = base64.b64decode(d['lyric'])
            d = lyric.decode('utf-8')
        else:
            d = ''
        return d

    def getQQMusicMediaLyric(self, mid: str) -> dict:
        """[已经被弃用]早期的歌词下载接口v1,但还可以使用。

        参数:
            mid (str): 音乐文件的mid

        返回:
            dict: 词典
        """
        # d = getQQServersCallback(
        #     f'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?songmid={mid}&g_tk=5381')
        d = self.getQQServersCallback(
            "https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric_new.fcg?g_tk=5381&format=json&inCharset=utf-8&outCharset=utf-8&notice=0&platform=h5&needNewCode=1&ct=121&cv=0&songmid="
            + mid
        )
        d = d.text  # MusicJsonCallback(...)
        d = d[18:-1]
        return json.loads(d)

    @staticmethod
    def getUUID():
        return uuid.uuid1().__str__()

    def parseQQMusicPlaylist(self, playID: str):
        """
        从客户端获取歌单列表
        参数:
            playID: 歌单id

        返回:

        """
        _uuid = self.getUUID()
        u = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        payload = {
            "getMusicPlaylist": {
                "module": "music.srfDissInfo.aiDissInfo",
                "method": "uniform_get_Dissinfo",
                "param": {
                    "disstid": int(playID),
                    "userinfo": 1,
                    "tag": 1,
                    "is_pc": 1,
                    "guid": _uuid,
                },
            },
            "comm": {
                "g_tk": 0,
                "uin": "",
                "format": "json",
                "ct": 6,
                "cv": 80600,
                "platform": "wk_v17",
                "uid": "",
                "guid": _uuid,
            },
        }
        r = self.getQQServersCallback(u, 1, payload)
        r = r.json()
        playlist = r["getMusicPlaylist"]
        if playlist["code"] == 0:
            lst = playlist["data"]["songlist"]
        else:
            lst = []
        # 数据清洗,去掉搜索结果中多余的数据
        list_clear = []
        for i in lst:
            list_clear.append(
                {
                    "album": i["album"],
                    "docid": "无",
                    "id": i["id"],
                    "mid": i["mid"],
                    "name": i["title"],
                    "singer": i["singer"],
                    "time_public": i["time_public"],
                    "title": i["title"],
                    "file": i["file"],
                }
            )
        # rebuild json
        # list_clear: 搜索出来的歌曲列表
        # {
        #   size 搜索结果总数
        #   next 下一搜索页码 -1表示搜索结果已经到底
        #   cur  当前搜索结果页码
        # }
        return {
            "data": list_clear,
            "page": {"size": len(list_clear), "next": "1", "cur": "1", "searchKey": ""},
        }

    def getQQMusicDownloadLinkV1(self, filename, songmid):
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        data = {
            "comm": {"ct": "19", "cv": "1777"},
            "queryvkey": {
                "method": "CgiGetVkey",
                "module": "vkey.GetVkeyServer",
                "param": {
                    "uin": "",
                    "guid": "QiuChenly",
                    "referer": "y.qq.com",
                    "songtype": [1],
                    "filename": [filename],
                    "songmid": [songmid],
                },
            },
        }
        d = self.getQQServersCallback(url, 1, data)
        d = d.json()
        vkey = d["queryvkey"]["data"]["midurlinfo"][0]
        return vkey

    def getQQMusicDownloadLinkByMacApp(self, filename, songmid) -> dict:
        """从Macos客户端中获取的查询文件purl的接口

        参数:
            filename (str): 拼接好的文件名
            songmid (str): 原始服务器返回的mid信息

        返回值:
            data: 一个数据结构 包含了purl等信息 通过['purl']拿到下载地址
        """
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        data = {
            "comm": {
                "wid": "",
                "tmeAppID": "qqmusic",
                "authst": "",
                "uid": "",
                "gray": "0",
                "OpenUDID": "",
                "ct": "6",
                "patch": "2",
                "psrf_qqopenid": "",
                "sid": "",
                "psrf_access_token_expiresAt": "",
                "cv": "80600",
                "gzip": "0",
                "qq": "",
                "nettype": "2",
                "psrf_qqunionid": "",
                "psrf_qqaccess_token": "",
                "tmeLoginType": "2",
            },
            "queryvkey": {
                "module": "music.vkey.GetEDownUrl",
                "method": "CgiGetEDownUrl",
                "param": {
                    "songmid": [songmid],
                    "uin": "",
                    # "musicfile": ["O6M0003dPNx22qGzZu.mgg"],
                    "checklimit": 1,
                    "scene": 0,
                    "filename": [filename],
                    "ctx": 1,
                    "referer": "y.qq.com",
                    "songtype": [1],
                    "downloadfrom": 0,
                    "nettype": "",
                    "guid": "2d484d3157d4ed482e406e6c5fdcf8c3d3275deb",
                },
            },
        }
        res = self.getQQServersCallback(url, 1, data)
        res = res.json()
        return res["queryvkey"]["data"]["midurlinfo"][0]

    def getQQMusicDownloadLinkByTrdServer(self, mid, sourceType) -> str:
        """
        从一个刚逆向出来的App共享资源服务器上获得的接口
        Args:
            sourceType: 设置音乐资源 sq hr hq mp3 四种类型
            mid: mid

        Returns:
            文件下载直链
        """
        return EncryptTools.testGetLink(mid, quality=sourceType)

    def getQQMusicSearchV2(self, key: str = "", page: int = 1, size: int = 30):
        json_ = self.getQQSearchData(key, page, size)
        # 开始解析QQ音乐的搜索结果
        res = json_["data"]
        lst = res["body"]["song"]["list"]
        meta = res["meta"]

        # 数据清洗,去掉搜索结果中多余的数据
        list_clear = []
        for i in lst:
            list_clear.append(
                {
                    "album": i["album"],
                    "docid": i["docid"],
                    "id": i["id"],
                    "mid": i["mid"],
                    "name": i["title"],
                    "singer": i["singer"],
                    "time_public": i["time_public"],
                    "title": i["title"],
                    "file": i["file"],
                }
            )

        # rebuild json
        # list_clear: 搜索出来的歌曲列表
        # {
        #   size 搜索结果总数
        #   next 下一搜索页码 -1表示搜索结果已经到底
        #   cur  当前搜索结果页码
        # }
        return {
            "data": list_clear,
            "page": {
                "size": meta["sum"],
                "next": meta["nextpage"],
                "cur": meta["curpage"],
                "searchKey": key,
            },
        }

    def getQQSearchData(self, key, page, size):
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"

        payload = {"music.search.SearchCgiService.DoSearchForQQMusicDesktop": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "search_type": 0,
                "query": key,
                "page_num": page,
                "num_per_page": size
            }
        }}
        headers = {
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8",
            "referer": "https://i.y.qq.com",
            "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1",
            "content-type": "application/json",
            "accept": "application/json",
            "Host": "u.y.qq.com",
            "Connection": "Keep-Alive"
        }

        res = self.QQHttpServer.getHttp2Json(
            url,
            1,
            payload,
            headers,
        )
        # print(res.text)
        json_ = res.json()
        return json_["music.search.SearchCgiService.DoSearchForQQMusicDesktop"]

    def getQQMusicSearch(
            self, key: str = "", page: int = 1, size: int = 30
    ) -> dict:
        """
        搜索音乐
        此接口已废弃。请参考@getQQMusicSearchV2

        参数:
            key (str): 搜索关键词. 默认是 "".
            page (int): 分页序号. 默认是 1.

        返回值:
            dict: 返回搜索列表
        """

        return self.getQQMusicSearchV2(key, page, size)

        # base url
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        # url = "https://u.y.qq.com/cgi-bin/musics.fcg" # 需要加密 懒得动了
        # base data content from qqmusic pc-client-apps

        # 一次获取最多获取30条数据 否则返回空列表
        page_per_num = size
        data = {
            "comm": {"ct": 19, "cv": 1845},
            "music.search.SearchCgiService": {
                "method": "DoSearchForQQMusicDesktop",
                "module": "music.search.SearchCgiService",
                "param": {"query": key, "num_per_page": page_per_num, "page_num": page},
            },
        }

        data = {
            "comm": {
                "wid": "",
                "tmeAppID": "qqmusic",
                "authst": "",
                "uid": "",
                "gray": "0",
                "OpenUDID": "2d484d3157d4ed482e406e6c5fdcf8c3d3275deb",
                "ct": "6",
                "patch": "2",
                "psrf_qqopenid": "",
                "sid": "",
                "psrf_access_token_expiresAt": "",
                "cv": "80600",
                "gzip": "0",
                "qq": "",
                "nettype": "2",
                "psrf_qqunionid": "",
                "psrf_qqaccess_token": "",
                "tmeLoginType": "2",
            },
            "music.search.SearchCgiService.DoSearchForQQMusicDesktop": {
                "module": "music.search.SearchCgiService",
                "method": "DoSearchForQQMusicDesktop",
                "param": {
                    "num_per_page": page_per_num,
                    "page_num": page,
                    "remoteplace": "txt.mac.search",
                    "search_type": 0,
                    "query": key,
                    "grp": 1,
                    "searchid": uuid.uuid1().__str__(),
                    "nqc_flag": 0,
                },
            },
        }
        res = self.QQHttpServer.getHttp2Json(
            url,
            1,
            data,
            {
                "referer": "https://y.qq.com/portal/profile.html",
                "Content-Type": "json/application;charset=utf-8",
                "user-agent": "QQ%E9%9F%B3%E4%B9%90/73222 CFNetwork/1406.0.3 Darwin/22.4.0",
            },
        )
        # print(res.text)
        jsons = res.json()
        # 开始解析QQ音乐的搜索结果
        res = jsons["music.search.SearchCgiService.DoSearchForQQMusicDesktop"]["data"]
        lst = res["body"]["song"]["list"]
        meta = res["meta"]

        # 数据清洗,去掉搜索结果中多余的数据
        list_clear = []
        for i in lst:
            list_clear.append(
                {
                    "album": i["album"],
                    "docid": i["docid"],
                    "id": i["id"],
                    "mid": i["mid"],
                    "name": i["title"],
                    "singer": i["singer"],
                    "time_public": i["time_public"],
                    "title": i["title"],
                    "file": i["file"],
                }
            )

        # rebuild json
        # list_clear: 搜索出来的歌曲列表
        # {
        #   size 搜索结果总数
        #   next 下一搜索页码 -1表示搜索结果已经到底
        #   cur  当前搜索结果页码
        # }
        return {
            "data": list_clear,
            "page": {
                "size": meta["sum"],
                "next": meta["nextpage"],
                "cur": meta["curpage"],
                "searchKey": key,
            },
        }

    @staticmethod
    def getQQMusicFileName(code, mid, format):
        """获取"""
        return f"{code}{mid}.{format}"

    def getQQMusicMatchSong(self, title: dict):
        name = title["name"]
        (lst, meta) = self.getQQMusicSearch(name)
        songs = self.formatList(lst)
        print(f"搜索到{len(songs)}条。")
        if len(songs) == 0:
            return None
        for song in songs:
            if song["singer"].upper() == title["author_simple"].upper():
                return song
            else:
                print(
                    f"不匹配: {song['singer']} {song['title']} != {title['author_simple']} {title['name']}"
                )
        return None

    def search(self, searchKey: str) -> list[Songs]:
        pass

    def formatList(self, mlist):
        """
        处理音乐列表
        Args:
            mlist (Array<T>): 歌曲列表

        Returns:
            lists, songs: 处理过的数据数组
        """
        songs = []  # : list[Songs]
        for i in mlist:
            singer = i["singer"][0]["name"]

            id = i["file"]
            # 批量下载不需要选择音质 直接开始解析为最高音质 枚举
            code = ""
            format = ""
            qStr = ""
            fsize = 0
            mid = id["media_mid"]
            if int(id["size_hires"]) != 0:
                # 高解析无损音质
                code = "RS01"
                format = "flac"
                qStr = "高解析无损 Hi-Res"
                fsize = int(id["size_hires"])
            elif int(id["size_flac"]) != 0:
                isEnc = False  # 这句代码是逆向出来的 暂时无效
                if isEnc:
                    code = "F0M0"
                    format = "mflac"
                else:
                    code = "F000"
                    format = "flac"
                qStr = "无损品质 FLAC"
                fsize = int(id["size_flac"])
            elif int(id["size_320mp3"]) != 0:
                code = "M800"
                format = "mp3"
                qStr = "超高品质 320kbps"
                fsize = int(id["size_320mp3"])
            elif int(id["size_192ogg"]) != 0:
                isEnc = False  # 这句代码是逆向出来的 暂时无效
                if isEnc:
                    code = "O6M0"
                    format = "mgg"
                else:
                    code = "O600"
                    format = "ogg"
                qStr = "高品质 OGG"
                fsize = int(id["size_192ogg"])
            elif int(id["size_128mp3"]) != 0:
                isEnc = False  # 这句代码是逆向出来的 暂时无效
                if isEnc:
                    code = "O4M0"
                    format = "mgg"
                else:
                    code = "M500"
                    format = "mp3"
                qStr = "标准品质 128kbps"
                fsize = int(id["size_128mp3"])
            elif int(id["size_96aac"]) != 0:
                code = "C400"
                format = "m4a"
                qStr = "低品质 96kbps"
                fsize = int(id["size_96aac"])
            else:
                print("这首歌曲好像无法下载,请检查是否有vip权限.")
                continue

            albumName = str(i["album"]["title"]).strip(" ")
            if albumName == "":
                albumName = "未分类专辑"

            # 开始检查歌曲过滤显示
            # 第三方修改歌曲可以在这里对歌曲做二次处理
            flacName = i["title"]

            time_publish = i["time_public"]
            if time_publish == "":
                time_publish = "1970-01-01"

            # 通过检查 将歌曲放入歌曲池展示给用户 未通过检查的歌曲将被放弃并且不再显示
            songs.append(
                {
                    "prefix": code,
                    "extra": format,
                    "notice": qStr,
                    "mid": mid,
                    "musicid": i["id"],
                    "songmid": i["mid"],
                    "size": f"%.2fMB" % (fsize / 1024 / 1024),
                    "title": flacName,
                    "singer": f"{singer}",
                    "album": albumName,
                    "albumMid": i["album"]["mid"],
                    "time_publish": time_publish,
                    "readableText": f'{time_publish} {singer} - {i["title"]} | {qStr}',
                }
            )
        # 这部分其实可以只返回songs 但是代码我懒得改了 反正又不是不能用=v=
        return songs

    def parseQQMusicAlbum(self, _id: str):
        """
        从客户端接口获取专辑列表
        参数:
            _id: 专辑ID

        返回专辑列表:

        """
        _uuid = self.getUUID()
        u = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        payload = {
            "AlbumSongList": {
                "module": "music.musichallAlbum.AlbumSongList",
                "method": "GetAlbumSongList",
                "param": {"albumMid": _id, "begin": 0, "num": 60, "order": 2},
            },
            "comm": {
                "g_tk": 0,
                "uin": "",
                "format": "json",
                "ct": 6,
                "cv": 80600,
                "platform": "wk_v17",
                "uid": "",
                "guid": _uuid,
            },
        }
        r = self.getQQServersCallback(u, 1, payload)
        r = r.json()
        playlist = r["AlbumSongList"]
        if playlist["code"] == 0:
            lst = playlist["data"]["songList"]
        else:
            lst = []
        # 数据清洗,去掉搜索结果中多余的数据
        list_clear = []
        for i in lst:
            i = i["songInfo"]
            list_clear.append(
                {
                    "album": i["album"],
                    "docid": "无",
                    "id": i["id"],
                    "mid": i["mid"],
                    "name": i["title"],
                    "singer": i["singer"],
                    "time_public": i["time_public"],
                    "title": i["title"],
                    "file": i["file"],
                }
            )
        # rebuild json
        # list_clear: 搜索出来的歌曲列表
        # {
        #   size 搜索结果总数
        #   next 下一搜索页码 -1表示搜索结果已经到底
        #   cur  当前搜索结果页码
        # }
        return {
            "data": list_clear,
            "page": {"size": len(list_clear), "next": "1", "cur": "1", "searchKey": ""},
        }

    def parseQQMusicToplist(self, _id: str):
        """
        从客户端接口获取专辑列表
        参数:
            _id: TopListID

        返回专辑列表:

        """
        _uuid = self.getUUID()
        u = "https://u.y.qq.com/cgi-bin/musicu.fcg"
        payload = {
            "comm": {
                "cv": 4747474,
                "ct": 24,
                "format": "json",
                "inCharset": "utf-8",
                "outCharset": "utf-8",
                "notice": 0,
                "platform": "yqq.json",
                "needNewCode": 1,
                "uin": 0,
                "g_tk_new_20200303": 5381,
                "g_tk": 5381,
            },
            "req_1": {
                "module": "musicToplist.ToplistInfoServer",
                "method": "GetDetail",
                "param": {"topid": int(_id), "offset": 0, "num": 100},  # , "period": "2023-07-01"},
            },
        }

        r = self.getQQServersCallback(u, 1, payload)
        r = r.json()
        playlist = r["req_1"]
        print(playlist)
        if playlist["code"] == 0:
            lst = playlist["data"]["songInfoList"]
        else:
            lst = []
        # 数据清洗,去掉搜索结果中多余的数据
        list_clear = []
        for i in lst:
            list_clear.append(
                {
                    "album": i["album"],
                    "docid": "无",
                    "id": i["id"],
                    "mid": i["mid"],
                    "name": i["title"],
                    "singer": i["singer"],
                    "time_public": i["time_public"],
                    "title": i["title"],
                    "file": i["file"],
                }
            )
        # rebuild json
        # list_clear: 搜索出来的歌曲列表
        # {
        #   size 搜索结果总数
        #   next 下一搜索页码 -1表示搜索结果已经到底
        #   cur  当前搜索结果页码
        # }
        return {
            "data": list_clear,
            "page": {"size": len(list_clear), "next": "1", "cur": "1", "searchKey": ""},
        }

    def getAlbumInfomation(self, albumMid="002eFUFm2XYZ7z", albumID=0):
        url = "https://u.y.qq.com/cgi-bin/musicu.fcg"

        payload = {
            "comm": {
                "cv": 4747474,
                "ct": 24,
                "format": "json",
                "inCharset": "utf-8",
                "outCharset": "utf-8",
                "notice": 0,
                "platform": "yqq.json"
            },
            "AlbumInfoServer": {
                "module": "music.musichallAlbum.AlbumInfoServer",
                "method": "GetAlbumDetail",
                "param": {
                    "albumMid": albumMid,
                    "albumID": albumID
                }
            }
        }
        headers = {
            "authority": "u.y.qq.com",
            "accept": "application/json",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "content-type": "application/json",
            "origin": "https://y.qq.com",
            "referer": "https://y.qq.com/",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.1901.183"
        }
        r = self.getQQServersCallback(url, 1, payload)
        r = r.json()
        return r

    def getSingleMusicInfoAll(self, _id: str, albumMid=''):
        """
        获取单曲歌曲信息

        参数:
            _id: https://y.qq.com/n/ryqq/songDetail/0042QMDR1VzSsx 里面的 0042QMDR1VzSsx\n
            https://y.qq.com/n/ryqq/songDetail/374229667?songtype=0 里面的 374229667

        返回:

        """

        # 这里有两种格式 一种是纯数字 一种是mid 所以判断是否可被int即可

        try:
            sid = int(_id)
            mid = 0
        except Exception as e:
            sid = 0
            mid = _id

        # 切换接口
        useV2 = False
        if useV2:
            url = "https://u6.y.qq.com/cgi-bin/musicu.fcg"
            payload = {
                "comm": {
                    "format": "json",
                    "inCharset": "utf-8",
                    "outCharset": "utf-8",
                    "notice": 0,
                    "platform": "h5",
                    "needNewCode": 1
                },
                "get_song_detail": {
                    "module": "music.pf_song_detail_svr",
                    "method": "get_song_detail",
                    "param": {
                        "song_id": sid, "song_mid": mid, "song_type": 0
                    }
                },
                "AlbumInfoServer": {
                    "module": "music.musichallAlbum.AlbumInfoServer",
                    "method": "GetAlbumDetail",
                    "param": {
                        "albumMid": albumMid,
                        "albumID": 0
                    }
                }
            }
            headers = {
                "authority": "u6.y.qq.com",
                "accept": "application/json",
                "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
                "content-type": "application/json",
                "origin": "https://i.y.qq.com",
                "referer": "https://i.y.qq.com/",
                "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/115.0.0.0"
            }
            r = self.QQHttpServer.getHttp2Json(url, 1, payload, headers)
        else:
            u = "https://u.y.qq.com/cgi-bin/musicu.fcg"
            d = {
                "comm": {
                    "g_tk": 0,
                    "uin": "",
                    "format": "json",
                    "ct": 6,
                    "cv": 80600,
                    "platform": "h5",
                    "uid": "",
                    "guid": self.getUUID(),
                },
                "get_song_detail": {
                    "module": "music.pf_song_detail_svr",
                    "method": "get_song_detail",
                    "param": {
                        "song_id": sid, "song_mid": mid, "song_type": 0
                    },
                },
                "AlbumInfoServer": {
                    "module": "music.musichallAlbum.AlbumInfoServer",
                    "method": "GetAlbumDetail",
                    "param": {
                        "albumMid": albumMid,
                        "albumID": 0
                    }
                }
            }
            r = self.getQQServersCallback(u, 1, d)
        r = r.json()
        get_song_detail = r
        return get_song_detail

    def getSingleMusicInfo(self, _id: str):
        """
        获取单曲音乐详细信息

        Args:
            _id (str): _description_

        Returns:
            _type_: _description_
        """
        get_song_detail = self.getSingleMusicInfoAll(_id, '')["get_song_detail"]
        # print(r)
        if get_song_detail["code"] == 0:
            i = get_song_detail["data"]["track_info"]
            lst = [
                {
                    "album": i["album"],
                    "docid": "无",
                    "id": i["id"],
                    "mid": i["mid"],
                    "name": i["title"],
                    "singer": i["singer"],
                    "time_public": i["time_public"],
                    "title": i["title"],
                    "file": i["file"],
                }
            ]
        else:
            lst = []
        # 数据清洗,去掉搜索结果中多余的数据
        # rebuild json
        # list_clear: 搜索出来的歌曲列表
        # {
        #   size 搜索结果总数
        #   next 下一搜索页码 -1表示搜索结果已经到底
        #   cur  当前搜索结果页码
        # }
        return {
            "data": lst,
            "page": {"size": len(lst), "next": "1", "cur": "1", "searchKey": ""},
        }
