#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - test.py
#  @修改时间    : 2023-03-06 06:02:23
#  @上次修改    : 2023/3/6 下午6:02
import time
import uuid
from concurrent.futures import Future
from uuid import UUID

import requests
from flask import Flask

# from src.Api.Kuwo import KwApi
# from src.Api.Netease import Netease
# from src.Common import Concurrency
from src.Common.Concurrency import Downloader


# from src.Common.Tools import subString
# from src.Types.Types import Songs


# s = Songs("哈咯")
# s.title = "asd"
# print(s.title)

# subString("kw_token=123123;", "kw_token=", ";")

# kw = KwApi()
# res = kw.search("周杰伦")
# res = kw.getDownloadUrl(res[0].rid)
# res = requests.get(res)
# with open("test.mp3", 'wb+') as w:
#     w.write(res.content)
#     w.flush()
# 只能下载MP3格式 很遗憾

# ease = Netease()
# qrCode = ease.qrLogin()

def done(ret: Future):
    print(f"ret is down {ret.result()}")


def executeFn(a1: str, a2: bool):
    time.sleep(4)
    return a1 + "a2 True" if a2 else "a2 False"


app: Flask = Flask(__name__)

c = Downloader()
c.initPool(16)


@app.get("/")
def add():
    print("任务开始")
    c.addTask(done, executeFn, "1234", False)
    return {
        'code': 200
    }


app.run(
    '0.0.0.0',
    8899,
    debug=False
)
