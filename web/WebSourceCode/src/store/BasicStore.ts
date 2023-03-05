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
                }
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
