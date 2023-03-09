#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - Tools.py
#  @修改时间    : 2023-03-09 06:01:38
#  @上次修改    : 2023/3/9 下午6:01
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


def fixWindowsFileName2Normal(texts=''):
    """
    修正windows的符号问题
    “?”、“、”、“╲”、“/”、“*”、““”、“”“、“<”、“>”、“|” " " ":"

    参数:
        texts (str, optional): 通常类型字符串. 默认值为 ''.

    返回值:
        str: 替换字符后的结果
    """
    targetChars = {
        '|': ',',
        '/': ' - ',
        '╲': ' - ',
        '、': '·',
        '“': '"',
        '”': '"',
        '*': 'x',
        '?': '？',  # fix for sample: Justin Bieber - What do you mean ? (Remix)
        '<': '《',
        '>': '》',
        ' ': '',
    }
    for suffix in targetChars:
        fix = targetChars[suffix]
        texts = texts.replace(suffix, fix)
    return texts


def handleKuwo(mid: str, type: str):
    from web.API.kw import kw
    url = kw.getDownloadUrlV2(mid, type)
    if url.text == 'failed' or url.text == 'res not found':
        return None
    return url.json()['url']


def handleMigu(mid: str, _type: str):
    from web.API.kw import mg
    url = mg.getDownloadLink(mid, _type)
    if url is None:
        return None
    return url


def handleWyy(mid):
    from web.API.es import netes
    url = netes.getMusicUrl(mid)
    print("解析网易云歌曲下载接口:", url)
    if url['br'] == -1:
        return None
    return url['url']


def handleQQ(music, musicFileInfo):
    songmid = music['songmid']
    # musicid = music['musicid']
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
    if link.find('stream.qqmusic.qq.com') == -1:
        print(f"无法加载资源文件！解析歌曲下载地址失败！{musicFileInfo}，错误细节:" + link)
        link = None
    return link


def downSingle(music, platform, download_home, onlyShowSingerSelfSongs=False, musicAlbumsClassification=True):
    """
    多渠道下载
    Args:
        music: kwid or qqmusicobject
        platform: qq kw wyy mg
        download_home:
        onlyShowSingerSelfSongs:
        musicAlbumsClassification:

    Returns:

    """
    header = {}
    if platform == 'qq':
        musicid = music['musicid']
        file = QQApi.getQQMusicFileName(music['prefix'], music['mid'], music['extra'])
        musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}] {music['size']} - {file}"
        link = handleQQ(music, musicFileInfo)
    elif platform == 'kw':
        link = handleKuwo(music['mid'], '1000kape')  # music['prefix'] + 'k' + music['extra']
        musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}]"
    elif platform == 'mg':
        link = handleMigu(music['mid'], music['prefix'])
        musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}]"
    elif platform == 'wyy':
        link: str = handleWyy(music['mid'])
        if link is not None:
            music['extra'] = 'flac' if link.find(".flac?") != -1 else 'mp3'
        music['singer'] = music['author_simple']
        music["album"] = music['album']
        musicFileInfo = f"{music['author_simple']} - {music['title']}"
    elif platform == 'myfreemp3':
        link = music['prefix']
        musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}]"
        header = {
            "accept": "application/json, text/plain, */*",
            "content-type": "application/json",
            "origin": "https://tools.liumingye.cn",
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50"
        }
    else:
        link = None
        musicFileInfo = ''

    # 测试歌词下载保存接口代码
    # lyric = getQQMusicMediaLyric(songmid) # 早期方法 已弃用
    # lyric = getQQMusicLyricByMacApp(musicid)
    # lyric = getQQMusicLyricByWeb(musicid)
    # lyrics = base64.b64decode(lyric['lyric'])
    # with open("lyric.txt", 'wb') as code:
    #     code.write(lyrics)
    #     code.flush()
    # 测试歌词下载代码结束

    if link is None:
        return {
            'msg': f"无法加载资源文件！解析歌曲下载地址失败！",
            'code': "-1"
        }

    # prepare
    localFile = f"{music['singer']} - {music['title']}.{music['extra']}".replace(
        "/", "\\")
    localLrcFile = f"{music['singer']} - {music['title']}.lrc".replace(
        "/", "\\")
    mShower = localFile
    my_path = download_home + music['singer'] + '/'

    # 特殊字符处理
    music["title"] = fixWindowsFileName2Normal(f'{music["title"]}')
    music["singer"] = fixWindowsFileName2Normal(f'{music["singer"]}')
    music["album"] = fixWindowsFileName2Normal(f'{music["album"]}')

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
    if not os.path.exists(localLrcFile) and platform == 'qq':  # 只下载qq来源
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
        if platform != 'qq':
            print(f"本地已下载,跳过下载 [{music['album']} / {mShower}].")
            return {
                'code': 200,
                'msg': "本地已下载,跳过下载"
            }
        if os.path.getsize(localFile) == int(music['size']):
            print(f"本地已下载,跳过下载 [{music['album']} / {mShower}].")
            return {
                'code': 200,
                'msg': "本地已下载,跳过下载"
            }
        else:
            print(
                f"本地文件尺寸不符: {os.path.getsize(localFile)}/{int(music['size'])},开始覆盖下载 [{mShower}].")
    print(f'正在下载 | {music["album"]} / {musicFileInfo}')
    f = requests.get(link, headers=header)
    with open(localFile, 'wb') as code:
        code.write(f.content)
        code.flush()
    return {
        'code': 200,
        'msg': "下载完成"
    }
