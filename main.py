# -*- coding: utf-8 -*-
import base64
from email import header
from tokenize import String
import requests
import json
from pyDes import des, PAD_PKCS5, CBC

# 加解密工具
###
# 加密解密
# decodeOrEncode 0为解密 1为加密 默认加密模式
###


def decryptAndSetCookie(text: str):
    replace = text.replace("-", "").replace("|", "")

    if len(replace) < 10 or replace.find("%") is -1:
        return False

    split = replace.split("%")
    key = split[0]
    qq = decryptDES(split[1], key[0:8])
    if len(qq) < 8:
        qq += "QMD"
    mkey = decryptDES(key, qq[0:8])
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
def decryptText(text: str, qq: str): return decryptDES(
    text.replace("-", ""), ("QMD" + qq)[0:8])


def getHead():
    return {
        'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36',
        'content-type': 'application/json; charset=UTF-8',
        "referer": "https://y.qq.com/portal/profile.html"
    }


sess = requests.Session()


def buildSearchContent(song: String = '', page=1, page_per_num=100):
    return {
        "comm": {
            "ct": "19",
            "cv": "1845"
        },
        "music.search.SearchCgiService": {
            "method": "DoSearchForQQMusicDesktop",
            "module": "music.search.SearchCgiService",
            "param": {
                "query": song,
                "num_per_page": page_per_num,
                "page_num": page
            }
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


def _main():
    print("==== welcome to QQMusic digit High Quality Music download center ====")

    mkey, qq = decryptAndSetCookie(
        "1AxPKhgzRbWbIt8TfqfajraPgxZWmMhAoSh9HlWlPhFHQyVedFYNSOsPofZ/vj|J2XTtzdDIAqupT1T5tYMrN/u/qniED56dcBaUZSgXG2lN10Nc1OZIN87TsxcLwZQ1/TolMZ7f+oNiqQMPHs1Ff/Q==%aa2Ef93/cpOC3DyRvsNohA==")

    uid = "822a3b85-a5c9-438e-a277-a8da412e8265"
    systemVersion = "1.7.2"
    versionCode = "76"
    deviceBrand = "360"
    deviceModel = "QK1707-A01"
    appVersion = "7.1.2"
    encIP = encryptText(
        f'{uid}{deviceModel}{deviceBrand}{systemVersion}{appVersion}{versionCode}', "F*ckYou!")

    (list, meta) = searchMusic("最伟大的作品", 3)

    print()


_main()
