#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - Tools.py
#  @修改时间    : 2023-03-04 08:59:23
#  @上次修改    : 2023/3/4 下午8:59
import base64
import os
import threading

import requests

from web.API.qq import QQApi


def subString(text: str, left: str, right: str):
    """
    取文本中间
    Args:
        text: 完整文本
        left: 左边文本
        right: 右边文本

    Returns:
        返回中间的文本

    """
    leftInx = text.find(left)
    leftInx += len(left)
    rightInx = text.find(right, leftInx)
    txt = text[leftInx:rightInx]
    return txt


threadLock = threading.Lock()  # 多线程锁 防止同时创建同一个文件夹冲突


def downSingle(music, download_home, onlyShowSingerSelfSongs=False, musicAlbumsClassification=True):
    songmid = music['songmid']
    file = QQApi.getQQMusicFileName(music['prefix'], music['mid'], music['extra'])
    musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}] {round(int(music['size']) / 1024 / 1024, 2)}MB - {file}"
    musicid = music['musicid']
    # link = getQQMusicDownloadLinkByMacApp(file, songmid)
    # link = getQQMusicDownloadLinkV1(file, songmid)  # 早期方法 可食用
    # vkey = link['purl']
    # link = f'http://ws.stream.qqmusic.qq.com/{vkey}&fromtag=140'
    # if vkey == '':
    #     print(f"找不到资源文件! 解析歌曲下载地址失败！{musicFileInfo}")
    #     return False

    # 自动匹配歌曲类型
    sourceSelect = "hr" if music['prefix'] == "RS01" else "sq" if music['prefix'] == "F000" else \
        "hq" if music['prefix'] == "M800" else "mp3"

    link = QQApi.getQQMusicDownloadLinkByTrdServer(songmid, sourceSelect)

    # 测试歌词下载保存接口代码
    # lyric = getQQMusicMediaLyric(songmid) # 早期方法 已弃用
    # lyric = getQQMusicLyricByMacApp(musicid)
    # lyric = getQQMusicLyricByWeb(musicid)
    # lyrics = base64.b64decode(lyric['lyric'])
    # with open("lyric.txt", 'wb') as code:
    #     code.write(lyrics)
    #     code.flush()
    # 测试歌词下载代码结束

    if link.find('stream.qqmusic.qq.com') == -1:
        print(f"无法加载资源文件！解析歌曲下载地址失败！{musicFileInfo}")
        return False

    # prepare
    localFile = f"{music['singer']} - {music['title']}.{music['extra']}".replace(
        "/", "\\")
    localLrcFile = f"{music['singer']} - {music['title']}.lrc".replace(
        "/", "\\")
    mShower = localFile
    my_path = download_home + music['singer'] + '/'

    if not onlyShowSingerSelfSongs:
        if not os.path.exists(my_path):
            os.mkdir(f"{my_path}")

    threadLock.acquire()  # 多线程上锁解决同时创建一个mkdir的错误
    my_path = f"{my_path}{music['album'] if musicAlbumsClassification else ''}"

    try:
        if not os.path.exists(my_path):
            os.mkdir(f"{my_path}")
    except:
        pass
    threadLock.release()
    localFile = os.path.join(my_path, f"{localFile}")
    localLrcFile = os.path.join(my_path, f"{localLrcFile}")

    # 下载歌词
    if not os.path.exists(localLrcFile):
        print(f"本地歌词文件不存在,准备自动下载: [{localLrcFile}].")
        # lyric = getQQMusicMediaLyric(songmid)  # lyric trans
        lyric = QQApi.getQQMusicLyricByMacApp(musicid)
        if lyric['lyric'] != '':
            # "retcode": 0,
            # "code": 0,
            # "subcode": 0,
            # {'retcode': -1901, 'code': -1901, 'subcode': -1901}
            # 外语歌曲有翻译 但是👴不需要！
            lyric = base64.b64decode(lyric['lyric'])
            try:
                with open(localLrcFile, 'wb+') as code:
                    code.write(lyric)
                    code.flush()
            except:
                print("歌词获取出错了！")
        else:
            print(f"歌词获取失败!服务器上搜索不到此首 [{music['singer']} - {music['title']}] 歌曲歌词!")

    # 下载歌曲
    if os.path.exists(localFile):
        if os.path.getsize(localFile) == int(music['size']):
            print(f"本地已下载,跳过下载 [{music['album']} / {mShower}].")
            return True
        else:
            print(
                f"本地文件尺寸不符: {os.path.getsize(localFile)}/{int(music['size'])},开始覆盖下载 [{mShower}].")
    print(f'正在下载 | {music["album"]} / {musicFileInfo}')
    f = requests.get(link)
    with open(localFile, 'wb') as code:
        code.write(f.content)
        code.flush()

    return True
