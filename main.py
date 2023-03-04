# -*- coding: utf-8 -*-
#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - main.py
#  @修改时间    : 2023-03-04 09:44:23
#  @上次修改    : 2023/3/4 下午9:44
import json
import math
import os
import threading
from time import sleep

from src.Api.Netease import Netease

parseThreadSize = 1
"""
协程线程池容量
"""

# mConcurrentPool = concurrent.futures.ThreadPoolExecutor(max_workers=parseThreadSize)
"""
协程线程池实例
"""


def clear():
    # print('\033c', end='')
    pass


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


def downAll(target, size):
    """
    一键下载所有搜索结果
    """
    num = math.ceil(size / 100)
    result = []
    for i in range(1, num + 1):
        (lst, meta) = getQQMusicSearch(target, i)
        songs = parseList(lst, target)
        result.extend(songs)
    return result


def parseList(mlist, target):
    """
    处理音乐列表
    如果需要屏蔽显示某些类型的歌曲，可以在这个函数里末尾处理

    Args:
        list (Array<T>): 歌曲列表
        target (str): 搜索的歌手名称,用于是否使用歌手名匹配歌曲歌手信息

    Returns:
        lists, songs: 处理过的数据数组
    """
    songs = formatList(mlist)
    if len(songs) == 0:
        return []
    lists = []
    for i in songs:
        if i['singer'] != target and onlyShowSingerSelfSongs:
            # print(f"{singer} not is {target}")
            continue
        if i['album'] == "未分类专辑" and ignoreNoAlbumMusic:
            continue

        # 开始检查歌曲过滤显示
        # 第三方修改歌曲可以在这里对歌曲做二次处理
        i["title"] = fixWindowsFileName2Normal(f'{i["title"]}')
        i["singer"] = fixWindowsFileName2Normal(f'{i["singer"]}')
        i["album"] = fixWindowsFileName2Normal(f'{i["album"]}')

        if needFilter(i["title"]):
            # print(f'过滤歌曲: {flacName}')
            continue

        # 通过检查 将歌曲放入歌曲池展示给用户 未通过检查的歌曲将被放弃并且不再显示
        lists.append(i)
    # 这部分其实可以只返回songs 但是代码我懒得改了 反正又不是不能用=v=
    return lists


def needFilter(fileName=''):
    """
    检查是否需要过滤本首歌曲

    """
    global filterList
    for it in filterList:
        if fileName.upper().find(it.upper()) != -1:
            return True
    return False


def matchToDownload():
    """
    匹配网易云歌单里的歌曲根据歌手名称专辑名称和歌曲名称精确匹配QQ曲库的歌曲
    """
    global netes_love, mConcurrentPool, onlyShowSingerSelfSongs
    onlyShowSingerSelfSongs = False
    print("因搜索算法的原因需要临时关闭[o 仅显示搜索的歌手歌曲]功能。")
    # pollCache = []  # 协程任务缓存池
    for neteaseMusic in netes_love:
        try:
            pre = download_home + \
                  neteaseMusic['author_simple'] + '/' + \
                  neteaseMusic['album']['name'] + "/"
            if os.path.exists(pre) and len(os.listdir(pre)) > 0:
                print(neteaseMusic['author_simple'] + ' - ' +
                      neteaseMusic['album']['name'] + " 已下载，跳过。")
                continue
            match = getQQMusicMatchSong(neteaseMusic)
            # pollCache.append(mConcurrentPool.submit(getQQMusicMatchSong, neteaseMusic))

            # for th in concurrent.futures.as_completed(pollCache):
            #     song = th.result()

            if match is not None:
                downSingle(match)
            else:
                print(
                    f"这首歌[{neteaseMusic['name']} - {neteaseMusic['author_simple']}]好像比较冷门, 服务器菌没找到捏QwQ。")
            sleep(2)
        except:
            print("出错了，继续运行。")


