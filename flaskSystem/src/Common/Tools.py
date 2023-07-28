#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - Tools.py
#  @修改时间    : 2023-07-28 08:32:25
#  @上次修改    : 2023/7/28 下午8:32

# 部分函数功能优化，错误修复
#  @作者         : QingXuDw
#  @邮件         : wangjingye55555@outlook.com
import base64
import json
import os
import threading
import requests
from mutagen.flac import FLAC, Picture
from mutagen import id3
from PIL import Image
import io

from flaskSystem.API.qq import QQApi


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
    修正windows的符号问题\n
    限制规则：https://learn.microsoft.com/en-us/windows/win32/fileio/naming-a-file （2023/03/13）

    @作者: QingXuDw\n
    @邮件: wangjingye55555@outlook.com

    参数:
        texts (str, optional): 通常类型字符串. 默认值为 ''.

    返回值:
        str: 替换字符后的结果
    """
    RESERVED_CHARS = [ord(c) for c in list('<>:\"/\\|?*')]  # Reserved characters in Windows
    CONTROL_CHARS = list(range(0, 32, 1))  # Control characters of ascii
    REP_RESERVED_CHARS = [ord(c) for c in
                          list('《》：“、、-？+')]  # Replace reserved characters in Windows with similar characters
    # noinspection PyTypeChecker
    TRANS_DICT = dict(zip(CONTROL_CHARS + RESERVED_CHARS, [None] * 32 + REP_RESERVED_CHARS))
    RESTRICT_STRS = ['con', 'prn', 'aux', 'nul', 'com0', 'com1',  # Restricted file names in Windows
                     'com2', 'com3', 'com4', 'com5', 'com6', 'com7',
                     'com8', 'com9', 'lpt0', 'lpt1', 'lpt2', 'lpt3',
                     'lpt4', 'lpt5', 'lpt6', 'lpt7', 'lpt8', 'lpt9']
    trans_table = str.maketrans(TRANS_DICT)
    texts = texts.translate(trans_table)
    equal_text = texts.casefold()
    for restrict_str in RESTRICT_STRS:
        if equal_text == restrict_str:
            texts = f'_{texts}_'
            break
    return texts.strip()


def handleKuwo(mid: str, type: str):
    from flaskSystem.API.kw import kw
    # url = kw.getDownloadUrlV2(mid, type)
    # if url.text == 'failed' or url.text == 'res not found':
    #     return None
    # return url.json()['url']

    url = kw.getDownloadUrlByApp(mid)
    if len(url) < 10:  # 这里会返回一个很长的网址 所以一定超过10判定成功
        return None
    return url


def handleMigu(mid: str, _type: str):
    from flaskSystem.API.kw import mg
    url = mg.getDownloadLink(mid, _type)
    if url is None:
        return None
    return url


def handleWyy(mid):
    from flaskSystem.API.es import netes
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


def downSingle(music, download_home, config):
    """
    多渠道下载
    Args:
        music: kwid or qqmusicobject
        download_home:
        config:

    Returns:

    """
    # platform: qq kw wyy mg myfreemp3
    platform = config['platform']
    onlyShowSingerSelfSongs = config['onlyMatchSearchKey']
    musicAlbumsClassification = config['classificationMusicFile']

    header = {}
    super_music_info = None
    if platform == 'qq':
        musicid = music['musicid']
        file = QQApi.getQQMusicFileName(music['prefix'], music['mid'], music['extra'])
        musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}] {music['size']} - {file}"
        link = handleQQ(music, musicFileInfo)
    elif platform == 'kw':
        link = handleKuwo(music['mid'], '1000kape')  # music['prefix'] + 'k' + music['extra']
        musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}]"
    elif platform == 'mg':
        super_music_info = handleMigu(music['mid'], music['prefix'])
        link = super_music_info['url']  # music['prefix'] + 'k' + music['extra']
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
    localFile = fixWindowsFileName2Normal(f"{music['singer']} - {music['title']}.{music['extra']}")
    localLrcFile = fixWindowsFileName2Normal(f"{music['singer']} - {music['title']}.lrc")
    mShower = localFile
    my_path = download_home + fixWindowsFileName2Normal(music['singer']) + '/'

    threadLock.acquire()  # 多线程上锁解决同时创建一个mkdir的错误
    if musicAlbumsClassification:
        if not os.path.exists(my_path):
            os.mkdir(f"{my_path}")

    my_path = f"{my_path}{fixWindowsFileName2Normal(music['album']) if musicAlbumsClassification else ''}"

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
            if super_music_info:
                fulfillMusicMetaData(localFile, super_music_info)
            return {
                'code': 200,
                'msg': "本地已下载,跳过下载"
            }
        sz = os.path.getsize(localFile)
        sz = f"%.2fMB" % (sz / 1024 / 1024)
        if sz == music['size']:
            print(f"本地已下载,跳过下载 [{music['album']} / {mShower}].")
            if super_music_info:
                fulfillMusicMetaData(localFile, {})
            return {
                'code': 200,
                'msg': "本地已下载,跳过下载"
            }
        else:
            print(
                f"本地文件尺寸不符: {os.path.getsize(localFile)}/{music['size']},开始覆盖下载 [{mShower}].")
    print(f'正在下载 | {music["album"]} / {musicFileInfo}')
    f = requests.get(link, headers=header)
    with open(localFile, 'wb') as code:
        code.write(f.content)
        code.flush()
        if super_music_info:
            fulfillMusicMetaData(localFile, {})
    return {
        'code': 200,
        'msg': "下载完成"
    }


def convert_webp_bytes2jpeg_bytes(webp_bytes=b''):
    """
    转换webp二进制数据为jpeg专辑封面数据
    Args:
        webp_bytes: webp https response

    Returns:
        JPEG二进制数据流
    """
    temp = io.BytesIO()
    Image.open(io.BytesIO(webp_bytes)).convert("RGB").save(temp, format="JPEG", quality=100)
    return temp.getvalue()


def fulfillMusicMetaData(musicFile, metaDataInfo):
    """
    填充歌曲元数据 不同平台返回的元数据不完整 需要单独处理
    Args:
        musicFile: 音乐文件路径
        metaDataInfo: 元数据内容

    Returns:

    """
    fileType = None
    with open(musicFile, "rb") as mu:
        tpe = mu.read(128)
        if tpe.startswith(b'fLaC'):
            fileType = 'flac'

    if fileType == None:
        return
    if fileType == 'flac':
        simple = FLAC("/Volumes/data/Jay/周杰伦 - 反方向的钟.flac")
        music = FLAC(musicFile)

        if 'source_platform' not in music:
            # 添加音乐元数据获取来源
            music["source_platform"] = json.dumps({
                'platform': metaDataInfo['source_platform'],
                "musicId": metaDataInfo['source_platform_music_id']
            })

        if 'LYRICS' not in music:
            # 下载歌词
            lrc = metaDataInfo['lrcUrl']
            lrcText = requests.get(lrc).content.decode("utf-8")
            music["LYRICS"] = lrcText

        # 下载封面
        albumImage = requests.get(metaDataInfo['albumImgs'][0]).content

        music.clear_pictures()

        pic = Picture()
        pic.type = id3.PictureType.COVER_FRONT
        pic.data = convert_webp_bytes2jpeg_bytes(albumImage)
        pic.mime = u"image/jpeg"
        im1 = pic
        # 在使用Mutagen库向音频文件添加图片元数据时,type参数表示图片的类型,主要有以下几种:
        #
        # 0 - 其他
        # 1 - 32x32像素 PNG 文件图标
        # 2 - 其他文件图标
        # 3 - 前封面
        # 4 - 后封面
        # 5 - 素材(艺术家/表演者/剧组照片)
        # 6 - 录音师/录音室/制作人/指挥照片
        # 7 - 演出画面或电影/视频画面截图
        # 8 - 鱼眼图的缩图
        # 9 - 艺术家/表演者照片
        # 10 - 发行商/制作商徽标
        # 11 - 海报或横幅
        # 所以,常见的使用场景是:
        #
        # 专辑封面:type=3(前封面)
        # 歌曲封面:type=3(前封面)
        # 艺术家图片:type=5或9
        music.add_picture(im1)

        # 下载歌手封面
        singerImage = requests.get(metaDataInfo['singerImgs'][0]).content
        pic = Picture()
        pic.data = convert_webp_bytes2jpeg_bytes(singerImage)
        pic.type = id3.PictureType.ARTIST
        pic.mime = u"image/jpeg"
        music.add_picture(pic)

        # 标题
        music['title'] = metaDataInfo['songName']

        # 艺术家
        music['artist'] = [it['name'] for it in metaDataInfo['artists']]

        # 专辑
        music['album'] = metaDataInfo['album']
        music.save()
    print("")
