/*
 * # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
 * # @作者         : 秋城落叶(QiuChenly)
 * # @邮件         : qiuchenly@outlook.com
 * # @文件         : 项目 [qqmusic] - vite.config.ts
 * # @修改时间    : 2023-03-15 03:50:51
 * # @上次修改    : 2023/3/15 上午3:50
 */

import { BuildOptions, defineConfig } from "vite";
import path from "path";
import vue from "@vitejs/plugin-vue";
import Icons from "unplugin-icons/vite";
import IconsResolver from "unplugin-icons/resolver";
import Inspect from "vite-plugin-inspect";
import Components from "unplugin-vue-components/vite";
import viteCompression from "vite-plugin-compression";

let pathSrc = path.resolve(__dirname, "src");
// https://vitejs.dev/config/
export default defineConfig({
  build: {
    outDir: "../flaskSystem/static",
    terserOptions: {
      compress: {
        drop_console: true,
        drop_debugger: true,
      },
    },
    rollupOptions: {
      // output: { //静态资源分类打包
      //     chunkFileNames: 'static/js/[name]-[hash].js',
      //     entryFileNames: 'static/js/[name]-[hash].js',
      //     assetFileNames: 'static/[ext]/[name]-[hash].[ext]',
      //     manualChunks(id) { //静态资源分拆打包
      //         if (id.includes('node_modules')) {
      //             return id.toString().split('node_modules/')[1].split('/')[0].toString();
      //         }
      //     }
      // }
    },
  } as BuildOptions,
  resolve: {
    alias: {
      "@": pathSrc,
    },
  },
  plugins: [
    vue(),
    Components({
      resolvers: [IconsResolver()],
    }),

    Icons({
      compiler: "vue3",
      autoInstall: true,
    }),
    Inspect(),
    // viteCompression({
    //     verbose: true,
    //     disable: false,
    //     threshold: 10240,
    //     algorithm: 'gzip',
    //     ext: '.gz',
    // }),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: "@import '@/global/MainStyle.scss';",
      },
    },
  },
});
