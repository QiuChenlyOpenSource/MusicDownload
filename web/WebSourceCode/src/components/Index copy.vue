<template>
  <div class="content">
    <div>
      <a href="https://vuejs.org/" target="_blank">
        <img src="@/assets/vue.svg" class="logo vue" alt="Vue logo" />
      </a>
    </div>

    主页
    <el-button @click="esLogin">获取二维码</el-button>
    <el-image
      style="width: 100px; height: 100px"
      :src="loginCode"
      fit="cover"
    />
    <div>{{ bStore.token }}</div>

    <p></p>
    <h3>关于unplugin-icons:</h3>
    <div>
      read more:
      <a href="https://github.com/antfu/unplugin-icons"
        >https://github.com/antfu/unplugin-icons</a
      >
    </div>
    <div>
      更多icons:
      <a href="https://icones.js.org/">https://icones.js.org/</a>
    </div>

    <code>自动导入 unplugin-icons </code>
    <div>
      <i-system-uicons-sun />
      <i-carbon-accessibility />
      <i-mdi-account-box style="font-size: 2em; color: red" />
    </div>

    <code>use unplugin-icons by raws - it's svg</code>
    <div>
      <span v-html="RawMdiAlarmOff" />
      <span v-html="RawMdiAlarmOff2" />
    </div>
  </div>
</template>

<script lang="ts" setup>
import RawMdiAlarmOff from "~icons/mdi/alarm-off?raw&width=4em&height=4em";
import RawMdiAlarmOff2 from "~icons/mdi/alarm-off?raw&width=1em&height=1em";

import { onMounted, ref } from "vue";
import { useRoute } from "vue-router";
import { ref2, SystemStore } from "@/store/SystemStore";
import { Api } from "@/utils/Http";

const { basicStore } = SystemStore();
const bStore = ref2(basicStore); //写入basicStore数据后这里自动刷新 可以绑定到界面上

const loginCode = ref("");

// 路由传参
const route = useRoute();

onMounted(() => {
  if (basicStore.firstOpen) {
    console.log("用户是第一次打开哦");

    setTimeout(() => {
      basicStore.token = "simulate load custom token";
      basicStore.firstOpen = false;
    }, 2000);
  }
});

const esLogin = () => {
  Api.esQRCode().then((r) => {
    loginCode.value = r.qrcode;
  });
};
</script>

<style lang="scss" scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
}

.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}

.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}

.content {
  text-align: center;
  width: 100%;
  height: 100%;

  display: flex;
  flex-direction: column;
  justify-content: center;
}
</style>
