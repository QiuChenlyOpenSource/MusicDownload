#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - kw.py
#  @修改时间    : 2023-07-28 11:32:28
#  @上次修改    : 2023/7/28 下午11:32
from flask import request

from flaskSystem.src.Api.Kuwo import KwApi
from flaskSystem.src.Api.MiGu import MiGu
from flaskSystem.src.Api.MyFreeMP3 import MyFreeMP3
from flaskSystem.App import app

kw = KwApi()
mg = MiGu()
myFreeMP3 = MyFreeMP3()


@app.get("/kw/search/<searchKey>/<page>/<size>/<rid>/<encId>")
def kwsearch(searchKey: str, page=1, size=100,rid='', encId=''):
    lst = kw.search_kw_h5(searchKey, int(page), int(size),rid,encId)  # Mac端搜索接口
    page = lst['page']
    return {
        'code': 200,
        'list': lst['data'],
        'page': page
    }
    
@app.get("/kw/search/getToken")
def kw_get_token():
    return {
        'code': 200,
        'token': kw.getInitializationToken()
    }


@app.get("/mg/search/<searchKey>/<page>/<size>")
def mgsearch(searchKey: str, page=1, size=100):
    prefix = searchKey.split(":")
    lst = None
    if len(prefix) == 2:
        command = prefix[0]
        _id = prefix[1]
        # 高级指令
        if command == 'p':
            pass
            # 加载歌单
        elif command == 'b':
            # 加载专辑
            lst = mg.getAlbumList(_id)
        elif command == 'id':
            # 指定单曲id
            pass
        elif command == 't':
            # 加载排行版
            pass
        else:
            lst = None
    else:
        lst = mg.search(searchKey, int(page), int(size))  # Mac端搜索接口
    if lst is None:
        lst = {
            'data': []
        }
    else:
        page = lst['page']
    return {
        'code': 200,
        'list': lst['data'],
        'page': page
    }


@app.post("/myfreemp3/search")
def myFreeMP3search():
    data = request.get_json()
    lst = myFreeMP3.search(data)
    page = lst['page']
    return {
        'code': 200,
        'list': lst['data'],
        'page': page
    }


def init():
    pass
