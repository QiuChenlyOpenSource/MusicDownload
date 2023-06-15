<!--
  - # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
  - # @作者         : 秋城落叶(QiuChenly)
  - # @邮件         : qiuchenly@outlook.com
  - # @文件         : 项目 [qqmusic] - Home.vue
  - # @修改时间    : 2023-04-14 01:38:05
  - # @上次修改    : 2023/4/14 下午1:38
  -->

<script setup lang="ts">
import { Download, Switch } from "@element-plus/icons-vue";
import { defineComponent, ref } from "vue";
import { SystemStore } from "@/store/SystemStore.js";
import { Api } from "@/utils/Http";

const { basicStore } = SystemStore();

const save_config = () => {
  Api.setBaseConfig({
    num: basicStore.config.concurrency.num,
    folder: basicStore.config.concurrency.downloadFolder,
  }).then((r) => {});
};

const customKey = ref("");

const loadConfig = () => {
  Api.getBaseConfig().then((r) => {
    basicStore.config.concurrency.num = r.num;
    basicStore.config.concurrency.downloadFolder = r.folder;
  });
};

loadConfig();

/**
 * 删除一个过滤关键词
 * @param key
 */
const deleteKeys = (key: string) => {
  let i = 0;
  for (let it of basicStore.filterKeys) {
    if (it === key) {
      basicStore.filterKeys.splice(i, 1);
      return;
    }
    i++;
  }
};

const enterClick = (ev: KeyboardEvent) => {
  if (ev.key === "Enter") {
    basicStore.filterKeys.push(customKey.value);
    customKey.value = "";
  }
};
</script>

<template>
  <div class="content">
    <h1 style="text-align: center">网易云曲库流浪计划</h1>
    <div class="safe-area">
      <el-space fill="fill" direction="vertical" wrap>
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>作品介绍</span>
            </div>
          </template>
          <div>本作品实现了如下功能:</div>
          <div>
            1.QQ音乐 无损音质解析下载 自动提取最高音质下载
            <span>Hi-Res -> Flac -> 320KbpsMP3 -> 128KbpsMP3</span>
          </div>
          <div>2. 登录网易云同步歌单匹配下载,已完成。</div>
        </el-card>

        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>设置</span>
            </div>
          </template>
          <div class="function">
            <div class="threadControl">
              <div>多线程数</div>
              <el-input
                v-model="basicStore.config.concurrency.num"
                placeholder="输入协程并发数量"
                :prefix-icon="Switch"
              />
            </div>
            <div class="threadControl">
              <div>下载目录</div>
              <el-input
                v-model="basicStore.config.concurrency.downloadFolder"
                placeholder="输入下载目录路径"
                :prefix-icon="Download"
              />
            </div>
            <div class="actions">
              <el-button type="success" @click="save_config">保存</el-button>
            </div>
          </div>
        </el-card>

        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>歌曲关键词过滤(修改即时生效)</span>
            </div>
          </template>
          <div class="filter-area">
            <div class="filter-list">
              <el-tag
                closable
                round
                effect="dark"
                class="filter-key"
                v-for="it in basicStore.filterKeys"
                :key="it"
                @close="deleteKeys(it)"
                >{{ it }}
              </el-tag>
              <div>
                <el-input
                  style="width: 400px"
                  v-model="customKey"
                  placeholder="输入自定义关键词并按下Enter"
                  @keyup="enterClick"
                />
              </div>
            </div>
          </div>
        </el-card>
      </el-space>
    </div>
    <div class="button-bar">
      <span>音质升级计划</span>
      <span>Design ❤️ QiuChenly @ 2023</span>
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

  .safe-area {
    flex: 1;
    width: 100%;
    display: flex;
    flex-direction: column;
    overflow: auto;

    .el-space {
      padding: 10px;

      .el-card {
      }
    }
  }

  .button-bar {
    font-size: 15px;
    //color: rgba(black, 0.6);
    border-top: 1px solid rgba(black, 0.1);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    padding: 30px 0;
  }

  .function {
    display: flex;
    flex-direction: column;
  }

  .threadControl {
    margin-bottom: 10px;
    display: inline-flex;
    flex-direction: column;

    .el-input {
      width: 400px;
    }
  }

  .filter-area {
    display: flex;
    flex-direction: column;

    .el-tag {
      margin-right: 10px;
      margin-bottom: 10px;

      &:last-of-type {
      }
    }
  }

  .actions {
    display: flex;
    justify-content: right;

    .el-button {
      min-width: 130px;
    }
  }
}
</style>
