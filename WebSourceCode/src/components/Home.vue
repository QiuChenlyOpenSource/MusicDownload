<script setup lang="ts">
import {Download, Switch} from "@element-plus/icons-vue";
import {defineComponent} from "vue";
import {SystemStore} from "@/store/SystemStore.js";
import {Api} from "@/utils/Http";

const {basicStore} = SystemStore()

const save_config = () => {
  Api.setBaseConfig({
    num: basicStore.config.concurrency.num,
    folder: basicStore.config.concurrency.downloadFolder,
  }).then(r => {

  })
}

const loadConfig = () => {
  Api.getBaseConfig().then(r => {
    basicStore.config.concurrency.num = r.num;
    basicStore.config.concurrency.downloadFolder = r.folder;
  })
}

loadConfig()
</script>

<template>
  <div class="content">
    <h1 style="text-align: center">网易云曲库流浪计划</h1>
    <div class="description">
      <div>本作品实现了如下功能:</div>
      <br/>
      <div>1.QQ音乐 无损音质解析下载
        <br/>
        自动提取最高音质下载
        <br/>
        <span>Hi-Res -> Flac -> 320KbpsMP3 -> 128KbpsMP3</span>
      </div>
      <br/>
      <div>
        2. 登录网易云同步歌单匹配下载 - 开发中，未完成。
      </div>

      <div class="function">
        <div class="threadControl">
          <div>多线程设置</div>
          <el-input
              v-model="basicStore.config.concurrency.num"
              placeholder="输入协程并发数量"
              :prefix-icon="Switch"
          />
        </div>
        <div class="threadControl">
          <div>下载目录设置</div>
          <el-input
              style="width: 400px;"
              v-model="basicStore.config.concurrency.downloadFolder"
              placeholder="输入下载目录路径"
              :prefix-icon="Download"
          />
        </div>
        <div class="actions">
          <el-button type="success" @click="save_config">保存</el-button>
        </div>
      </div>

    </div>
    <div class="button-bar">
      <span>Music Quality Upgrade Plan</span>
      <span>Design by QiuChenly</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;

  .description {
    flex: 1;
    padding: 10px;
    // background-color: red;

    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    .function {
      display: flex;
      flex-direction: column;

      > div {
        margin-top: 20px;
      }
    }
  }

  .button-bar {
    font-size: 15px;
    color: rgba(black, 0.6);
    border-top: 1px solid rgba(black, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 30px 0;
  }

  .threadControl {
    display: inline-flex;
    align-items: center;

    > div {

    }

    .el-input {
      margin-left: 10px;
      flex: 1;
    }
  }

  .actions {
    display: flex;
    justify-content: center;

    .el-button {
      min-width: 130px;
    }
  }
}
</style>
