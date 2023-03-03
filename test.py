#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - test.py
#  @修改时间    : 2023-03-02 11:43:24
#  @上次修改    : 2023/3/2 上午11:43
import requests

from src.Api.Kuwo import KwApi
from src.Api.Netease import Netease
from src.Common.Tools import subString
from src.Types.Types import Songs

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

ease = Netease()
qrCode = ease.qrLogin()
