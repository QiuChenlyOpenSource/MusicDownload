#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - EncryptTools.py
#  @修改时间    : 2023-04-23 03:41:34
#  @上次修改    : 2023/4/23 下午3:41
import json
import random
import zlib
from hashlib import md5
from Crypto.Cipher import AES
import base64
import time as tm
import binascii

from flaskSystem.src.Common import Http


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

#

class KuwoDES():
    """
    酷我直链解析加密算法\n
    来自网友 彭狸花喵 贡献，在此感谢他的贡献。\n

    update: 秋城落叶\n
    author: 彭狸花喵(https://github.com/helloplhm-qwq)\n

    \n原作者repo:\n

    试着修了一下酷我的下载，结果自己太渣看不懂qwq\n
    就加了个算法和链接，之后的就请秋城落叶大佬做了qwq\n
    **不要在加密前数据中加br=xxx，不然是错误提示音频**\n
    不知道能用多久，先用着吧\n
    酷狗音乐的signature算法也可以提供（我是[洛雪音乐助手](https://github.com/lyswhut/lx-music-desktop)那边的贡献者 ~~虽然我是个废物~~）\n
    自行把音乐id改成对应数字\n
    原来的antiserver接口还可以用，但是不能高音质了（只有128k）\n
    请使用KuwoDES.base64_encrypt函数加密然后这么拼url\n
    http://mobi.kuwo.cn/mobi.s?f=kuwo&q=加密后数据\n

    请求User-Agent是`okhttp/3.10.0`\n

    示例：<http://mobi.kuwo.cn/mobi.s?f=kuwo&q=QTTCEVWADWjGHNKyqOt6peSJECe9IlwYOThEXM42tOPVu6boc62uWnhTsSmlQDn46NvDv+yKU0JVRFu8k+uReJLGA0BF5mBYu2iIKCWTWoSRAcRvUqhAdgBiZRX9VKg7RH9HNl+ysrqQlCTCcM05ysIhldsvO4SwlU0Im684N1508N6jXVwtmzIoSAi5h4W0lMKrFJSszAeaeLsQXvNM0N5lI1uC+zXyUG8H47dJM4tcRqylCr2KtSq+DAXJMu+eyGNf4jh2vGLM2lyEIDdPOJWgXw4N1n7LCg5NQkddT43YfZXoDcpjXywy7DaUoiMfU0odyQufaPRhUoXBmcL6+g==>
    上面的返回：\n
    ```
    format=mp3
    bitrate=1
    url=http://ar.player.ra05.sycdn.kuwo.cn/2b9c3159b8e9d681d9b0db67870a4a14/64435f6e/resource/n2/320/74/46/2352675463.mp3?bitrate$1&format$mp3&source$kwplayer_ar_9.3.1.3_qq.apk&type$convert_url2&user$0
    sig=9625213586057656967
    rid=260839262
    type=1
    ```\n
    示例返回（320k）\n
    ```
    format=mp3
    bitrate=320
    url=http://nx01.sycdn.kuwo.cn/a1a1c32ae1bd9fdcbf873f4a0270cfa1/64435bd1/resource/n1/66/9/1107056446.mp3?bitrate$320&format$mp3&type$convert_url2
    sig=4754771234559730982
    rid=51513854
    type=0
    ```\n
    加密前数据（320k）：\n
    ```
    user=0&android_id=0&prod=kwplayer_ar_9.3.1.3&corp=kuwo&newver=3&vipver=9.3.1.3&source=kwplayer_ar_9.3.1.3_qq.apk&p2p=1&notrace=0&type=convert_url2&format=flac|mp3|aac&sig=0&rid=音乐id&priority=bitrate&loginUid=0&network=WIFI&loginSid=0&mode=download
    ```
    示例返回（flac）\n
    ```
    format=flac
    bitrate=1
    url=http://other.player.rc03.sycdn.kuwo.cn/4394f83b5051e5a24693fe836613d5c3/64435da2/resource/s2/85/49/1592794249.flac?bitrate$1&format$flac&type$convert_url2
    sig=6840999210798105689
    rid=260839262
    type=1
    ```
    加密前数据（flac）：\n
    ```
    corp=kuwo&p2p=1&type=convert_url2&format=flac&rid=音乐id
    ```
    示例返回（128k）：\n
    ```
    format=mp3
    bitrate=1
    url=http://ew.sycdn.kuwo.cn/d4cdcf1a811814d166d7d126d646ac99/6443611a/resource/n1/38/24/1285019596.mp3?bitrate$1&format$mp3&type$convert_url2
    sig=5519117143462714854
    rid=260839262
    type=1
    ```
    加密前数据（128k）：\n
    ```
    corp=kuwo&p2p=1&type=convert_url2&format=mp3|aac&rid=音乐id
    ```
    """
    DES_MODE_DECRYPT = 1

    arrayE = [
        31, 0, DES_MODE_DECRYPT, 2, 3, 4, -1, -1, 3, 4, 5, 6, 7, 8, -1, -1, 7, 8, 9, 10, 11, 12, -1, -1, 11, 12, 13, 14,
        15, 16, -1, -1, 15, 16, 17, 18, 19, 20, -1, -1, 19, 20, 21, 22, 23, 24, -1, -1, 23, 24, 25, 26, 27, 28, -1, -1,
        27, 28, 29, 30, 31, 30, -1, -1
    ]

    arrayIP = [
        57, 49, 41, 33, 25, 17, 9, DES_MODE_DECRYPT, 59, 51, 43, 35, 27, 19, 11, 3, 61, 53, 45, 37, 29, 21, 13, 5, 63,
        55, 47, 39, 31, 23, 15, 7, 56, 48, 40, 32, 24, 16, 8, 0, 58, 50, 42, 34, 26, 18, 10, 2, 60, 52, 44, 36, 28, 20,
        12, 4, 62, 54, 46, 38, 30, 22, 14, 6
    ]

    arrayIP_1 = [
        39, 7, 47, 15, 55, 23, 63, 31, 38, 6, 46, 14, 54, 22, 62, 30, 37, 5, 45, 13, 53, 21, 61, 29, 36, 4, 44, 12, 52,
        20, 60, 28, 35, 3, 43, 11, 51, 19, 59, 27, 34, 2, 42, 10, 50, 18, 58, 26, 33, DES_MODE_DECRYPT, 41, 9, 49, 17,
        57, 25, 32, 0, 40, 8, 48, 16, 56, 24
    ]
    arrayLs = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]
    arrayLsMask = [0, 0x100001, 0x300003]
    arrayMask = [2 ** i for i in range(64)]
    arrayMask[-1] *= -1
    arrayP = [
        15, 6, 19, 20, 28, 11, 27, 16,
        0, 14, 22, 25, 4, 17, 30, 9,
        1, 7, 23, 13, 31, 26, 2, 8,
        18, 12, 29, 5, 21, 10, 3, 24,
    ]
    arrayPC_1 = [
        56, 48, 40, 32, 24, 16, 8, 0,
        57, 49, 41, 33, 25, 17, 9, 1,
        58, 50, 42, 34, 26, 18, 10, 2,
        59, 51, 43, 35, 62, 54, 46, 38,
        30, 22, 14, 6, 61, 53, 45, 37,
        29, 21, 13, 5, 60, 52, 44, 36,
        28, 20, 12, 4, 27, 19, 11, 3,
    ]
    arrayPC_2 = [
        13, 16, 10, 23, 0, 4, -1, -1,
        2, 27, 14, 5, 20, 9, -1, -1,
        22, 18, 11, 3, 25, 7, -1, -1,
        15, 6, 26, 19, 12, 1, -1, -1,
        40, 51, 30, 36, 46, 54, -1, -1,
        29, 39, 50, 44, 32, 47, -1, -1,
        43, 48, 38, 55, 33, 52, -1, -1,
        45, 41, 49, 35, 28, 31, -1, -1,
    ]
    matrixNSBox = [[
        14, 4, 3, 15, 2, 13, 5, 3,
        13, 14, 6, 9, 11, 2, 0, 5,
        4, 1, 10, 12, 15, 6, 9, 10,
        1, 8, 12, 7, 8, 11, 7, 0,
        0, 15, 10, 5, 14, 4, 9, 10,
        7, 8, 12, 3, 13, 1, 3, 6,
        15, 12, 6, 11, 2, 9, 5, 0,
        4, 2, 11, 14, 1, 7, 8, 13, ], [
        15, 0, 9, 5, 6, 10, 12, 9,
        8, 7, 2, 12, 3, 13, 5, 2,
        1, 14, 7, 8, 11, 4, 0, 3,
        14, 11, 13, 6, 4, 1, 10, 15,
        3, 13, 12, 11, 15, 3, 6, 0,
        4, 10, 1, 7, 8, 4, 11, 14,
        13, 8, 0, 6, 2, 15, 9, 5,
        7, 1, 10, 12, 14, 2, 5, 9, ], [
        10, 13, 1, 11, 6, 8, 11, 5,
        9, 4, 12, 2, 15, 3, 2, 14,
        0, 6, 13, 1, 3, 15, 4, 10,
        14, 9, 7, 12, 5, 0, 8, 7,
        13, 1, 2, 4, 3, 6, 12, 11,
        0, 13, 5, 14, 6, 8, 15, 2,
        7, 10, 8, 15, 4, 9, 11, 5,
        9, 0, 14, 3, 10, 7, 1, 12, ], [
        7, 10, 1, 15, 0, 12, 11, 5,
        14, 9, 8, 3, 9, 7, 4, 8,
        13, 6, 2, 1, 6, 11, 12, 2,
        3, 0, 5, 14, 10, 13, 15, 4,
        13, 3, 4, 9, 6, 10, 1, 12,
        11, 0, 2, 5, 0, 13, 14, 2,
        8, 15, 7, 4, 15, 1, 10, 7,
        5, 6, 12, 11, 3, 8, 9, 14, ], [
        2, 4, 8, 15, 7, 10, 13, 6,
        4, 1, 3, 12, 11, 7, 14, 0,
        12, 2, 5, 9, 10, 13, 0, 3,
        1, 11, 15, 5, 6, 8, 9, 14,
        14, 11, 5, 6, 4, 1, 3, 10,
        2, 12, 15, 0, 13, 2, 8, 5,
        11, 8, 0, 15, 7, 14, 9, 4,
        12, 7, 10, 9, 1, 13, 6, 3, ], [
        12, 9, 0, 7, 9, 2, 14, 1,
        10, 15, 3, 4, 6, 12, 5, 11,
        1, 14, 13, 0, 2, 8, 7, 13,
        15, 5, 4, 10, 8, 3, 11, 6,
        10, 4, 6, 11, 7, 9, 0, 6,
        4, 2, 13, 1, 9, 15, 3, 8,
        15, 3, 1, 14, 12, 5, 11, 0,
        2, 12, 14, 7, 5, 10, 8, 13, ], [
        4, 1, 3, 10, 15, 12, 5, 0,
        2, 11, 9, 6, 8, 7, 6, 9,
        11, 4, 12, 15, 0, 3, 10, 5,
        14, 13, 7, 8, 13, 14, 1, 2,
        13, 6, 14, 9, 4, 1, 2, 14,
        11, 13, 5, 0, 1, 10, 8, 3,
        0, 11, 3, 5, 9, 4, 15, 2,
        7, 8, 12, 15, 10, 7, 6, 12, ], [
        13, 7, 10, 0, 6, 9, 5, 15,
        8, 4, 3, 10, 11, 14, 12, 5,
        2, 11, 9, 6, 15, 12, 0, 3,
        4, 1, 14, 13, 1, 2, 7, 8,
        1, 2, 12, 15, 10, 4, 0, 3,
        13, 14, 6, 9, 7, 8, 9, 6,
        15, 1, 5, 12, 3, 10, 14, 5,
        8, 7, 11, 0, 4, 13, 2, 11, ],
    ]

    SECRET_KEY = b'ylzsxkwm'

    def bit_transform(self, arr_int, n, l):
        l2 = 0
        for i in range(n):
            if arr_int[i] < 0 or (l & self.arrayMask[arr_int[i]] == 0):
                continue
            l2 |= self.arrayMask[i]
        return l2

    def DES64(self, longs, l):
        out = 0
        SOut = 0
        pR = [0] * 8
        pSource = [0, 0]
        sbi = 0
        t = 0
        L = 0
        R = 0
        out = self.bit_transform(self.arrayIP, 64, l)
        pSource[0] = 0xFFFFFFFF & out
        pSource[1] = (-4294967296 & out) >> 32
        for i in range(16):
            R = pSource[1]
            R = self.bit_transform(self.arrayE, 64, R)
            R ^= longs[i]
            for j in range(8):
                pR[j] = 255 & R >> j * 8
            SOut = 0
            for sbi in range(7, -1, -1):
                SOut <<= 4
                SOut |= self.matrixNSBox[sbi][pR[sbi]]

            R = self.bit_transform(self.arrayP, 32, SOut)
            L = pSource[0]
            pSource[0] = pSource[1]
            pSource[1] = L ^ R
        pSource = pSource[::-1]
        out = -4294967296 & pSource[1] << 32 | 0xFFFFFFFF & pSource[0]
        out = self.bit_transform(self.arrayIP_1, 64, out)
        return out

    def sub_keys(self, l, longs, n):
        l2 = self.bit_transform(self.arrayPC_1, 56, l)
        for i in range(16):
            l2 = ((l2 & self.arrayLsMask[self.arrayLs[i]]) << 28 -
                  self.arrayLs[i] | (l2 & ~self.arrayLsMask[self.arrayLs[i]]) >> self.arrayLs[i])
            longs[i] = self.bit_transform(self.arrayPC_2, 64, l2)
        j = 0
        while n == 1 and j < 8:
            l3 = longs[j]
            longs[j], longs[15 - j] = longs[15 - j], longs[j]
            j += 1

    def encrypt(self, msg, key=SECRET_KEY):
        if isinstance(msg, str):
            msg = msg.encode()
        if isinstance(key, str):
            key = key.encode()
        assert (isinstance(msg, bytes))
        assert (isinstance(key, bytes))

        # 处理密钥块
        l = 0
        for i in range(8):
            l = l | key[i] << i * 8

        j = len(msg) // 8
        # arrLong1 存放的是转换后的密钥块, 在解密时只需要把这个密钥块反转就行了
        arrLong1 = [0] * 16
        self.sub_keys(l, arrLong1, 0)
        # arrLong2 存放的是前部分的明文
        arrLong2 = [0] * j
        for m in range(j):
            for n in range(8):
                arrLong2[m] |= msg[n + m * 8] << n * 8

        # 用于存放密文
        arrLong3 = [0] * ((1 + 8 * (j + 1)) // 8)
        # 计算前部的数据块(除了最后一部分)
        for i1 in range(j):
            arrLong3[i1] = self.DES64(arrLong1, arrLong2[i1])

        # 保存多出来的字节
        arrByte1 = msg[j * 8:]
        l2 = 0
        for i1 in range(len(msg) % 8):
            l2 |= arrByte1[i1] << i1 * 8
        # 计算多出的那一位(最后一位)
        arrLong3[j] = self.DES64(arrLong1, l2)

        # 将密文转为字节型
        arrByte2 = [0] * (8 * len(arrLong3))
        i4 = 0
        for l3 in arrLong3:
            for i6 in range(8):
                arrByte2[i4] = (255 & l3 >> i6 * 8)
                i4 += 1
        return arrByte2

    def base64_encrypt(self, msg):
        b1 = self.encrypt(msg)
        b2 = bytearray(b1)
        s = base64.encodebytes(b2)
        return s.replace(b'\n', b'').decode()


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
    osVersion = '13' #从sdkVersion修改为androidVersion
    time = str(int(tm.time()))
    # f389249d91bd845c9b817db984054cfb 1678713735 6562653262383463363633646364306534333663
    # lowerCase = hashMd5("6d849adb2f3e00d413fe48efbb18d9bb" + time + "6562653262383463363633646364306534333668").lower() # 更新参数
    lowerCase = hashMd5("d86b856be4a7ea7a5bc9b6c4eed46f4e" + time + "6562653262383463363633646364306534333668").lower() # app的MD5改变了

    s6 = "{\\\"method\\\":\\\"GetMusicUrl\\\",\\\"platform\\\":\\\"" + platform + "\\\",\\\"t1\\\":\\\"" + t1_MusicID + "\\\",\\\"t2\\\":\\\"" + t2 + "\\\"}"
    s7 = "{\\\"uid\\\":\\\"\\\",\\\"token\\\":\\\"\\\",\\\"deviceid\\\":\\\"84ac82836212e869dbeea73f09ebe52b\\\",\\\"appVersion\\\":\\\"4.1.4\\\",\\\"vercode\\\":\\\"4140\\\",\\\"device\\\":\\\"" + device + "\\\",\\\"osVersion\\\":\\\"" + osVersion + "\\\"}" # 更新app版本
    s8 = "{\n\t\"text_1\":\t\"" + s6 + "\",\n\t\"text_2\":\t\"" + s7 + "\",\n\t\"sign_1\":\t\"" + lowerCase + "\",\n\t\"time\":\t\"" + time + "\",\n\t\"sign_2\":\t\"" + hashMd5(
        s6.replace("\\", "") + s7.replace("\\", "") + lowerCase + time + "NDRjZGIzNzliNzEe").lower() + "\"\n}" # 更新param

    # 资源大师接口
    # s5 = hashMd5(
    #     "2c6d031981d1b6920fefd537043fd6eb" + time + "6562653262383463363633646364306534333663").lower()
    # s6 = "{\\\"method\\\":\\\"GetMusicUrl\\\",\\\"platform\\\":\\\"" + platform + "\\\",\\\"t1\\\":\\\"" + t1_MusicID + "\\\",\\\"t2\\\":\\\"" + t2 + "\\\"}"
    # s7 = "{\\\"uid\\\":\\\"\\\",\\\"token\\\":\\\"\\\",\\\"deviceid\\\":\\\"84c599d711066ef740eb49109dac9782\\\",\\\"appVersion\\\":\\\"4.0.9.V1\\\",\\\"vercode\\\":\\\"4090\\\",\\\"device\\\":\\\"" + device + "\\\",\\\"osVersion\\\":\\\"" + osVersion + "\\\"}"
    # s8 = "{\n\t\"text_1\":\t\"" + s6 + "\",\n\t\"text_2\":\t\"" + s7 + "\",\n\t\"sign_1\":\t\"" + s5 + "\",\n\t\"time\":\t\"" + time + "\",\n\t\"sign_2\":\t\"" + hashMd5(
    #     s6.replace("\\", "") + s7.replace("\\", "") + s5 + time + "NDRjZGIzNzliNzEx").lower() + "\"\n}"
    # 资源大师接口结束

    # 移除AES加密，只需要一遍hex
    s8 = binascii.hexlify(s8.encode('utf-8')).decode('utf-8').upper().encode('utf-8')
    s8 = zlib.compress(s8)
    url = [
        "http://app.kzti.top/client/cgi-bin/api.fcg", # 源app更新地址
        "http://gcsp.kzti.top:1030/client/cgi-bin/api.fcg", # 源app已更新地址
        "http://119.91.134.171:1030/client/cgi-bin/api.fcg",
        "http://106.52.68.150:1030/client/cgi-bin/api.fcg"  # 资源大师接口
    ]
    url = url[0]
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
