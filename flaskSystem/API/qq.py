#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - qq.py
#  @修改时间    : 2023-03-13 11:07:40
#  @上次修改    : 2023/3/13 下午11:07

from flaskSystem.src.Api.QQMusic import QQMusicApi
from flaskSystem.App import app

QQApi = QQMusicApi()


@app.get("/qq/search/<searchKey>/<page>/<size>")
def search(searchKey: str, page=1, size=30):
    size = int(size)
    if size > 30:  # 这里强制让qq音乐指定为30一页 因为qq服务器现在禁止超过30一页拉取数据
        size = 30
    lst = QQApi.getQQMusicSearch(searchKey, int(page), int(size))
    page = lst['page']
    lst = QQApi.formatList(lst['data'])
    return {
        'code': 200,
        'list': lst,
        'page': page
    }


def init():
    pass
