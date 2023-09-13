#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - Concurrency.py
#  @修改时间    : 2023-07-28 02:05:27
#  @上次修改    : 2023/7/28 下午2:05
import os
from concurrent import futures
from concurrent.futures import ThreadPoolExecutor


class Downloader():
    def __init__(self):
        self.maxWorks = 4
        self.mConcurrentPool: ThreadPoolExecutor = None
        self.mPoolThread = []
        self.folder = ''
        self.save_lyric = False
        self.set_folder(os.getcwd() + '/music/')

    def set_folder(self, folder):
        folder = folder.replace(' ', '')
        if not folder.endswith('/'):
            folder += '/'
        self.folder = folder
        if not os.path.exists(self.folder):
            os.mkdir(self.folder)
        return self.folder

    def get_folder(self):
        return self.folder

    def initPool(self, max_works: int):
        """
        初始化线程池
        Args:
            max_works: 线程数量

        Returns:

        """
        self.maxWorks = max_works
        if self.mConcurrentPool is not None:
            self.mConcurrentPool.shutdown(False)
        # for th in concurrent.futures.as_completed(pollCache):
        #     song = th.result()
        self.mConcurrentPool = ThreadPoolExecutor(max_workers=max_works)

    def set_lyric(self, save_lyric: bool):
        """
        设置是否保存歌词
        Args:
            save_lyric: 是否保存歌词

        Returns:

        """
        self.save_lyric = save_lyric
    
    def get_lyric(self):
        return self.save_lyric

    def addTask(self, callback, fn, *args, **kwargs, ):
        t = self.mConcurrentPool.submit(fn, *args, **kwargs)
        t.add_done_callback(callback)
        self.mPoolThread.append(t)
        return True

    def getCurrentResize(self):
        return self.maxWorks
