#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - Tools.py
#  @修改时间    : 2023-08-02 03:21:29
#  @上次修改    : 2023/8/2 上午3:21

# 部分函数功能优化，错误修复
#  @作者         : QingXuDw
#  @邮件         : wangjingye55555@outlook.com
import json
import os
import threading
import requests
from mutagen.flac import FLAC, Picture
from mutagen import id3
from mutagen.id3 import ID3, APIC, USLT, TPE1, TXXX, TPE2, TRCK, TDRC, TPUB, TIT2, TALB, TPOS, TCON, COMM, TLAN, \
    Encoding
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
    saveLyric = config['concurrency']['saveLyric']

    header = {}
    super_music_info = None
    link = None
    if platform == 'qq':
        musicid = music['musicid']
        albumMid = music['albumMid']

        info = QQApi.getAlbumInfomation(albumMid)
        music['singer'] = info['AlbumInfoServer']['data']['singer']['singerList'][0]['name'] \
            if info['AlbumInfoServer']['code'] != 104400 else music['singer']
        file = QQApi.getQQMusicFileName(music['prefix'], music['mid'], music['extra'])
        musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}] {music['size']} - {file}"
        link = handleQQ(music, musicFileInfo)  # 由于QQ歌曲的特殊性 这里处理一下获取专辑艺术家信息
        super_music_info = {
            **music,
            'source_platform': "QQ",
            'source_platform_music_id': music['musicid']
            #  'lrcUrl':''
        }
    elif platform == 'kw':
        link = handleKuwo(music['mid'], '1000kape')  # music['prefix'] + 'k' + music['extra']
        tlt = music['title']
        music['title'] = tlt.replace("&nbsp;", " ")
        if link is not None:
            music['extra'] = 'flac' if link.find(".flac?") != -1 else 'mp3'
            if "&" in music['singer']:
                music['artists'] = [{
                    'name': i
                } for i in music['singer'].split("&")]
                music['singer'] = music['artists'][0]['name']
        musicFileInfo = f"{music['singer']} - {music['title']} [{music['notice']}]"
        super_music_info = {
            **music,
            'source_platform': "KuWo",
            'source_platform_music_id': music['mid']
            #  'lrcUrl':''
        }
    elif platform == 'mg':
        super_music_info = handleMigu(music['mid'], music['prefix'])
        if super_music_info:
            super_music_info = {
                **super_music_info,
                **music
            }
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
    if platform == 'qq':  # 只下载qq来源
        # lyric = getQQMusicMediaLyric(songmid)  # lyric trans
        lyric = QQApi.getQQMusicLyricByMacApp(musicid)
        if lyric != '':
            # "retcode": 0,
            # "code": 0,
            # "subcode": 0,
            # {'retcode': -1901, 'code': -1901, 'subcode': -1901}
            # 外语歌曲有翻译 但是👴不需要！
            super_music_info['lrcContent'] = lyric

            # 单独下载lrc歌词文件
            if saveLyric == True:
                with open(localLrcFile, 'w', encoding='utf-8') as f:
                    f.write(lyric)
        else:
            print(f"歌词获取失败!服务器上搜索不到此首 [{music['singer']} - {music['title']}] 歌曲歌词!")
    # 下载歌曲
    if os.path.exists(localFile):
        print(f"本地已下载,跳过下载 [{music['album']} / {mShower}].")
        if super_music_info:
            fulfillMusicMetaData(localFile, super_music_info)
        return {
            'code': 200,
            'msg': "本地已下载,跳过下载"
        }
    print(f'正在下载 | {music["album"]} / {musicFileInfo}')
    f = requests.get(link, headers=header)
    with open(localFile, 'wb') as code:
        code.write(f.content)
        code.flush()
        code.close()

    if super_music_info:
        fulfillMusicMetaData(localFile, super_music_info)
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


import zhconv


