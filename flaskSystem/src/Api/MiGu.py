#  Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
#  @作者         : 秋城落叶(QiuChenly)
#  @邮件         : qiuchenly@outlook.com
#  @文件         : 项目 [qqmusic] - MiGu.py
#  @修改时间    : 2023-07-28 11:49:29
#  @上次修改    : 2023/7/28 下午11:49
from flaskSystem.src.Common import Http
from flaskSystem.src.Common.Http import HttpRequest


class MiGu():
    httpClient: HttpRequest = None

    def __init__(self):
        self.httpClient = Http.HttpRequest()

    def getUrl(self, url: str, method=0, data=None, params=None):
        res = self.httpClient.getHttp(url, method, data, {
            "Referer": "http://m.music.migu.cn/v3",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36 Edg/110.0.1587.50",
        }, params)
        return res

    def search(self, searchKey="周杰伦", pageNum=1, pageSize=100):
        url = "https://m.music.migu.cn/migu/remoting/scr_search_tag"
        querystring = {"keyword": searchKey, "pgc": f"{pageNum}", "rows": f"{pageSize}", "type": "2"}
        data = self.getUrl(url, params=querystring).json()
        lst = []
        for li in data['musics']:
            kbpsList = li['hasSQqq']
            extra = 'flac' if kbpsList == '1' else 'mp3'
            it = {
                'prefix': "prefixNone",
                'extra': extra,
                'cover': li['cover'],
                'notice': "FLAC 无损音质" if extra == 'flac' else f'{extra.upper()}',
                'mid': li['copyrightId'],
                'musicid': li['copyrightId'],
                'songmid': li['copyrightId'],
                'size': "无法计算",
                'title': li['title'],
                'singer': li['singerName'],
                'album': li['albumName'],
                'time_publish': "无",
                # 'hasLossless': li['hasLossless'],
                'readableText': f"{li['singerName']} - {li['title']}"
            }
            lst.append(it)
        return {
            'data': lst,
            'page': {
                'size': data['pgt'],
                'next': pageNum + 1,
                'cur': pageNum,
                'searchKey': searchKey
            }
        }

    def getAlbumList(self, _albumId):
        url = "https://m.music.migu.cn/migumusic/h5/album/info"

        querystring = {"albumId": _albumId}

        headers = {
            "Accept": "application/json, text/plain, */*",
            "By": "efcca141f13e5b23e0677983721f586e",
            "Referer": "https://m.music.migu.cn/v4/music/album/" + _albumId,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/115.0.0.0"
        }
        response = self.httpClient.getHttp(url, 0, b'', headers, querystring).json()
        musics = response['data']['songs']['items']
        lst = []
        for li in musics:
            kbpsList = li['sq'] != None
            extra = 'flac' if kbpsList else 'mp3'
            
            if li['bit24'] != None:
                haveBit24 = True
            if li['d3'] != None:
                have3D = True
                
            singer = [it['name'] for it in li['singers']][0]
            it = {
                'prefix': "prefixNone",
                'extra': extra,
                'cover': "https://"+response['data']['detailInfo']['largePic'],
                'notice': "FLAC 无损音质" if extra == 'flac' else f'{extra.upper()}',
                'mid': li['copyrightId'],
                'musicid': li['copyrightId'],
                'songmid': li['copyrightId'],
                'size': "无法计算",
                'title': li['name'],
                'singer': singer,
                'album': li['album']['albumName'],
                'time_publish': response['data']['detailInfo']['publishDate'],
                # 'hasLossless': li['hasLossless'],
                'readableText': f"{singer} - {li['name']}"
            }
            lst.append(it)
        return {
            'data': lst,
            'page': {
                'size': len(response['data']['songs']['items']),
                'next': 0,
                'cur': 1,
                'searchKey': ""
            }
        }

    def getDownloadLink(self, _id="0", _type="4"):
        url = "https://c.musicapp.migu.cn/MIGUM2.0/v1.0/content/resourceinfo.do"
        querystring = {"copyrightId": _id, "resourceType": "2"}
        res = self.getUrl(url, params=querystring).json()
        if res['code'] == '000000':  # 这里如果不是六个0则表示那确实废了
            if res['resource']:
                sizet = 0
                music = None
                
                # if 'z3dCode' in res['resource'][0]:
                    # res['resource'][0]['newRateFormats'].append(res['resource'][0]['z3dCode'])
                
                # 计算flac音质 原理是高品质音乐文件必然比低品质音乐文件大
                for it in res['resource'][0]['newRateFormats']:
                    if 'size' not in it:
                        it['size'] = it['androidSize']
                    size = int(it['size'])
                    if size > sizet:
                        sizet = size
                        music = it
                        
                if music is None:
                    return None

                music = {
                    **res['resource'][0],  # 元数据填充
                    **music,
                    'source_platform': "MiGu",
                    'source_platform_music_id': _id
                }
                music['albumImgs'] = [i['img'] for i in music['albumImgs']]
                music['singerImgs'] = [
                    i2['img'] for i2 in
                    [
                        i1['miguImgItems'] for i1 in
                        [
                            music['singerImg'][i] for i in music['singerImg']
                        ]
                    ][0]
                ]
                typeMap = {
                    'PQ': "128",
                    'HQ': "320",
                    'SQ': "flac",
                }
                if 'format' not in music:
                    music['format'] = music['androidFormat']
                # 无损 24bit无损 3d无损
                if music['format'] == '011002' or music['format'] == '011005' or music['format'] == '020024':  # 3D无损
                    url = music['androidUrl']
                    music['fileType'] = 'flac'
                else:  # 不是无损一律按照乐色处理
                    url = music['url']
                if url.find('/public')>-1:
                    music['url'] = "https://freetyst.nf.migu.cn/public" + url.split("/public")[1]
                elif  url.find('/mp3')>-1:
                    music['url'] = "https://freetyst.nf.migu.cn/mp3" + url.split("/mp3")[1]
                else:
                    return None
                return music
            return None
        else:
            return None
