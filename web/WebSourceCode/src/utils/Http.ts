import {MD5} from "crypto-js";
import axios, {AxiosHeaders, AxiosRequestHeaders, AxiosResponse} from "axios";
import {SearchMusicResult, SearchMusicResultSingle} from "@/utils/type/BasicType";

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

    async searchMusic(key: string, page: number) {
        return this.get<SearchMusicResult>("/qq/search/" + key + "/" + page);
    },

    async esQRCode() {
        let u = "/qq/search";
        return this.get<{
            code: Number;
            qrcode: string;
        }>(u);
    },

    uploadExams(uri: string) {
        return this.get<{
            code: number;
        }>("/exams/upExams/" + uri);
    },
    queryMineExams() {
        return this.get<{
            code: number;
            message: string;
            list: Array<String>;
        }>("/exams/query");
    },
    checkLogin() {
        return this.get<{
            code: number;
            message: string;
        }>("/user/checkUseful");
    },
    login(user: string, password: string) {
        let pwd = MD5(password).toString();
        return this.get<{
            message: string | undefined;
            token: string;
            code: number;
        }>("/user/login/" + user + "/" + pwd);
    },
    getImage(src: string) {
        return config.baseURL + `/getImage/${src}/${userStore().token}`;
    },
    getUserInfo() {
        return this.get<String>("/user/info");
    },
    removeExams(id: string) {
        return this.get<{
            message: string;
            code: number;
            data: Object;
        }>("/exams/cancelExams/" + id);
    },
    registerUser(info: { phoneNum: string; password: string }) {
        return this.post<{
            message: string;
            code: number;
            user: {
                nickName: string;
                sharedUid: number;
                userAvatar: string;
                userId: number;
                userPoints: number;
            };
        }>("/user/register", info);
    },
    postDownload(data: SearchMusicResultSingle, config: object) {
        return this.post("/download", {
            music: data,
            config: config
        })
    },
    setBaseConfig(param: { folder: string; num: number }) {
        return this.post("/config", param)
    },
    getBaseConfig() {
        return this.get<{ folder: string; num: number }>("/getConfig")
    }
};