def itunes_search_music_meta(albumName, songName, musicTitle):
    # 把古汉语晚替换成简体中文晚
    musicTitle = musicTitle.encode().replace(b'\xe6\x99\x9a', b'\xe6\x99\xa9').decode()

    url = "https://itunes.apple.com/search"

    if musicTitle:
        musicTitle1 = musicTitle.split("(")[0].replace(' ', '')

    print("正在查询...", albumName, songName, musicTitle1)
    querystring = {
        "term": musicTitle1 + " " + songName,
        "media": "music",
        "entity": "song",
        "limit": "20",
        "country": "CN"
    }

    response = requests.request("GET", url, params=querystring)

    try:
        response = response.json()
        for meta in response['results']:
            trackCensoredNameNative = meta['trackCensoredName'].split("(")[0].replace(' ', '').replace('.', '')
            trackCensoredName = zhconv.convert(trackCensoredNameNative, 'zh-cn')
            # collectionArtistName artistName
            if 'collectionArtistName' in meta:
                artistName = meta['collectionArtistName']
            else:
                artistName = meta['artistName']
            if artistName == songName and trackCensoredName == musicTitle1:
                print(albumName, songName, musicTitle1, "成功精确匹配到了iTunes曲库信息。")
                return meta
        print(albumName, songName, musicTitle1, "没有匹配到iTunes曲库中的信息。")
        return None
    except Exception as e:
        print("iTunes 搜索过程中出现了意外。")
        return None


def search_qq_meta(albumName, songName, musicTitle, qqMusicID=None, albumId=''):
    if qqMusicID:
        infoAll = QQApi.getSingleMusicInfoAll(qqMusicID, albumId)
        detail = infoAll["get_song_detail"]
        album = infoAll["AlbumInfoServer"]['data']
        if detail['code'] != 0:
            # 如果没找到任何有效信息 则返回None
            return None
        infos = detail['data']
        print(albumName, songName, musicTitle, qqMusicID, "成功使用MusicID精确匹配到了QQ曲库信息。")
        return {
            "album": infos['track_info']['album'],
            "albumCollection": album,
            "info": infos['info'],
            'track_info': infos['track_info'],
            "extra": json.dumps(infos, ensure_ascii=False)
        }
    if musicTitle and musicTitle.find("Live") == -1:
        musicTitle1 = musicTitle.split("(")[0].replace(" ", "")
    else:
        musicTitle1 = musicTitle.replace("（", "(")
        musicTitle1 = musicTitle1.replace("）", ")")
    if '-' in musicTitle1:
        musicTitle1 = musicTitle1.split("-")[0]
    lst = QQApi.getQQSearchData(songName + ' ' + albumName, 1, 30)
    lst2 = QQApi.getQQSearchData(musicTitle + ' ' + albumName, 1, 30)
    lst3 = lst['data']['body']['song']['list']
    lst3.extend(lst2['data']['body']['song']['list'])
    for it in lst3:
        tempTitle = it['title'].replace(" ", '').split('(')[0]
        if it['album']['name'] == albumName and it['singer'][0]['name'] == songName and tempTitle == musicTitle1:
            print(albumName, songName, musicTitle1, "成功精确匹配到了QQ曲库信息。")
            return it
    print(albumName, songName, musicTitle1, "没有匹配到QQ曲库中的信息。")
    return None


