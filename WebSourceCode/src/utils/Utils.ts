/*
 * # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
 * # @作者         : 秋城落叶(QiuChenly)
 * # @邮件         : qiuchenly@outlook.com
 * # @文件         : 项目 [WebSourceCode] - Utils.ts
 * # @修改时间    : 2023-03-05 06:13:16
 * # @上次修改    : 2023/3/5 下午6:13
 */

export function timestampToTime(timestamp: number) {
  let date = new Date(timestamp); //时间戳为10位需*1000，时间戳为13位的话不需乘1000
  let Y = date.getFullYear() + "-";
  let M =
    (date.getMonth() + 1 < 10
      ? "0" + (date.getMonth() + 1)
      : date.getMonth() + 1) + "-";
  let D = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()) + " ";
  let h =
    (date.getHours() < 10 ? "0" + date.getHours() : date.getHours()) + ":";
  let m =
    (date.getMinutes() < 10 ? "0" + date.getMinutes() : date.getMinutes()) +
    ":";
  let s = date.getSeconds() < 10 ? "0" + date.getSeconds() : date.getSeconds();
  return Y + M + D + h + m + s;
}

/**
 * 判断类型是否属于某一种
 * @param props
 */
export const isType = <T>(props: any): props is T =>
  //@ts-ignore
  typeof (props as T)["js"] !== "undefined";

export const platformList = [
  {
    name: "QQ音乐",
    value: "qq",
  },
  {
    name: "网易云音乐",
    value: "wyy",
  },
  {
    name: "酷我音乐",
    value: "kw",
  },
  {
    name: "咪咕音乐",
    value: "mg",
  },
  {
    name: "MyFreeMP3",
    value: "myfreemp3",
  },
];

export const platformListv2: any = {
  "qq": "QQ音乐",
  "wyy": "网易云音乐",
  "kw": "酷我音乐",
  "mg": "咪咕音乐",
  "myfreemp3": "MyFreeMP3"
}

export const MetaInfomationSupport: any = {
  "iTunes": "Apple Music",
  "QQMusic": "QQ音乐"
}

export const MetaInfomationSupportTypes: any = {
  "albumName": "专辑名称",
  "songer": "歌手名称",
  "title": "歌曲名称"
}

export const MetaInfomationSupportOptions: any = {
  "reflect": {
    name: "看作",
    lint: "如果是"
  },
  "replace": {
    name: "替换",
    lint: "将字符"
  }
}