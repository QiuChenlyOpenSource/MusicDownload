/*
 * # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
 * # @作者         : 秋城落叶(QiuChenly)
 * # @邮件         : qiuchenly@outlook.com
 * # @文件         : 项目 [qqmusic] - router.ts
 * # @修改时间    : 2023-03-14 08:22:45
 * # @上次修改    : 2023/3/14 下午8:22
 */

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
import Cloud from "@/components/Cloud.vue";

const routes = [
  {
    path: "/",
    name: "Index",
    component: Index,
    children: [
      {
        path: "home",
        alias: "/", //修复第一次打开页面白屏的问题
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
      {
        path: "cloud",
        component: Cloud,
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
