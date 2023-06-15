<!--
  - # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
  - # @作者         : 秋城落叶(QiuChenly)
  - # @邮件         : qiuchenly@outlook.com
  - # @文件         : 项目 [qqmusic] - Index.vue
  - # @修改时间    : 2023-03-14 08:23:20
  - # @上次修改    : 2023/3/14 下午8:23
  -->

<template>
  <div class="content">
    <div class="left-banner">
      <div class="title">QQ音乐无损音源下载工具</div>
      <div class="functions">
        <div class="home-page" @click="router.push('/home')">
          <i-system-uicons-sun />
          <span>主页</span>
        </div>
        <div class="home-page" @click="router.push('/search')">
          <i-system-uicons-search />
          <span>音乐搜索</span>
        </div>
        <div class="home-page" @click="router.push('/netease')">
          <i-carbon-cloud-data-ops />
          <span>网易云登录</span>
        </div>
        <div class="home-page" @click="router.push('/cloud')">
          <i-carbon-cloud-data-ops />
          <span>网易云云盘</span>
        </div>
        <div class="home-page" @click="router.push('/download')">
          <i-carbon-download />
          <span>下载列表</span>
        </div>
      </div>
    </div>

    <div class="right-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import { SystemStore } from "@/store/SystemStore";

const { basicStore } = SystemStore();
// 路由传参
const router = useRouter();
onMounted(() => {
  if (basicStore.firstOpen) {
    setTimeout(() => {
      basicStore.token = "simulate load custom token";
      basicStore.firstOpen = false;
    }, 2000);
  }
});
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
  overflow: auto;

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
    overflow: auto;
  }
}
</style>
