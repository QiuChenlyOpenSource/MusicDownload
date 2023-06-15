/*
 * # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
 * # @作者         : 秋城落叶(QiuChenly)
 * # @邮件         : qiuchenly@outlook.com
 * # @文件         : 项目 [WebSourceCode] - UserInfoDetail.ts
 * # @修改时间    : 2023-03-05 03:46:32
 * # @上次修改    : 2023/3/5 下午3:46
 */

export interface NetEaseUserInfo {
  account: Account;
  code: number;
  profile: Profile;
}

export interface Account {
  anonimousUser: boolean;
  ban: number;
  baoyueVersion: number;
  createTime: number;
  donateVersion: number;
  id: number;
  paidFee: boolean;
  status: number;
  tokenVersion: number;
  type: number;
  userName: string;
  vipType: number;
  whitelistAuthority: number;
}

export interface Profile {
  accountStatus: number;
  accountType: number;
  anchor: boolean;
  authStatus: number;
  authenticated: boolean;
  authenticationTypes: number;
  authority: number;
  avatarDetail: any;
  avatarImgId: number;
  avatarUrl: string;
  backgroundImgId: number;
  backgroundUrl: string;
  birthday: number;
  city: number;
  createTime: number;
  defaultAvatar: boolean;
  description: any;
  detailDescription: any;
  djStatus: number;
  expertTags: any;
  experts: any;
  followed: boolean;
  gender: number;
  lastLoginIP: string;
  lastLoginTime: number;
  locationStatus: number;
  mutual: boolean;
  nickname: string;
  province: number;
  remarkName: any;
  shortUserName: string;
  signature: any;
  userId: number;
  userName: string;
  userType: number;
  vipType: number;
  viptypeVersion: number;
}
