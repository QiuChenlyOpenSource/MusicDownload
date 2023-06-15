#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - Types.py
#  @修改时间    : 2023-03-05 09:43:21
#  @上次修改    : 2023/3/5 下午9:43

class Songs(object):
    def __init__(self,
                 album: str,
                 artist: str,
                 musicrid: str,
                 releaseDate: str,
                 albumid: int,
                 songTimeMinutes: str,
                 pic120: str,
                 albumpic: str,
                 name: str,
                 rid: int,
                 *args,
                 **kwargs) -> None:
        """

        Args:
            album: 专辑
            artist: 艺术家，歌手
            musicrid: 音乐id
            releaseDate: 发布时间
            albumid: 专辑ID
            songTimeMinutes: 歌曲时间
            pic120: 音乐图片
            albumpic: 专辑图片
            name: 歌曲名称
            rid: 歌曲实际数字id
            *args:
            **kwargs:
        """
        self.rid = rid
        self.name = name
        self.pic120 = pic120
        self.songTimeMinutes = songTimeMinutes
        self.albumid = albumid
        self.albumpic = albumpic
        self.releaseDate = releaseDate
        self.album = album
        self.artist = artist
        self.musicrid = musicrid

    # @property
    # def title(self):
    #     return self._album
