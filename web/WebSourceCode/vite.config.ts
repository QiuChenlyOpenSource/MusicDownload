import { BuildOptions, defineConfig } from "vite";
import path from "path";
import vue from "@vitejs/plugin-vue";
import Icons from "unplugin-icons/vite";
import IconsResolver from "unplugin-icons/resolver";
import Inspect from "vite-plugin-inspect";
import Components from "unplugin-vue-components/vite";

let pathSrc = path.resolve(__dirname, "src");
// https://vitejs.dev/config/
export default defineConfig({
  build: {
    outDir: "../static",
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
    Icons({ compiler: "vue3" }),
    Inspect(),
  ],
  css: {
    preprocessorOptions: {
      scss: {
        additionalData: "@import '@/global/MainStyle.scss';",
      },
    },
  },
});
