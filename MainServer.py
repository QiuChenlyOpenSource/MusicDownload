#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - MainServer.py
#  @修改时间    : 2023-03-05 01:44:30
#  @上次修改    : 2023/3/5 下午1:44
from web.API.es import init as es
from web.API.qq import init as qq
from web.App import Start

es()
qq()

Start()
