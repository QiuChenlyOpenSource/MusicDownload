import { MediaQuery } from './../utils/type/BasicType';
/*
 * # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
 * # @作者         : 秋城落叶(QiuChenly)
 * # @邮件         : qiuchenly@outlook.com
 * # @文件         : 项目 [qqmusic] - BasicStore.ts
 * # @修改时间    : 2023-04-14 01:32:39
 * # @上次修改    : 2023/4/14 下午1:32
 */

import { defineStore } from "pinia";
import { NetEaseUserInfo } from "@/utils/type/UserInfoDetail";

export const BasicStore = defineStore("basicStore", {
  state: () => {
    return {
      firstOpen: true,
      token: "",
      searchHistory: [] as string[],
      lastSearch: "",
      filterKeys: [
        "DJ",
        "Remix",
        "即兴",
        "变调",
        "Live",
        "伴奏",
        "版,",
        "版)",
        "慢四",
        "纯音乐",
        "二胡",
        "串烧",
        "现场",
      ],
      config: {
        onlyMatchSearchKey: false,
        ignoreNoAlbumSongs: false,
        classificationMusicFile: false,
        disableFilterKey: false,
        concurrency: {
          num: 16,
          downloadFolder: "",
          saveLyric: false,
        },
        platform: "qq",
      },
      MusicMetaPrepare: [{
        platform: 'mg',
        metas: [] as MediaQuery[]
      }],
      netease: {
        isLogin: false,
        token: "",
        anonimousCookie: "",
        user: {} as NetEaseUserInfo,
      },
    };
  },
  getters: {},
  actions: {
    initEnv() { },
  },
  persist: true,
});
