#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - BaseApi.py
#  @修改时间    : 2023-03-13 11:07:40
#  @上次修改    : 2023/3/13 下午11:07
import abc

from flaskSystem.src.Types.Types import Songs


class BaseApi(abc.ABC):
    @abc.abstractmethod
    def search(self, searchKey: str) -> list[Songs]:
        """
        搜索歌曲并获取统一列表
        Args:
            searchKey: 搜索字符串

        Returns:
            返回 `SearchResult` 类型的列表数据
        """
