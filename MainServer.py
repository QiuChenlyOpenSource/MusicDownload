#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - MainServer.py
#  @修改时间    : 2023-03-05 09:31:18
#  @上次修改    : 2023/3/5 下午9:31

# 由于Python解释性语言特性，必须要严格按照加载顺序

from web.App import Start  # 必须先加载他 这是初始化flask框架代码
from web.API.es import init as es  # 下面无需顺序
from web.API.kw import init as kw  # 下面无需顺序
from web.API.qq import init as qq  # es qq模块不分顺序

es()  # 加载API接口
qq()
kw()

Start()  # 最后启动总函数
