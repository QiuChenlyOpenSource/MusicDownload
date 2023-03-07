import {MD5} from "crypto-js";
import axios, {AxiosHeaders, AxiosRequestHeaders, AxiosResponse} from "axios";
import {InitAnonimous, SearchMusicResult, SearchMusicResultSingle} from "@/utils/type/BasicType";
import {NetEaseUserInfo} from "@/utils/type/UserInfoDetail";
import {MusicPlaylist} from "@/utils/type/NeteaseMusicPlayList";
import {NeteasePlayListSongs} from "@/utils/type/NetEasePlayListSong";

const userStore = () => {
    return {
        token: "test",
    };
};

const config = {
    baseURL: "http://localhost:8899",
    timeout: 1000,
    headers: {
        "Content-Type": "multipart/form-data;application/json;charset=UTF-8;",
    },
};

const http = axios.create(config);

//请求拦截器
http.interceptors.request.use(
    (config) => {
        // 可使用async await 做异步操作
        const token = userStore().token;
        if (token) {
            config.headers["token"] = token;
            // console.log("config.method", config);
            // if (config.method === "POST") {
            //   //@ts-ignore
            //   config.data = JSON.stringify(config.data);
        }
        return config;
    },
    (error) => {
        return Promise.resolve(error);
    }
);

// 响应拦截器
http.interceptors.response.use(
    (response) => {
        console.log(response);
        return response;
    },
    (error) => {
        //未登录时清空缓存跳转
        // if (error.statusCode == 401) {
        //     uni.clearStorageSync();
        //     uni.switchTab({
        //         url: "/pages/index/index.vue"
        //     })
        // }
        // uni.showToast({
        //   title: "网络开了小差～",
        //   icon: "error",
        //   mask: true,
        // });
        return Promise.resolve(error);
    }
);
export const Client = http;

export const Api = {
    pack<T>(res: AxiosResponse<T>) {
        return res.data;
    },
    async get<T>(url: string) {
        const r = await Client.get<T>(url);
        return this.pack(r);
    },
    async post<T>(url: string, data: object) {
        const r = await Client.post<T>(url, data, {
            headers: {
                "Content-Type": "application/json",
            },
        });
        return this.pack(r);
    },
    async status() {
        return this.get<{
            code: Number;
        }>("/status");
    },
    async searchMusic(key: string, page: number, type = 'qq', size = 30) {
        let url = ''
        if (type === 'qq')
            url = "/qq/search/" + key + "/" + page
        else if (type === 'kw')
            url = "/kw/search/" + key + "/" + page + '/' + size
        else if (type === 'wyy')
            url = "/wyy/search/" + key + "/" + page + '/' + size
        else if (type === 'mg')
            url = "/mg/search/" + key + "/" + page + '/' + size
        return this.get<SearchMusicResult>(url);
    },
    postDownload(data: object, config: object, platform = 'qq') {
        return this.post("/download", {
            music: data,
            config: config,
            platform: platform
        })
    },
    setBaseConfig(param: { folder: string; num: number }) {
        return this.post("/config", param)
    },
    getBaseConfig() {
        return this.get<{ folder: string; num: number }>("/getConfig")
    },
    getNeteaseQRCode() {
        return this.get<{
            code: Number;
            qrcode: {
                'url': string,
                'b64': string,
                'uniKey': string
            };
        }>("/es/qrLogin")
    },
    checkESState: (unikey: string) => Api.get<{
        code: number,
        cookie: string
    }>("/es/checkLoginState/" + unikey),
    getNetEaseUserInfo: () => Api.get<NetEaseUserInfo>("/es/getUserInfo"),
    /**
     * 把本地保存的cookie设置进去 防止二次登录
     * @param data
     */
    setESCookie: (data: {
        cookie: string
    }) => Api.post<{
        code: number
    }>("/es/setCookie", data),
    initAnonimous: () => Api.get<InitAnonimous>("/es/initAnonimous"),
    getUserPlaylist: (userid: string) => Api.get<MusicPlaylist>("/es/getUserPlaylist/" + userid),
    getMusicListByPlaylistID: (playListID: string, page: number, size: number) => Api.get<NeteasePlayListSongs>(`/es/getMusicListByPlaylistID/${playListID}/${page}/${size}`)
};
