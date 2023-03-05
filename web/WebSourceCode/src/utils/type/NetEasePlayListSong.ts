/*
 * # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
 * # @作者         : 秋城落叶(QiuChenly)
 * # @邮件         : 1925374620@qq.com
 * # @文件         : 项目 [WebSourceCode] - NetEasePlayListSong.ts
 * # @修改时间    : 2023-03-05 05:33:39
 * # @上次修改    : 2023/3/5 下午5:33
 */

export interface NeteasePlayListSongs {
    code: number
    list: NeteasePlayListSongsList[]
}

export interface NeteasePlayListSongsList {
    album: Album
    author: Author[]
    author_simple: string
    id: number
    name: string
    publishTime: number
}

export interface Album {
    id: number
    name: string
    pic: number
    picUrl: string
    pic_str?: string
    tns: string[]
}

export interface Author {
    alias: any[]
    id: number
    name: string
    tns: any[]
}
