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
import { defineComponent, watch, ref, onMounted } from "vue";
import { SystemStore } from "@/store/SystemStore.js";
import { Api } from "@/utils/Http";
import { platformListv2, MetaInfomationSupport, MetaInfomationSupportOptions, MetaInfomationSupportTypes } from "@/utils/Utils";
import { ElDivider, ElMessage } from 'element-plus';

const { basicStore } = SystemStore();

const save_config = () => {
  Api.setBaseConfig({
    num: basicStore.config.concurrency.num,
    folder: basicStore.config.concurrency.downloadFolder,
    lyric: basicStore.config.concurrency.saveLyric
  }).then((r) => { });
};

const customKey = ref("");

const title_height = ref()

const title_height_size = ref(0)

onMounted(() => {
  title_height_size.value = title_height.value.clientHeight;
})

const loadConfig = () => {
  Api.getBaseConfig().then((r) => {
    basicStore.config.concurrency.num = r.num;
    basicStore.config.concurrency.downloadFolder = r.folder;
    basicStore.config.concurrency.saveLyric = r.lyric;
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

const addFilter = function (obj: any) {
  obj.metas.push({
    meta_support: 'iTunes',
    meta_option: 'reflect',
    meta_types: 'albumName',
    from: "",
    to: ""
  })
}

const addFilterBase = function () {
  basicStore.MusicMetaPrepare.push({
    platform: "mg",
    metas: [{
      meta_support: 'iTunes',
      meta_option: 'reflect',
      meta_types: 'albumName',
      from: "",
      to: ""
    }]
  })
}

const selectOptions = ref(false)
const importorexport = ref(false)
const localConfiguration = ref("")
const optionOps = ref({
  title: "",
  data: {} as any,
  target: {} as any
})

let stopWatch: any = null;

const showOptions = (selectData: any, callback: Function, lstData: any) => {
  optionOps.value.data = lstData;
  if (stopWatch !== null) stopWatch();
  stopWatch = watch(optionOps, (nl, old) => {
    callback(nl.target)
  }, { deep: true })

  optionOps.value.target = selectData;
  selectOptions.value = true;
}

/**
 * 格式化对象成可读性较高的对象
 * @param objs 
 */
const parseKeys = (objs: any) => {
  let obj = {} as any
  for (let it in objs) {
    // console.log(it);
    obj[it] = objs[it]['name']
  }
  return obj
}

const saveLocalConfigurature = () => {
  try {
    basicStore.MusicMetaPrepare = JSON.parse(localConfiguration.value)
    importorexport.value = false
  } catch (error) {
    console.log(error);
    ElMessage({
      type: "error",
      message: '出现错误: ' + error
    })
  }
}

const loadLocalConfigurature = () => {
  localConfiguration.value = JSON.stringify(basicStore.MusicMetaPrepare)
  importorexport.value = true
}
</script>

<template>
  <div class="content">
    <span class="title-name" ref="title_height">
      <el-image class="logo" src="../static/svg/web-2191ca79.svg"></el-image>
      <span>&nbsp;|&nbsp;</span>
      <span>曲库流浪计划</span>
    </span>
    <div class="safe-area" :style="{
      'padding-top': title_height_size + 'px'
    }">
      <div class="cards">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>简介</span>
            </div>
          </template>
          <h2>项目介绍</h2>
          <div>本作品实现了如下功能:</div>
          <div>
            1.QQ音乐 无损音质解析下载 自动提取最高音质下载
            <span>Hi-Res -> Flac -> 320KbpsMP3 -> 128KbpsMP3</span>
          </div>
          <div>2. 登录网易云同步歌单匹配下载,目前因为兼容性问题已停止使用。</div>
          <div>3. 酷我音乐无损歌曲解析。</div>
          <div>4. qq音乐元数据填充，苹果专辑元数据自动填充，歌词自动下载。</div>
          <div>5. 完美写入MP3/FLac元数据 让emby等支持读取音乐标签的软件分类管理。</div>
          <br>
          <h2>致谢</h2>
          <div>1. 本页面图标logo来自于@Vectorzhao(https://github.com/VectorZhao),感谢设计。</div>
          <div>2. 酷我音乐直链解析算法来自于@彭狸花喵(https://github.com/helloplhm-qwq),感谢TA的逆向分析。</div>
          <div>3. 还有很多其他的开发者向我提供了宝贵的Pull Requests,在此一并感谢！</div>

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
              <el-input v-model="basicStore.config.concurrency.num" placeholder="输入协程并发数量" :prefix-icon="Switch" />
            </div>
            <div class="threadControl">
              <div>下载目录</div>
              <el-input v-model="basicStore.config.concurrency.downloadFolder" placeholder="输入下载目录路径"
                :prefix-icon="Download" />
            </div>
            <div class="threadControl">
              <el-checkbox v-model="basicStore.config.concurrency.saveLyric" label="单独保存歌词文件" />
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
              <el-tag closable round effect="dark" class="filter-key" v-for="it in basicStore.filterKeys" :key="it"
                @close="deleteKeys(it)">{{ it }}
              </el-tag>
              <div>
                <el-input v-model="customKey" placeholder="输入自定义关键词并按下Enter" @keyup="enterClick" />
              </div>
            </div>
          </div>
        </el-card>

        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>元数据匹配</span>
            </div>
          </template>
          <el-dialog class="dialog-attr" destroy-on-close align-center v-model="selectOptions"
            :title="'请选择' + optionOps.title">
            <el-select v-model="optionOps.target" placeholder="请选择接口" style="width: 100%">
              <el-option v-for="(it, vl) in optionOps.data" :label="it" :value="vl" />
            </el-select>
          </el-dialog>
          <el-dialog class="dialog-attribute" destroy-on-close align-center v-model="importorexport" width="90%"
            :title="'导出或导入规则'">

            <div class="dialog-cts">
              <textarea v-model="localConfiguration" placeholder="请粘贴json数据">
              </textarea>
              <el-button type="primary" @click="saveLocalConfigurature">保存</el-button>
            </div>
          </el-dialog>
          <div class="filter-area">
            <div class="filter-list">
              <div class="add-filter" v-for="(prepare, inx) in basicStore.MusicMetaPrepare">
                从<span class="option-style"
                  @click="showOptions(prepare.platform, (vl: string) => { prepare.platform = vl }, platformListv2)">
                  {{ platformListv2[prepare.platform]
                  }}
                </span>下载后, 匹配元数据时执行:
                <el-divider />
                <div v-if="prepare.metas && prepare.metas.length === 0">此规则没有任何约束，请增加一条约束。</div>
                <div class="extra-meta" v-for="(metas_instance, inx1) in prepare.metas">
                  <div class="extra-info">
                    用<span class="option-style"
                      @click="showOptions(metas_instance.meta_support, (vl: string) => { metas_instance.meta_support = vl }, MetaInfomationSupport)">
                      {{ MetaInfomationSupport[metas_instance.meta_support]
                      }}
                    </span>查询元数据时, 从{{ platformListv2[prepare.platform] }}下载歌曲的
                    <span class="option-style"
                      @click="showOptions(metas_instance.meta_types, (vl: string) => { metas_instance.meta_types = vl }, MetaInfomationSupportTypes)">
                      {{ MetaInfomationSupportTypes[metas_instance.meta_types]
                      }}
                    </span>{{ MetaInfomationSupportOptions[metas_instance.meta_option]['lint'] }}
                    <el-input v-model="metas_instance.from" placeholder="输入原始内容" />

                    <span class="option-style"
                      @click="showOptions(metas_instance.meta_option, (vl: string) => { metas_instance.meta_option = vl }, parseKeys(MetaInfomationSupportOptions))">
                      {{ MetaInfomationSupportOptions[metas_instance.meta_option]["name"]
                      }}
                    </span>为<el-input v-model="metas_instance.to" placeholder="将替换的内容" /><br /><br />
                    <el-button type="danger" @click="prepare.metas.splice(inx1, 1)">删除约束</el-button>
                  </div>
                </div>
                <el-divider />
                <el-button type="success" @click="addFilter(prepare)">添加约束</el-button>
                <el-button type="danger" @click="basicStore.MusicMetaPrepare.splice(inx, 1)">删除规则</el-button>
              </div>
            </div>
            <div>
              <el-button type="success" @click="addFilterBase">添加新规则</el-button>
              <el-button type="primary" @click="loadLocalConfigurature">添加外部规则</el-button>
            </div>
          </div>
        </el-card>
      </div>
    </div>
    <div class="button-bar">
      <span>音质升级计划</span>
      <span>Design ❤️ <a href="https://github.com/QiuChenlyOpenSource/QQFlacMusicDownloader">秋城落叶开源项目</a> @ 2023</span>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@media screen and (max-width: 550px) {
  .content {
    .title-name {
      font-size: 15px !important;
    }

    .button-bar {
      font-size: 10px !important;
      //color: rgba(black, 0.6);
      border-top: 1px solid var(--qiuchen-text-15) !important;
      padding: 15px 0 !important;
    }

    .filter-area {
      .el-tag {
        padding: 15px 20px;
        font-size: 14px;
      }
    }
  }
}

.content {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  position: relative;

  .title-name {
    font-size: 28px;
    text-align: center;
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    background-color: rgba(black, 0.1);
    backdrop-filter: blur(10px);
    height: 45px;
    padding: 10px 0;
    display: flex;
    align-items: center;
    justify-content: center;
    border-bottom: solid 1px rgba(white, 0.1);
    z-index: 1;

    .logo {
      height: 40px;
      will-change: filter;
    }
  }

  .safe-area {
    flex: 1;
    overflow-x: hidden;

    .cards {
      margin: 10px;

      .el-card {
        margin-bottom: 10px;
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
    transition: padding .5s;
  }

  .function {
    display: flex;
    flex-direction: column;
  }

  .threadControl {
    margin-bottom: 10px;
    display: inline-flex;
    flex-direction: column;
  }

  .box-card {
    // padding: 10px;
  }


  :deep(.el-card__body) {
    padding: 10px;
  }

  :deep(.el-dialog__body) {
    padding: 10px;
  }

  .dialog-cts {
    height: 70vh;
    display: flex;
    flex-direction: column;

    textarea {
      flex: 1;
      margin-bottom: 10px;
      resize: none;
      overflow-y: scroll;
      outline: none;
      border: none;
      border-radius: 8px;
      padding: 10px;
      box-shadow: 0 0 10px rgba($color: #000000, $alpha: .15);
    }

    textarea::-webkit-scrollbar {
      width: 5px;
    }

    textarea::-webkit-scrollbar-track {
      border-radius: 10px;
      background: black;
    }

    textarea::-webkit-scrollbar-thumb {
      background: rgba(white, 0.4);
      border-radius: 10px;
    }

    textarea::-webkit-scrollbar-thumb:hover {
      background: rgba(white, 0.8);
    }
  }

  .filter-area {
    display: flex;
    flex-direction: column;

    .el-tag {
      margin-right: 10px;
      margin-bottom: 10px;
      transition: padding .5s;

      &:last-of-type {}
    }
  }

  .actions {
    display: flex;
    justify-content: right;

    .el-button {
      min-width: 130px;
    }
  }

  .meta-list {
    margin-top: 10px;
    border-radius: 8px;
    padding: 10px;
    border: solid 0.2px rgba($color: #000000, $alpha: .15);
    box-shadow: 0 2px 5px rgba($color: #000000, $alpha: .1);
  }

  .extra-meta {
    display: flex;
    flex-direction: column;
  }

  .extra-info {
    display: inline-block;
    margin-bottom: 10px;

    .el-input {
      width: auto;
    }
  }

  .add-filter {
    border: solid 1px var(--black);
    padding: 10px;
    border-radius: 4px;
    // box-shadow: 0 5px 6px rgba($color: #000000, $alpha: .1);
    margin-bottom: 10px;
  }

  .option-style {
    border: solid 1px var(--qiuchen-white-50);
    margin: 5px 10px;
    padding: 5px 10px;
    display: inline-block;
    cursor: pointer;
    transition: all .25s cubic-bezier(0.075, 0.82, 0.165, 1);

    &:hover {
      background-color: var(--black);
      color: var(--white);
    }
  }
}
</style>