def rebaseQQMuiscInfomation(originalInfo):
    info = {}
    for it in originalInfo:
        tpe = it['type']
        kvs = [{
            'type': it['title'],
            'value': it1['value'],
            'picurl': it1['picurl']
        } for it1 in it['content']]
        if tpe in info:
            info[tpe].extend(kvs)
        else:
            info[tpe] = kvs
    return info


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
        elif tpe.startswith(b'ID3'):
            fileType = 'mp3'
        else:
            print("不是受支持的歌曲类型文件，跳过元数据写入。")

    if fileType is None:
        return
    elif fileType == 'flac' or fileType == 'mp3':
        # music1 = FLAC("/Volumes/Disk1/周杰伦 - 晴天.flac")
        lyric = ""
        if 'lrcUrl' in metaDataInfo:
            # 下载歌词
            lrc = metaDataInfo['lrcUrl']
            lrcText = requests.get(lrc).content
            try:
                lrcText = lrcText.decode("utf-8")
            except Exception as e:
                lrcText = ""
            lyric = lrcText
        elif 'lrcContent' in metaDataInfo:
            # lrcContent 设置用于额外处理歌词内容需要自定义转码的情况 比如qq歌词
            lyric = metaDataInfo['lrcContent']
        else:
            print("无法为这首歌嵌入歌词文件。")

        albumImage = None
        # 下载封面
        if 'albumImgs' in metaDataInfo:
            albumImageBin = requests.get(metaDataInfo['albumImgs'][0]).content
            pic = Picture()
            pic.type = id3.PictureType.COVER_FRONT
            pic.data = convert_webp_bytes2jpeg_bytes(albumImageBin)
            pic.mime = u"image/jpeg"
            albumImage = pic

        # 歌手照片
        singerImage = None
        if 'singerImgs' in metaDataInfo:
            # 下载歌手封面
            singerImageBin = requests.get(metaDataInfo['singerImgs'][0]).content
            pic = Picture()
            pic.data = convert_webp_bytes2jpeg_bytes(singerImageBin)
            pic.type = id3.PictureType.ARTIST
            pic.mime = u"image/jpeg"
            singerImage = pic

        # 歌曲名称
        title = metaDataInfo['songName'] if 'songName' in metaDataInfo else metaDataInfo['title']

        artist = [it['name'] for it in metaDataInfo['artists']] if 'artists' in metaDataInfo else [
            metaDataInfo['singer']]
        # 设置专辑艺术家让专辑中歌曲能完整显示出来
        # TODO: 当存在多个专辑艺术家的时候无法确定谁才是此专辑主要作者 会引起分类错误 需要后期解决
        albumartist = [it['name'] for it in metaDataInfo['artists']] if 'artists' in metaDataInfo else [
            metaDataInfo['singer']
        ]

        album = metaDataInfo['album']
        # 备份音乐平台完整的元数据信息 方便用于后期二次处理
        extra_info_full = ""
        date = ''
        trackNumber = ''
        description = None
        label = None
        gener = []
        LANGUAGE = None
        otherImages = []
        discNumber = '1'
        trackCount = None
        discCount = None

        isQQMusicSource = metaDataInfo['source_platform'] == "QQ"

        # 如果是QQ源则有完整的元数据信息 所以我直接写入这个信息
        if isQQMusicSource:
            meta = search_qq_meta(
                metaDataInfo['album'],
                artist[0],
                title,
                metaDataInfo['source_platform_music_id'],
                metaDataInfo['albumMid']
            )
            extra_info_full = meta["extra"]
            date = meta['track_info']['time_public']
            # 专辑中歌曲的序号 iTunes里是最全的 qq搞什么鬼
            trackNumber = str(meta['track_info']['index_album'])

            # 专辑描述
            description = meta['albumCollection']['basicInfo']['desc']
            # 唱片公司
            label = meta['albumCollection']['company']['name']
            # GENRE 流派
            # genres 可能为 None
            geners = meta.get('albumCollection', {}).get('basicInfo', {}).get('genres')
            if geners is not None:
                for it in geners:
                    gener.append(it['name'])
            # 专辑艺术家
            albumartist = [it['name'] for it in meta['albumCollection']['singer']['singerList']]

            LANGUAGE = meta['albumCollection']['basicInfo']['language']

            info = rebaseQQMuiscInfomation(meta['info'])

            artist = [it['name'] for it in meta['track_info']['singer']]

            if 'lyric' in info:
                lyric = info['lyric']
                if len(lyric) > 0:
                    lyric = lyric[0]['value']

            # 加入曲谱信息 QQ音乐源特有的钢琴曲谱
            if 'OPERN' in info:
                sheets = info['OPERN']
                if len(sheets) > 0 and len(sheets) > 0:
                    opern = [d['picurl'] for d in sheets]
                    for img in opern:
                        albumCoverBin = requests.get(img).content
                        pic = Picture()
                        pic.type = id3.PictureType.OTHER
                        pic.data = albumCoverBin
                        pic.mime = u"image/jpeg"
                        im1 = pic
                        otherImages.append(im1)

            albumCover = f'https://y.qq.com/music/photo_new/T002R800x800M000{meta["album"]["pmid"]}.jpg'
            albumCoverBin = requests.get(albumCover).content
            pic = Picture()
            pic.type = id3.PictureType.COVER_FRONT
            pic.data = albumCoverBin
            pic.mime = u"image/jpeg"

            albumImage = pic
            discNumber = '1'
            date = meta['track_info']['time_public']
            trackNumber = str(meta['track_info']['index_album'])
        else:
            # 测试iTunes元数据
            meta = itunes_search_music_meta(
                album,
                artist[0],
                title
            )
            if meta:
                albumCover = meta['artworkUrl100'].replace('100x100', '3000x3000')
                # print("albumCover = ",albumCover)
                albumCoverBin = requests.get(albumCover).content
                pic = Picture()
                pic.type = id3.PictureType.COVER_FRONT
                pic.data = albumCoverBin
                pic.mime = u"image/jpeg"
                albumImage = pic
                date = meta['releaseDate']
                trackNumber = str(meta['trackNumber'])
                trackCount = str(meta['trackCount'])
                discCount = str(meta['discCount'])
                discNumber = str(meta['discNumber'])
                gener = [meta['primaryGenreName']]
            else:
                meta = search_qq_meta(
                    metaDataInfo['album'],
                    artist[0],
                    title
                )
                if meta:
                    albumCover = f'https://y.qq.com/music/photo_new/T002R800x800M000{meta["album"]["pmid"]}.jpg'
                    albumCoverBin = requests.get(albumCover).content
                    pic = Picture()
                    pic.type = id3.PictureType.COVER_FRONT
                    pic.data = albumCoverBin
                    pic.mime = u"image/jpeg"
                    albumImage = pic
                    discNumber = '1'
                    date = meta['time_public']
                    trackNumber = str(meta['index_album'])
                    # music['trackCount'] = str(meta['index_album'])
                    # music['discCount'] =  str(meta['discCount'])
                    # music['discNumber'] = str(meta['index_cd'])
                    # music['GENRE'] = [meta['primaryGenreName']]
                else:
                    print(metaDataInfo['album'],
                          artist[0],
                          title, "很遗憾，只能写入基本数据信息.")

        source_platform = json.dumps({
            'platform': metaDataInfo['source_platform'],
            "musicId": metaDataInfo['source_platform_music_id'],
            "productby": "秋城落叶无损音乐 https://github.com/QiuChenlyOpenSource/QQFlacMusicDownloader".encode(
                "utf-8").decode(),
            "extra_info_full": extra_info_full.encode("utf-8").decode()
        }, ensure_ascii=False)
        # if 'source_platform' not in music:
        # 添加音乐元数据获取来源
        write_metadata_information(
            1 if fileType == 'flac' else 2,
            musicFile,
            lyric,
            album,
            date,
            title,
            artist,
            albumartist,
            trackNumber,
            discNumber,
            trackCount,
            discCount,
            description,
            label,
            gener,
            LANGUAGE,
            singerImage,
            albumImage,
            otherImages,
            source_platform
        )
        # fileName = musicFile.split("/")[-1]
        # fixName = musicFile.replace(fileName,"")
        # fixName  = fixName+ meta['artistName']+" - " +meta['trackCensoredName']+".flac"
        # os.rename(musicFile,fixName)


