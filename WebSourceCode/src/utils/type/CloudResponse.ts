/*
 * # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
 * # @作者         : 秋城落叶(QiuChenly)
 * # @邮件         : qiuchenly@outlook.com
 * # @文件         : 项目 [qqmusic] - CloudResponse.ts
 * # @修改时间    : 2023-03-14 08:35:43
 * # @上次修改    : 2023/3/14 下午8:35
 */

export interface CloudResponse {
  count: number;
  hasMore: boolean;
  list: List[];
}

export interface List {
  addTime: number;
  album: string;
  artist: string;
  bitrate: number;
  cover: number;
  coverId: string;
  fileName: string;
  fileSize: number;
  lyricId: string;
  simpleSong: SimpleSong;
  songId: number;
  songName: string;
  version: number;
}

export interface SimpleSong {
  a: any;
  al: Al;
  alia: string[];
  ar: Ar[];
  cd?: string;
  cf?: string;
  copyright: number;
  cp: number;
  crbt?: string;
  djId: number;
  dt: number;
  fee: number;
  ftype: number;
  h?: H;
  id: number;
  l?: L;
  m?: M;
  mark: number;
  mst: number;
  mv: number;
  name: string;
  no: number;
  noCopyrightRcmd?: NoCopyrightRcmd;
  originCoverType: number;
  originSongSimpleData?: OriginSongSimpleData;
  pop: number;
  privilege: Privilege;
  pst: number;
  publishTime: number;
  rt?: string;
  rtUrl: any;
  rtUrls: any[];
  rtype: number;
  rurl: any;
  s_id: number;
  single: number;
  st: number;
  t: number;
  v: number;
  tns?: string[];
}

export interface Al {
  id: number;
  name?: string;
  pic: number;
  picUrl: string;
  pic_str?: string;
  tns: string[];
}

export interface Ar {
  alias: any[];
  id: number;
  name?: string;
  tns: any[];
}

export interface H {
  br: number;
  fid: number;
  size: number;
  vd: number;
}

export interface L {
  br: number;
  fid: number;
  size: number;
  vd: number;
}

export interface M {
  br: number;
  fid: number;
  size: number;
  vd: number;
}

export interface NoCopyrightRcmd {
  songId?: string;
  type: number;
  typeDesc: string;
}

export interface OriginSongSimpleData {
  albumMeta: AlbumMeta;
  artists: Artist[];
  name: string;
  songId: number;
}

export interface AlbumMeta {
  id: number;
  name: string;
}

export interface Artist {
  id: number;
  name: string;
}

export interface Privilege {
  chargeInfoList?: ChargeInfoList[];
  cp: number;
  cs: boolean;
  dl: number;
  dlLevel: string;
  downloadMaxBrLevel: string;
  downloadMaxbr: number;
  fee: number;
  fl: number;
  flLevel: string;
  flag: number;
  freeTrialPrivilege: FreeTrialPrivilege;
  id: number;
  maxBrLevel: string;
  maxbr: number;
  payed: number;
  pl: number;
  plLevel: string;
  playMaxBrLevel: string;
  playMaxbr: number;
  preSell: boolean;
  rscl: any;
  sp: number;
  st: number;
  subp: number;
  toast: boolean;
}

export interface ChargeInfoList {
  chargeMessage: any;
  chargeType: number;
  chargeUrl: any;
  rate: number;
}

export interface FreeTrialPrivilege {
  listenType: any;
  resConsumable: boolean;
  userConsumable: boolean;
}
