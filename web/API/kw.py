#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - kw.py
#  @修改时间    : 2023-03-07 08:35:39
#  @上次修改    : 2023/3/7 下午8:35
from src.Api.Kuwo import KwApi
from web.App import app

kw = KwApi()


@app.get("/kw/search/<searchKey>/<page>/<size>")
def kwsearch(searchKey: str, page=1, size=100):
    lst = kw.search_kw_mac(searchKey, int(page), int(size))  # Mac端搜索接口
    page = lst['page']
    return {
        'code': 200,
        'list': lst['data'],
        'page': page
    }


def init():
    pass