def _main(target=""):
    """
    主函数 不建议随意修改 请在上方函数修改
    """
    global download_home, dualThread, \
        searchKey, onlyShowSingerSelfSongs, \
        musicAlbumsClassification, ignoreNoAlbumMusic

    # fix create directory files error(if not exists)
    if not os.path.exists(download_home):
        os.mkdir(f"{download_home}")

    # 当关闭仅搜索歌手模式的时候 此处代码不应执行
    my_path = f'{download_home}{target + "/" if onlyShowSingerSelfSongs else ""}'
    if onlyShowSingerSelfSongs and not os.path.exists(my_path):
        os.mkdir(f"{my_path}")

    # 根据文件名获取下载链接
    # getDownloadLink("RS01003w2xz20QlUZt.flac")

    # filename = "ID9TZr-ensC/-rJ2t6-atFsm+sRG+2S6CqS"
    # filename = decryptText(filename, qq)
    # 解密后 RS01 003w2xz20QlUZt . flac
    page = 1
    while True:
        (lst, meta) = getQQMusicSearch(target, page)
        songs = parseList(lst, meta['searchKey'])
        while True:
            add = 1
            span = '  '

            clear()
            print("==== Welcome to Digit High Quality Music Download Center ====\n")
            print("==== \t\tCreative By QiuChenly\t\t ====")

            if add > 9:
                span = " "
            if add > 99:
                span = ""
            for li in songs:
                print(f"{add}{span}{li['readableText']}")
                add += 1
            willDownAll = False
            print(f"""
==== 获取列表成功.共{meta['size']}条搜索结果,当前第{page}页,{f'第{meta["next"]}页仍有更多数据' if meta['next'] != -1 else '下一页没有数据了'}. ====
p 切换上一页 (Previous)
n 切换下一页 (Next)
a 一键下载本页所有歌曲 (All)
l 一键下载所有页面歌曲 (All)
1 <输入1/2/3> 若要下载某一首,请输入歌曲前的序号 (Single)
s [{searchKey}] 修改搜索关键词 (Search)
t [{dualThread}] 修改当前线程并发数 (ThreadPool)
h 修改当前下载缓存的主目录 [{download_home}] (Download Home)
o [{'已开启' if onlyShowSingerSelfSongs else '已关闭'}] 切换模式:仅显示搜索的歌手歌曲 (OnlyMatchSinger&Songer)
i [{'已开启' if ignoreNoAlbumMusic else '已关闭'}] 切换模式:屏蔽无所属专辑歌曲 (IgnoreNoAlbumSong)
c [{'已开启' if musicAlbumsClassification else '已关闭'}] 切换模式:按照专辑名称分文件夹归档音乐歌曲文件 (Music Albums Classification)
m [{'已可用' if len(netes_love) > 0 else '不可用'}] 根据已登录的网易云账号歌单进行批量匹配下载 当前获取到了歌单中全部[{len(netes_love)}首歌曲]

==== 请在下方输入指令 ====
>""", end='')
            inputKey = input()
            if inputKey == "n":
                break
            elif inputKey == "o":
                onlyShowSingerSelfSongs = not onlyShowSingerSelfSongs
                saveConfigs()
                return _main(searchKey)
            elif inputKey == "i":
                ignoreNoAlbumMusic = not ignoreNoAlbumMusic
                saveConfigs()
                return _main(searchKey)
            elif inputKey == 'm':
                if len(netes_love) == 0:
                    checkUseForUpdateNetEase(True)
                    return _main(searchKey)
                else:
                    matchToDownload()
            elif inputKey == "s" or inputKey == "h":
                print(
                    f"请输入新的{'搜索关键词' if inputKey == 's' else '下载主目录'}:", end='')
                if inputKey == 'h':
                    download_home = input()
                    download_home = download_home.replace(' ', '')
                    if not download_home.endswith('/'):
                        download_home += '/'
                else:
                    searchKey = input()
                saveConfigs()
                _main(searchKey)
                return
            elif inputKey == 'a':
                # 下载本页所有歌曲
                willDownAll = True
            elif inputKey == 'l':
                songs = downAll(target, meta['size'])
                willDownAll = True
            elif inputKey == 't':
                print("请输入线程数:", end='')
                dualThread = int(input())
                saveConfigs()
                continue
            elif inputKey == 'c':
                musicAlbumsClassification = not musicAlbumsClassification
                saveConfigs()
                continue
            elif inputKey == 'p':
                page -= 2
                if page + 1 < 1:
                    page = 0
                break
            if willDownAll:
                thList = []
                for mp3 in songs:
                    th = threading.Thread(target=downSingle, args=(mp3,))
                    thList.append(th)
                    th.start()
                    if len(thList) == dualThread:
                        while len(thList) > 0:
                            thList.pop().join()
                while len(thList) > 0:
                    thList.pop().join()
            else:
                op = -1
                try:
                    op = int(inputKey)
                except:
                    print("输入无效字符,请重新输入。")
                    continue
                it = songs[op - 1]
                downSingle(it)
            print("下载完成!")
        page += 1


def saveConfigs():
    """
    保存设置
    """
    cfg = json.dumps({
        'dualThread': dualThread,
        'download_home': download_home,
        'searchKey': searchKey,
        'onlyShowSingerSelfSongs': onlyShowSingerSelfSongs,
        'musicAlbumsClassification': musicAlbumsClassification,
        'ignoreNoAlbumMusic': ignoreNoAlbumMusic,
        'netes_love': netes_love
    }, ensure_ascii=False).encode()
    with open(cfgName, "wb") as cf:
        cf.write(cfg)
        cf.flush()


download_home = ""
"""
下载的文件要保存到哪里(目录) /Volumes/data类似于windows上的C:/
    
就是你自定义的文件夹名称 随便指定 会自动创建

本参数已自动处理 不建议修改
"""

