# -*- coding: utf-8 -*-
import base64
import requests
import os
import json
from pyDes import des, PAD_PKCS5, CBC

# 加解密工具


def decryptAndSetCookie(text: str):
    replace = text.replace("-", "").replace("|", "")

    if len(replace) < 10 or replace.find("%") == -1:
        return False

    split = replace.split("%")
    key = split[0]
    qq = str(decryptDES(split[1], key[0:8]), "utf-8")
    if len(qq) < 8:
        qq += "QMD"
    mkey = str(decryptDES(key, qq[0:8]), "utf-8")
    return mkey, qq   # 用对象的encrypt方法加密


# des解密
def decryptDES(strs: str, key: str): return des(
    key, CBC, key, padmode=PAD_PKCS5).decrypt(base64.b64decode(str(strs)))


# des加密
def encryptDES(text: str, key: str): return str(base64.b64encode(
    des(key, CBC, key, padmode=PAD_PKCS5).encrypt(text)), 'utf-8')


# 加密字符串
def encryptText(text: str, qq: str):
    key = ("QMD"+qq)[0:8]
    return encryptDES(text, key)


# 解密字符串
def decryptText(text: str, qq: str): return str(decryptDES(
    text.replace("-", ""), ("QMD" + qq)[0:8]), 'utf-8')


def getHead():
    return {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        "referer": "https://y.qq.com/portal/profile.html"
    }


sess = requests.Session()


def buildSearchContent(song: String = '', page=1, page_per_num=100):
    return {
        "comm": {"ct": "19", "cv": "1845"},
        "music.search.SearchCgiService": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {"query": song, "num_per_page": page_per_num, "page_num": page}
        }
    }


def searchMusic(key: String, page=1):
    # base url
    url = "https://u.y.qq.com/cgi-bin/musicu.fcg"
    # base data content from qqmusic pc-client-apps
    data = buildSearchContent(key, page)
    data = json.dumps(data, ensure_ascii=False)
    data = data.encode('utf-8')
    res = sess.post(url, data, headers=getHead())
    jsons = res.json()

    # 开始解析QQ音乐的搜索结果
    res = jsons['music.search.SearchCgiService']['data']
    list = res['body']['song']['list']
    meta = res['meta']

    # 数据清洗,去掉搜索结果中多余的数据
    list_clear = []
    for i in list:
        list_clear.append({
            'album': i['album'],
            'docid': i['docid'],
            'id': i['id'],
            'mid': i['mid'],
            'name': i['name'],
            'singer': i['singer'],
            'time_public': i['time_public'],
            'title': i['title'],
            'file': i['file'],
        })

    # rebuild json
    # list_clear: 搜索出来的歌曲列表
    # {
    #   size 搜索结果总数
    #   next 下一搜索页码 -1表示搜索结果已经到底
    #   cur  当前搜索结果页码
    # }
    return list_clear, {
        'size': meta['sum'],
        'next': meta['nextpage'],
        'cur': meta['curpage']
    }


def getCookie():
    uid = "822a3b85-a5c9-438e-a277-a8da412e8265"
    systemVersion = "1.7.2"
    versionCode = "76"
    deviceBrand = "360"
    deviceModel = "QK1707-A01"
    appVersion = "7.1.2"
    encIP = encryptText(
        f'{uid}{deviceModel}{deviceBrand}{systemVersion}{appVersion}{versionCode}', "F*ckYou!")

    u = 'http://8.136.185.193/api/Cookies'
    d = f'\{{"appVersion":"{appVersion}","deviceBrand":"{deviceBrand}","deviceModel":"{deviceModel}","ip":"{encIP}","systemVersion":"{systemVersion}","uid":"{uid}","versionCode":"{versionCode}"\}}'.replace(
        "\\", "")

    ret = sess.post(u, d, headers={
        'Content-Type': 'application/json;  charset=UTF-8'
    })
    return ret.text


def getDownloadLink(fileName):
    u = 'http://8.136.185.193/api/MusicLink/link'
    d = f'"{encryptText(fileName, mqq_)}"'
    ret = sess.post(
        u, d, headers={
            "Content-Type": "application/json;charset=utf-8"
        })
    return ret.text


def getMusicFileName(code, mid, format): return f'{code}{mid}.{format}'


mkey_ = ""
mqq_ = ""


