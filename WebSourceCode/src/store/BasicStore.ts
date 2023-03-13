/*
 * # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
 * # @作者         : 秋城落叶(QiuChenly)
 * # @邮件         : 1925374620@qq.com
 * # @文件         : 项目 [qqmusic] - BasicStore.ts
 * # @修改时间    : 2023-03-13 11:44:27
 * # @上次修改    : 2023/3/13 下午11:44
 */

import {defineStore} from "pinia";
import {NetEaseUserInfo} from "@/utils/type/UserInfoDetail";

export const BasicStore = defineStore("basicStore", {
    state: () => {
        return {
            firstOpen: true,
            token: "",
            searchHistory: [] as string[],
            lastSearch: "",
            config: {
                onlyMatchSearchKey: false,
                ignoreNoAlbumSongs: false,
                classificationMusicFile: false,
                concurrency: {
                    num: 16,
                    downloadFolder: ""
                },
                platform: "qq"
            },
            netease: {
                isLogin: false,
                token: "",
                anonimousCookie: "",
                user: {} as NetEaseUserInfo
            }
        };
    },
    getters: {},
    actions: {
        initEnv() {
        },
    },
    persist: true,
});
