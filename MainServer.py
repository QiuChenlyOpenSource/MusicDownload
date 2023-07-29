#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - MainServer.py
#  @修改时间    : 2023-03-13 11:07:40
#  @上次修改    : 2023/3/13 下午11:07

# 由于Python解释性语言特性，必须要严格按照加载顺序

import argparse

parser = argparse.ArgumentParser(description="QQFlacMusicDownloader.")
parser.add_argument("--port", default=8899, type=int)
args = parser.parse_args()

from flaskSystem.App import Start  # 必须先加载他 这是初始化flask框架代码
from flaskSystem.API.es import init as es  # 下面无需顺序
from flaskSystem.API.kw import init as kw  # 下面无需顺序
from flaskSystem.API.qq import init as qq  # es qq模块不分顺序
from flaskSystem.API.files import init as files  # es qq模块不分顺序

es()  # 加载API接口
qq()
kw()
files() # 加载文件管理接口

Start(args.port)  # 最后启动总函数
