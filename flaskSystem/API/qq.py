#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - qq.py
#  @修改时间    : 2023-03-14 02:55:44
#  @上次修改    : 2023/3/14 下午2:55

from flaskSystem.src.Api.QQMusic import QQMusicApi
from flaskSystem.App import app

QQApi = QQMusicApi()


@app.get("/qq/search/<searchKey>/<page>/<size>")
def search(searchKey: str, page=1, size=30):
    # 检查前缀
    prefix = searchKey.split(":")
    if len(prefix) == 2:
        command = prefix[0]
        _id = prefix[1]
        # 高级指令
        if command == 'p':
            # 加载歌单
            lst = QQApi.parseQQMusicPlaylist(_id)
        elif command == 'b':
            # 加载专辑
            lst = QQApi.parseQQMusicAlbum(_id)
        elif command == 'id':
            # 指定单曲id
            lst = QQApi.getSingleMusicInfo(_id)
        elif command == 't':
            # 加载排行版
            lst = QQApi.parseQQMusicToplist(_id)
        else:
            lst = []
    else:
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
