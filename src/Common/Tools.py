#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : 1925374620@qq.com
#  @文件         : 项目 [qqmusic] - Tools.py
#  @修改时间    : 2023-03-02 05:00:36
#  @上次修改    : 2023/3/2 下午5:00
from src.Common import Http


def subString(text: str, left: str, right: str):
    """
    取文本中间
    Args:
        text: 完整文本
        left: 左边文本
        right: 右边文本

    Returns:
        返回中间的文本

    """
    leftInx = text.find(left)
    leftInx += len(left)
    rightInx = text.find(right, leftInx)
    txt = text[leftInx:rightInx]
    return txt


QQHttpServer = Http.HttpRequest()