def write_metadata_information(
        type: int,
        musicFile: str,  # 文件路径
        lyric: str,  # 歌词信息
        album: str,  # 专辑名称,
        date: str,  # 发布年代
        title: str,  # 歌曲名称
        artist: list[str],  # 艺术家
        albumArtist: list[str],  # 专辑艺术家
        trackNumber,  # CD中的曲目序号
        discNumber,  # CD 磁碟序号
        trackCount,  # CD 中曲目总数量 Apple Music 特有
        discCount,  # CD 磁碟总数量 Apple Music 特有
        description,  # 专辑介绍
        publishCompany,  # 唱片公司
        gener: list[str],  # 流派 数组
        LANGUAGE,  # 语种
        singerImage,  # 歌手照片 数组
        albumImage,  # 专辑封面
        attachmentImgs,  # 其他图片 数组
        source_platform,  # 附加信息
):
    """

    Args:
        type: 1=Flac,2=mp3 可扩展
        musicFile:
        lyric:
        album:
        date:
        title:
        artist:
        albumArtist:
        trackNumber:
        discNumber:
        description:
        publishCompany:
        gener:
        LANGUAGE:
        singerImage:
        albumImage:
        attachmentImgs:
        source_platform:

    Returns:

    """
    music = None
    if type == 1:
        music = FLAC(musicFile)
        if 'LYRICS' not in music:
            music["LYRICS"] = lyric  # 写入歌词
        music['title'] = title

        # 艺术家
        music['artist'] = artist
        # 设置专辑艺术家让专辑中歌曲能完整显示出来
        music['albumartist'] = albumArtist
        # 专辑
        music['album'] = album
        music['DATE'] = date
        music['trackNumber'] = trackNumber
        music['discNumber'] = discNumber
        if trackCount: music['trackCount'] = trackCount
        if discCount: music['discCount'] = discCount
        if description: music['DESCRIPTION'] = description
        if publishCompany: music['LABEL'] = publishCompany
        music['GENRE'] = gener
        if LANGUAGE: music['LANGUAGE'] = LANGUAGE

        music.clear_pictures()

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
        music.add_picture(albumImage)
        if singerImage: music.add_picture(singerImage)
        # 加入其他图片
        for imgs in attachmentImgs:
            if imgs: music.add_picture(imgs)

        music["source_platform"] = source_platform
    elif type == 2:
        music = ID3(musicFile)
        music.clear()
        # 加入自定义标签头
        music["TXXX"] = TXXX(encoding=3, desc="source_platform", text=source_platform)

        music["TIT2"] = TIT2(encoding=3, text=title)

        # 提取时间戳和歌词
        if lyric: music.setall("USLT", [USLT(encoding=Encoding.UTF8, lang='chi', format=2, type=1, text=lyric)])

        # 写入流派
        if gener: music["TCON"] = TCON(encoding=3, text=gener)

        # 写入作曲家
        # music["TCOM"] = TCOM(encoding=3, text="John Smith")

        music["TPOS"] = TPOS(encoding=3, text=f'{discNumber}/{discCount}' if discCount else f'{discNumber}/1')

        # 写入歌手
        music["TPE1"] = TPE1(encoding=3, text=artist)

        # 专辑名称
        music["TALB"] = TALB(encoding=3, text=album)

        # 专辑艺术家
        music["TPE2"] = TPE2(encoding=3, text=albumArtist)

        # 发布日期
        music["TDRC"] = TDRC(encoding=3, text=date)

        # CD曲子序号
        music["TRCK"] = TRCK(encoding=3, text=trackNumber)

        # 歌曲介绍
        if description: music["COMM"] = COMM(encoding=3, lang='zho', desc='', text=description)

        # 语言
        if LANGUAGE: music["TLAN"] = TLAN(encoding=3, text=LANGUAGE)

        # 发布公司
        if publishCompany: music["TPUB"] = TPUB(encoding=3, text=publishCompany)

        # 在MP3的APIC框架中,type字段用于表示图片的类型,主要有以下几种:

        # 0 - 其他
        # 1 - 32x32像素的文件图标
        # 2 - 其他文件图标
        # 3 - 前面板封面图片
        # 4 - 后面板封面图片
        # 5 - 叠加图片
        # 6 - 插图
        # 7 - 歌手/表演者图片
        # 8 - 在电视屏幕捕获的图片
        # 9 - 光碟的激光雕刻图象
        # 10 - 媒体创作者/艺术家图片
        # 11 - 录音场所图片
        # 12 - 在活动过程中拍摄的图片
        # 写入封面图片
        music["APIC"] = APIC(encoding=3, mime='image/jpeg', type=3, desc='Cover', data=albumImage.data)

        # 写入歌手图片
        if singerImage: music["APIC"] = APIC(encoding=3, mime='image/jpeg', type=7, desc='', data=singerImage)
    else:
        return None
    music.save()
    pass
