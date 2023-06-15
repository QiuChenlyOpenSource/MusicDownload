#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - kw.py
#  @修改时间    : 2023-03-13 11:07:40
#  @上次修改    : 2023/3/13 下午11:07
from flask import request

from flaskSystem.src.Api.Kuwo import KwApi
from flaskSystem.src.Api.MiGu import MiGu
from flaskSystem.src.Api.MyFreeMP3 import MyFreeMP3
from flaskSystem.App import app

kw = KwApi()
mg = MiGu()
myFreeMP3 = MyFreeMP3()


@app.get("/kw/search/<searchKey>/<page>/<size>")
def kwsearch(searchKey: str, page=1, size=100):
    lst = kw.search_kw_mac(searchKey, int(page), int(size))  # Mac端搜索接口
    page = lst['page']
    return {
        'code': 200,
        'list': lst['data'],
        'page': page
    }


@app.get("/mg/search/<searchKey>/<page>/<size>")
def mgsearch(searchKey: str, page=1, size=100):
    lst = mg.search(searchKey, int(page), int(size))  # Mac端搜索接口
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
