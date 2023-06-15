#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - es.py
#  @修改时间    : 2023-03-15 04:38:40
#  @上次修改    : 2023/3/15 上午4:38
from flask import request
from flaskSystem.src.Api.Netease import Netease
from flaskSystem.App import app

netes = Netease()


@app.get("/es/qrLogin")
def loginCode():
    qrcode = netes.qrLogin()
    return {
        'code': 200,
        'qrcode': qrcode
    }


@app.get("/es/checkLoginState/<unikey>")
def checkLoginState(unikey: str):
    state = netes.checkQrState(unikey)
    return state


@app.get("/es/initAnonimous")
def initAnonimous():
    state = netes.anonimousLogin()
    return state


@app.post("/es/setCookie")
def setCookie():
    ck = request.get_json()['cookie']
    netes.set_cookie(ck)
    return {
        'code': 200
    }


@app.get("/es/getUserInfo")
def getUserInfo():
    state = netes.getUserDetail()
    return state


@app.get("/es/getCloud")
def getCloud():
    state = netes.getAllMusicCloud(1000)
    return state


@app.get("/es/esLogout")
def logout():
    state = netes.logoutUser()
    return state


@app.post("/es/bindSid2Asid")
def bindSid2Asid():
    data = request.get_json()
    state = netes.matchMusicSid2ASid(data)
    return state


@app.get("/es/getUserPlaylist/<userid>")
def getUserPlaylist(userid: str):
    state = netes.getUserPlaylist(userid)
    return {
        'code': 200,
        'list': state
    }


@app.get("/wyy/search/<searchKey>/<page>/<size>")
def essearch(searchKey: str, page=1, size=100):
    page = int(page)
    size = int(size)
    offset = (page - 1) * size
    if offset < 0 or size <= 0:
        return {
            'code': 400
        }
    lst = netes.searchMusic(
        searchKey, int(page), int(size))  # Mac端搜索接口
    page = lst['page']
    return {
        'code': 200,
        'list': lst['data'],
        'page': page
    }


@app.get("/es/getMusicListByPlaylistID/<playListID>/<page>/<size>")
def getMusicListByPlaylistID(playListID: str, page: str, size: str):
    page = int(page)
    size = int(size)
    offset = (page - 1) * size
    if offset < 0 or size <= 0:
        return {
            'code': 400
        }
    state = netes.getPlayListAllMusic(playListID, size, offset)
    if type(state) == int:
        if state == -1:
            return {
                'code': 20001
            }
    return {
        'code': 200,
        'list': state
    }


def init():
    pass
