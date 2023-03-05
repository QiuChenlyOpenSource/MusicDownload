<template>
  <div class="content">
    <div class="left-banner">
      <div class="title">QQ音乐无损音源下载工具</div>
      <div class="functions">
        <div class="home-page" @click="router.push('/home')">
          <i-system-uicons-sun/>
          <span>主页</span>
        </div>
        <div class="home-page" @click="router.push('/search')">
          <i-system-uicons-search/>
          <span>音乐搜索</span>
        </div>
        <div class="home-page" @click="router.push('/netease')">
          <i-carbon-cloud-data-ops/>
          <span>网易云登录</span>
        </div>
        <div class="home-page" @click="router.push('/download')">
          <i-carbon-download/>
          <span>下载列表</span>
        </div>
      </div>
    </div>

    <div class="right-content">
      <router-view></router-view>

      <!-- <el-button @click="esLogin">获取二维码</el-button>
      <el-image
        style="width: 100px; height: 100px"
        :src="loginCode"
        fit="cover"
      /> -->
    </div>
  </div>
</template>

<script lang="ts" setup>
import {onMounted, ref} from "vue";
import {useRoute, useRouter} from "vue-router";
import {ref2, SystemStore} from "@/store/SystemStore";
import {Api} from "@/utils/Http";

const {basicStore} = SystemStore();
const bStore = ref2(basicStore); //写入basicStore数据后这里自动刷新 可以绑定到界面上

const loginCode = ref("");

// 路由传参
const route = useRoute();
const router = useRouter();
onMounted(() => {
  if (basicStore.firstOpen) {
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

const music_page = () => {
  //二级路由自动识别
  router.push("/search");
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
  width: 100%;
  height: 100%;
  display: flex;

  min-width: 800px;
  min-height: 600px;
  overflow: scroll;

  .left-banner {
    overflow: hidden;
    box-shadow: 0 0 10px var(--qiuchen-text);
    // background-color: darkorange;
    width: 300px;
    min-width: 300px;
    min-height: 100%;
    z-index: 1;

    .title {
      height: 65px;
      display: flex;
      align-items: center;
      justify-content: center;
      // background-color: darkorange;
      box-shadow: 0 0 10px var(--qiuchen-text);
    }

    .functions {

      & div {
        // background-color: #000;
        box-shadow: 0 0 6px var(--qiuchen-text);
        margin: 10px;
        padding: 15px 0;
        display: flex;
        align-items: center;
        justify-content: left;
        padding-left: 20px;
        border-radius: 5px;
        cursor: pointer;
        transition: all 0.3s;

        &:hover {
          box-shadow: 0 0 6px var(--qiuchen-hover-text);
        }

        & span {
          margin-left: 10px;
        }
      }
    }
  }

  .right-content {
    // background-color: gainsboro;
    flex: 1;
    overflow: scroll;
  }
}
</style>