dualThread = 5
"""
多线程下载 线程数量
#####  如果你的宽带>=1000Mbps 可以适当调整至64
#####  100Mbps左右的小宽带不建议调高 会导致带宽不足连接失败
"""

searchKey = "周杰伦"
"""
默认搜索Key
"""

onlyShowSingerSelfSongs = False
"""
###  搜索歌曲名称时是否强制指定歌手和搜索key一致，用于过滤非本歌手的歌曲
如果是False,则显示所有搜索结果 如果你只想搜索某个歌手则可以开启本选项 默认关闭
#### 如何理解本选项？ 搜索结果是按照[时间] [歌手] - [歌名]排序的，你搜索的关键词searchKey严格匹配[歌手]选项,不是你搜索的歌手的歌则会强制过滤显示，如果你需要切换显示模式则输入 o 即可显示搜索未过滤结果
"""

musicAlbumsClassification = True
"""
音乐文件自动归档到单独的专辑文件夹中,如果关闭那么就不会生成专辑目录,默认自动按照专辑名称分类归档音乐文件
"""

cfgName = "config.json"
"""
配置项名称
"""

ignoreNoAlbumMusic = True
"""
忽略未分类专辑 只加载和显示有专辑收录的歌曲 过滤大部分串烧Dj之类的傻狗资源
"""


def initEnv():
    """
    第一次使用初始化环境信息 可以删除config.json，会自动创建初始化。
    """
    global download_home
    download_home = os.getcwd() + '/music/'  # 自动定位到执行目录，兼容Windows默认配置。
    saveConfigs()


filterList = []
"""
关键词过滤数组 注意 英文字母自动upper到大写比对 所以只需要写一次即可 如 DJ Dj 只需要写 ‘DJ’即可 自动到大写比对 
"""

# 初次使用即保存配置项
if not os.path.exists(cfgName):
    initEnv()

nete = Netease()

netes_love = []

# read default config
with open(cfgName, encoding='utf-8') as cfg:
    cfgLst = cfg.read()
    params: dict = json.loads(cfgLst)
    download_home = params['download_home']
    onlyShowSingerSelfSongs = bool(
        params.get('onlyShowSingerSelfSongs', False))
    searchKey = params.get('searchKey', "周杰伦")
    dualThread = int(params.get('dualThread', 5))
    musicAlbumsClassification = params.get('musicAlbumsClassification', True)
    filterList = params.get('filterList',
                            ['DJ', 'Remix', '即兴', '变调', 'Live', '伴奏', '版,', '版)', '慢四', "纯音乐", '二胡',
                             '串烧', '现场'])
    ignoreNoAlbumMusic = params.get('ignoreNoAlbumMusic', True)
    netes_love = params.get("netes_love", [])

    # 修复 删除了本地目录后缓存中的本地目录后，下次执行代码则还会去读这个目录 不存在导致FileNotFoundError: [Errno 2] No such file or directory错误
    if not os.path.exists(download_home):
        initEnv()


# print("请输入Cookie(扫码登录网页版qq音乐随便复制个请求的Cookie就可以): ")
# Cookie = input()
# setQQCookie(Cookie)


def checkUseForUpdateNetEase(noAsk=False):
    global netes_love
    """
    获取用户登录后的歌单列表 并根据需要指定下载某歌单所有歌曲 匹配QQ音乐无损曲库
    Returns:

    """
    if not noAsk:
        print("是否需要使用网易云音乐歌单焕新? y/n")
        k = input()
        if k != 'y':
            return

    if not nete.read_local():
        if not nete.qrLogin():
            return

    user = nete.getUserDetail()
    nickName = user['profile']['nickname']
    print(f"登录成功,欢迎使用,{nickName}.")
    # 准备拉取个人喜爱
    # mySubCount = nete.getUserLikeList()
    nete.save_local()
    ls = nete.getUserPlaylist()

    if len(netes_love) > 0:
        print("本地存在列表缓存，是否清除重新获取？y/n")
        k = input()
        if k != 'y':
            return

    playlist = ls[0]
    songSize = playlist['trackCount']
    songs = []
    page = 0
    batch = 300
    while True:
        tmp = nete.getPlayListAllMusic(playlist['id'], batch, page * batch)
        songs.extend(tmp)
        if (page + 1) * batch > songSize:
            break
        page += 1
    if len(songs) == 0:
        print("无法获取用户的歌单音乐,请退出重新登录试试.要清除Cookie并退出吗? y/n")
        k = input()
        if k == 'y':
            nete.save_local(True)
            clear()
            return checkUseForUpdateNetEase()
        return
    else:
        netes_love = songs
        saveConfigs()

# checkUseForUpdateNetEase()
# _main(searchKey)
