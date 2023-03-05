#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - qq.py
#  @修改时间    : 2023-03-05 01:43:55
#  @上次修改    : 2023/3/5 下午1:43
from flask import request

from src.Api.QQMusic import QQMusicApi
from web.App import app

QQApi = QQMusicApi()


@app.get("/qq/search/<searchKey>/<page>")
def search(searchKey: str, page=1):
    lst = QQApi.getQQMusicSearch(searchKey, int(page))
    page = lst['page']
    lst = QQApi.formatList(lst['data'])
    return {
        'code': 200,
        'list': lst,
        'page': page
    }


def init():
    pass
