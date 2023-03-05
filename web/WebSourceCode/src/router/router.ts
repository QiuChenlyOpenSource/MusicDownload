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

const routes = [
  {
    path: "/",
    name: "Index",
    component: Index,
    children: [
      {
        path: "home",
        component: Home,
      },
      {
        path: "search",
        component: SearchMusic,
      },
      {
        path: "netease",
        component: NotFound,
      },
      {
        path: "download",
        component: NotFound,
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