def downSingle(it):
    # prepare
    localFile = f"{it['name']}.{it['extra']}"
    my_path = os.path.abspath(
        os.path.dirname(__file__)) + '/music/'
    my_path = "/Volumes/data/music/"
    my_path = f"{my_path}{it['album']}"
    if not os.path.exists(my_path):
        os.mkdir(f"{my_path}")
    localFile = os.path.join(my_path, f"{localFile}")
    if os.path.exists(localFile):
        print(f"本地已下载,跳过下载 [{it['name']}.{it['extra']}].")
        return True

    file = getMusicFileName(
        it['prefix'], it['mid'], it['extra'])
    log = f"{it['name']} [{it['notice']}] {round(int(it['size'])/1024/1024,2)}MB - {file}"
    print('正在下载 - '+log)
    link = getDownloadLink(file)
    if link.find('qqmusic.qq.com') == -1:
        print(f"解析歌曲下载地址失败！{log}")
        return False
    f = sess.get(link)
    with open(localFile, 'wb') as code:
        code.write(f.content)
        code.flush()
    return True


def _main():
    global mkey_
    global mqq_
    print("==== welcome to QQMusic digit High Quality Music download center ====")
    my_path = os.path.abspath(os.path.dirname(__file__)) + '/music/'
    if not os.path.exists(my_path):
        os.mkdir(f"{my_path}")

    cookie = getCookie()

    mkey, qq = decryptAndSetCookie(cookie)
    mkey_ = mkey
    mqq_ = qq

    # 根据文件名获取下载链接
    # getDownloadLink("RS01003w2xz20QlUZt.flac")

    # filename = "ID9TZr-ensC/-rJ2t6-atFsm+sRG+2S6CqS"
    # filename = decryptText(filename, qq)
    # # 解密后 RS01 003w2xz20QlUZt . flac

    target = "周杰伦"
    page = 1
    while True:
        (list, meta) = searchMusic(target, page)
        if meta['next'] != -1:
            print(f'获取列表成功,当前第{page}页,共搜索到{meta["size"]}条数据.')
            add = 1
            span = "  "
            songs = []
            for i in list:
                singer = i['singer'][0]['name']
                if singer != target:
                    # print(f"{singer} not is {target}")
                    continue
                if add > 9:
                    span = " "
                if add > 99:
                    span = ""

                id = i["file"]
                # 批量下载不需要选择音质 直接开始解析为最高音质 枚举
                code = ""
                format = ""
                qStr = ""
                fsize = 0
                mid = id['media_mid']
                if int(id['size_hires']) != 0:
                    # 高解析无损音质
                    code = "RS01"
                    format = "flac"
                    qStr = "高解析无损 Hi-Res"
                    fsize = int(id['size_hires'])
                elif int(id['size_flac']) != 0:
                    isEnc = False  # 这句代码是逆向出来的 暂时无效
                    if(isEnc):
                        code = "F0M0"
                        format = "mflac"
                    else:
                        code = "F000"
                        format = "flac"
                    qStr = "无损品质 FLAC"
                    fsize = int(id['size_flac'])
                elif int(id['size_320mp3']) != 0:
                    code = "M800"
                    format = "mp3"
                    qStr = "超高品质 320kbps"
                    fsize = int(id['size_320mp3'])
                elif int(id['size_192ogg']) != 0:
                    isEnc = False  # 这句代码是逆向出来的 暂时无效
                    if(isEnc):
                        code = "O6M0"
                        format = "mgg"
                    else:
                        code = "O600"
                        format = "ogg"
                    qStr = "高品质 OGG"
                    fsize = int(id['size_192ogg'])
                elif int(id['size_128mp3']) != 0:
                    isEnc = False  # 这句代码是逆向出来的 暂时无效
                    if(isEnc):
                        code = "O4M0"
                        format = "mgg"
                    else:
                        code = "M500"
                        format = "mp3"
                    qStr = "标准品质 128kbps"
                    fsize = int(id['size_128mp3'])
                elif int(id['size_96aac']) != 0:
                    code = "C400"
                    format = "m4a"
                    qStr = "低品质 96kbps"
                    fsize = int(id['size_96aac'])
                songs.append({
                    'prefix': code,
                    'extra': format,
                    'notice': qStr,
                    'mid': mid,
                    'size': fsize,
                    'name': f'{singer} - {i["title"]}',
                    'album': i["album"]['title']
                })
                print(
                    f'{add} {span}{i["time_public"]} {singer} - {i["title"]}')
                add += 1
            willDownAll = False
            while True:
                print("\n下一页直接输入n回车即可\n请输入下载的歌曲序号:", end='')
                inputKey = input()
                if inputKey == "n":
                    break
                elif inputKey == 'a':
                    # 下载本页所有歌曲
                    willDownAll = True
                if willDownAll:
                    for mp3 in songs:
                        downSingle(mp3)
                else:
                    op = int(inputKey)
                    it = songs[op-1]
                    downSingle(it)
                print("下载完成!")
            page += 1
        else:
            break
    print()


_main()
