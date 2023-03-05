#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - EncryptTools.py
#  @修改时间    : 2023-03-05 10:56:10
#  @上次修改    : 2023/3/5 下午10:56
import json
import random
import zlib
from hashlib import md5
from Crypto.Cipher import AES
import base64
import time as tm

from src.Common import Http


# des解密


def decryptDES(strs: str, key: str): return des(
    key, CBC, key, padmode=PAD_PKCS5).decrypt(base64.b64decode(str(strs)))


# des加密
def encryptDES(text: str, key: str): return str(base64.b64encode(
    des(key, CBC, key, padmode=PAD_PKCS5).encrypt(text)), 'utf-8')


# 加密字符串
def encryptText(text: str, qq: str):
    key = (qq)[0:8]
    return encryptDES(text, key)


# 解密字符串
def decryptText(text: str, qq: str): return str(decryptDES(
    text.replace("-", ""), (qq)[0:8]), 'utf-8')


def AESEncrypt(data: str, key: str):
    password = key.encode("utf-8")  # 秘钥，b就是表示为bytes类型
    aes = AES.new(password, AES.MODE_ECB)  # 创建一个aes对象
    # AES.MODE_ECB 表示模式是ECB模式
    text = pad(AES.block_size, data)
    text = text.encode("utf-8")  # 需要加密的内容，bytes类型
    en_text = aes.encrypt(text)  # 加密明文
    return en_text


def pad(length, text):
    """
    填充函数，使被加密数据的字节码长度是block_size的整数倍
    """
    return text + (length - len(text) % length) * chr(length - len(text) % length)


# def AESDecrypt(data: bytes, key: str):
#     password = key.encode("utf-8")  # 秘钥，b就是表示为bytes类型
#     aes = AES.new(password, AES.MODE_ECB)  # 创建一个aes对象
#     # AES.MODE_ECB 表示模式是ECB模式
#     data = unpad(data)
#     en_text = aes.decrypt(data)
#     en_text = en_text.decode()
#     print("密文：", en_text)  # 加密明文，bytes类型
#     return en_text


hexs = [a for a in "0123456789abcdef"]


def hex2Str(hx: str):
    a = hx.lower()
    length = int(len(a) / 2)
    bt = bytearray()
    for i in range(0, length - 1):
        i2 = i * 2
        b = int(a[i2:i2 + 2], 16) & 255
        bt.append(b)
    return bytes(bt)


def byte2hex(bt: bytes):
    strs = ""
    for i in bt:
        s = hex(i)[2:].upper()
        if len(s) > 3:
            strs += s[6:]
        elif len(s) < 2:
            strs += '0' + s
        else:
            strs += s
    return strs


def hashMd5(s: str):
    return md5(s.encode("utf-8")).hexdigest()


mHttp = Http.HttpRequest()


def testGetLink(qqmusicID='003cI52o4daJJL', platform='qq', quality='sq'):
    t1_MusicID = qqmusicID
    platform = platform
    t2 = quality
    device = 'MI 14 Pro Max'
    osVersion = '27'
    time = str(int(tm.time()))
    lowerCase = hashMd5("f389249d91bd845c9b817db984054cfb" + time + "6562653262383463363633646364306534333663").lower()

    s6 = "{\\\"method\\\":\\\"GetMusicUrl\\\",\\\"platform\\\":\\\"" + platform + "\\\",\\\"t1\\\":\\\"" + t1_MusicID + "\\\",\\\"t2\\\":\\\"" + t2 + "\\\"}"
    s7 = "{\\\"uid\\\":\\\"\\\",\\\"token\\\":\\\"\\\",\\\"deviceid\\\":\\\"84c599d711066ef740eb49109dac9782\\\",\\\"appVersion\\\":\\\"4.1.0.V4\\\",\\\"vercode\\\":\\\"4100\\\",\\\"device\\\":\\\"" + device + "\\\",\\\"osVersion\\\":\\\"" + osVersion + "\\\"}"
    s8 = "{\n\t\"text_1\":\t\"" + s6 + "\",\n\t\"text_2\":\t\"" + s7 + "\",\n\t\"sign_1\":\t\"" + lowerCase + "\",\n\t\"time\":\t\"" + time + "\",\n\t\"sign_2\":\t\"" + hashMd5(
        s6.replace("\\", "") + s7.replace("\\", "") + lowerCase + time + "NDRjZGIzNzliNzEx").lower() + "\"\n}"

    s8 = AESEncrypt(s8, "6480fedae539deb2")
    s8 = byte2hex(s8)
    s8 = byte2hex(s8.encode("utf-8")).encode("utf-8")
    s8 = zlib.compress(s8)
    url = "http://app.kzti.top:1030/client/cgi-bin/api.fcg", "http://119.91.134.171:1030/client/cgi-bin/api.fcg"
    url = url[1]
    res = mHttp.getHttp(url, 1, s8)
    try:
        res = zlib.decompress(res.content).decode("utf-8")
    except:
        print("下载失败，无法获取原始文件链接。")
        return "下载失败，无法获取原始文件链接。"
    res = json.loads(res)
    if res['code'] == '403':
        print("下载失败，解析服务器返回403错误代码。")
        return "下载失败，解析服务器返回403错误代码。"
    # print(res['data'])
    return res['data']


# testGetLink()


def testUnzip():
    file = '/Users/qiuchenly/Downloads/response'
    # file = '/Users/qiuchenly/Downloads/request'
    with open(file, 'rb+') as p:
        bt: bytes = p.read()
        bt = zlib.decompress(bt)
        res = bt.decode("utf-8")

    # mode = 1
    # if mode is 1:
    # code = hex2Str(hex2Str(res).decode("utf-8"))
    # code = AESUtils.AESUtil().decrypt(code, "6480fedae539deb2")
    print(res)

# testUnzip()
