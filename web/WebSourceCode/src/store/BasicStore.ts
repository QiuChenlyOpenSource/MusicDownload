import {defineStore} from "pinia";

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
