#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - es.py
#  @修改时间    : 2023-03-04 10:48:39
#  @上次修改    : 2023/3/4 上午10:48
from src.Api.Netease import Netease
from web.App import app

netes = Netease()


@app.get("/es/qrLogin")
def loginCode():
    qrcode = netes.qrLogin()
    return {
        'code': 200,
        'qrcode': qrcode
    }
