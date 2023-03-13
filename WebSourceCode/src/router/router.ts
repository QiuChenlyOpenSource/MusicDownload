import Home from "@/components/Home.vue";
import Index from "@/components/Index.vue";
import NotFound from "@/components/NotFound.vue";
import SearchMusic from "@/components/SearchMusic.vue";
import {
    createWebHistory,
    createRouter,
    createWebHashHistory,
    RouterOptions,
    RouteRecordRaw,
} from "vue-router";
import Netease from "@/components/Netease.vue";
import Download from "@/components/Download.vue";

const routes = [
    {
        path: "/",
        name: "Index",
        component: Index,
        children: [
            {
                path: "home",
                alias: "/",//修复第一次打开页面白屏的问题
                component: Home,
            },
            {
                path: "search",
                component: SearchMusic,
            },
            {
                path: "netease",
                component: Netease,
            },
            {
                path: "download",
                component: Download,
            },
        ],
    },
    {
        path: "/home",
        name: "home",
        component: Home,
    },
    {
        path: "/:catchAll(.*)",
        component: NotFound,
    },
] as RouteRecordRaw[];

const router = createRouter({
    history: createWebHashHistory(),
    routes,
} as RouterOptions);

export default router;
