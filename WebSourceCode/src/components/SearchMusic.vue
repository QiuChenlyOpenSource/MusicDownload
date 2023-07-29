<!--
  - # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
  - # @作者         : 秋城落叶(QiuChenly)
  - # @邮件         : qiuchenly@outlook.com
  - # @文件         : 项目 [qqmusic] - SearchMusic.vue
  - # @修改时间    : 2023-04-14 01:33:25
  - # @上次修改    : 2023/4/14 下午1:33
  -->

<script lang="ts" setup>
import { Search } from "@element-plus/icons-vue";
import { ref, onMounted, watch, watchEffect } from "vue";
import { ref2, SystemStore } from "@/store/SystemStore";
import { Api } from "@/utils/Http";
import {
  SearchMusicResult,
  SearchMusicResultSingle,
} from "@/utils/type/BasicType";

//@ts-ignore
import EncodeEx from "../utils/MyMp3.js";
//@ts-ignore
import encMD5 from "../utils/kw.js"

import { platformList } from "@/utils/Utils";

import { ElMessage, ElNotification } from "element-plus";

const { basicStore } = SystemStore();
const refbasicStore = ref2(basicStore);
const music_current_page = ref(1);
const headRef = ref();

const searchByNetease = defineProps<{
  search: string | undefined;
}>();

watch(refbasicStore.lastSearch, (now, old) => {
  if (now.length === 0) {
    searchCache.value = undefined;
    music_current_page.value = 1;
  }
});

watch(refbasicStore.config.value, () => {
  searchCache.value = undefined;
  music_current_page.value = 1;
});

function page_change() {
  search();
}

const searchCache = ref<SearchMusicResult>();

const getMusicSinger = (music: SearchMusicResultSingle) => music.singer;
// .map(v => {
// return v.name
// }).join(music.singer.length === 1 ? '' : "&")

const timeFormat = (row: SearchMusicResultSingle) => {
  if (basicStore.config.platform === "wyy") {
    let date: any = new Date(row.time_publish);
    let day = date.getDate();
    let month = date.getMonth();
    let year = date.getFullYear();
    if (day < 10) day = "0" + day;
    if (month < 10) month = `0${month}`;
    return year + "-" + month + "-" + day;
  }
  return row.time_publish === "" ? "0000-01-01" : row.time_publish;
};

/**
 * 检查这首曲子是否不符合过滤标准 true表示曲子可以给用户显示 false反之
 * @param singleMusic
 */
const filterList = (singleMusic: SearchMusicResultSingle) => {
  if (!basicStore.config.disableFilterKey) {
    for (let k of basicStore.filterKeys) {
      if (singleMusic.title.toUpperCase().includes(k.toUpperCase()))
        return false;
    }
  }
  if (basicStore.config.ignoreNoAlbumSongs) {
    if (singleMusic.album == "未分类专辑" || singleMusic.album == "")
      return false;
  }
  if (basicStore.config.onlyMatchSearchKey) {
    let artist = getMusicSinger(singleMusic);
    // console.log("歌手", artist, "搜索的", basicStore.lastSearch)
    if (!artist.includes(basicStore.lastSearch)) return false;
  }
  return true;
};

const search = async () => {
  if (
    basicStore.searchHistory.find(
      (v, i, array) => v === basicStore.lastSearch
    ) === undefined
  )
    basicStore.searchHistory.push(basicStore.lastSearch);

  const resolve = (searchMusicResult: SearchMusicResult) => {
    let lst = [] as Array<SearchMusicResultSingle>;
    searchMusicResult.list.forEach((v) => {
      if (filterList(v)) lst.push(v);
    });
    searchMusicResult.list = lst;
    searchCache.value = searchMusicResult;
  };

  if (basicStore.config.platform === "myfreemp3") {
    let data = EncodeEx({
      type: "YQM",
      text: basicStore.lastSearch,
      page: music_current_page.value,
      v: "beta",
    });
    Api.searchMusicForMyFreeMp3(basicStore.config.platform, data).then(resolve);
  }
  else if (basicStore.config.platform === "kw") {
    const token = await Api.getKWToken();
    const result = encMD5(token.token)
    console.log(token.token, result);
    Api.searchMusic(
      basicStore.lastSearch,
      music_current_page.value,
      basicStore.config.platform,
      30,
      "/" + token.token + "/" + result
    ).then(resolve);
  }
  else
    Api.searchMusic(
      basicStore.lastSearch,
      music_current_page.value,
      basicStore.config.platform,
    ).then(resolve);
};

function getSinger(
  row: SearchMusicResultSingle,
  column: any,
  cellValue: any,
  index: number
) {
  // console.log(row)
  return getMusicSinger(row);
}

function getFileTypeAndSize(
  row: SearchMusicResultSingle,
  column: any,
  cellValue: any,
  index: number
) {
  // console.log(row)
  return row.notice + " | " + row.size;
}

const paddingHeadHeight = ref(0);



onMounted(() => {
  const observer = new ResizeObserver(entries => {
    // 在回调中获得高度 
    paddingHeadHeight.value = headRef.value.clientHeight
  })
  observer.observe(headRef.value)

  window.onresize = () => {
    // 窗口大小变化时更新高度
    paddingHeadHeight.value = headRef.value.clientHeight

  }

  // console.log(headRef.value);
  // const h = headRef.value as HTMLDivElement;
  // paddingHeadHeight.value = h.offsetTop + h.offsetHeight;
  console.log("searchByNetease", searchByNetease);
  if (searchByNetease.search !== undefined) {
    basicStore.lastSearch = searchByNetease.search;
    search();
  }
});

function parseParams(data: any) {
  try {
    var tempArr = [];
    for (var i in data) {
      var key = encodeURIComponent(i);
      var value = encodeURIComponent(data[i]);
      tempArr.push(key + "=" + value);
    }
    var urlParamsStr = tempArr.join("&");
    return urlParamsStr;
  } catch (err) {
    return "";
  }
}

const handleDown = (data: SearchMusicResultSingle) => {
  console.log(data);
  let _data = { ...data };
  if (basicStore.config.platform === "myfreemp3") {
    _data["prefix"] =
      "https://test.quanjian.com.cn/m/api/link?" +
      parseParams(
        EncodeEx({
          id: _data.mid.toString(),
          quality: _data.prefix.toString(),
        })
      );
  }
  Api.postDownload(_data, basicStore.config).then((r) => {
    if (r.code === 200) {
      ElNotification({
        title: "成功",
        message: "已经提交[" + _data.readableText + "]下载任务",
        type: "success",
      });
    }
  });
};

/**
 * 加个循环批量提交下载任务
 */
const downloadAllOfPage = () => {
  if (searchCache.value === undefined) return;
  for (let a of searchCache.value.list) {
    handleDown(a);
  }
};

/**
 * 触发下载操作
 */
const handleSearch = () => {
  searchCache.value = undefined;
  music_current_page.value = 1;
  search();
};

const downloadAllPage = function () {
  ElNotification({
    title: '功能还没做捏',
    message:
      '关注嘉然 顿顿解馋 关注柯洁喵 谢谢喵 关注七海Nana7mi 010 谢谢喵 关注天选罕见冬雪莲 谢谢喵',
    type: 'error',
  });
}
</script>

<template>
  <div class="content">
    <div ref="headRef" class="head-section">
      <div class="top-tip">搜索</div>
      <div class="area-top">
        <el-input v-model="basicStore.lastSearch" placeholder="请输入关键词搜索" class="input-with-select"
          @keyup.enter="handleSearch">
          <template #prepend>
            <el-select v-model="basicStore.config.platform" placeholder="请选择接口" style="width: 120px">
              <el-option v-for="it in platformList" :label="it.name" :value="it.value" />
            </el-select>
          </template>
          <template #append>
            <el-button :icon="Search" @click="handleSearch" />
          </template>
        </el-input>
        <div class="options">
          <el-checkbox v-model="basicStore.config.onlyMatchSearchKey" label="仅显示搜索的歌手歌曲" />
          <el-checkbox v-model="basicStore.config.disableFilterKey" label="不使用关键词过滤歌曲" />
          <el-checkbox v-model="basicStore.config.ignoreNoAlbumSongs" label="屏蔽无所属专辑歌曲" />
          <el-checkbox v-model="basicStore.config.classificationMusicFile" label="下载歌曲按专辑分类" />
          <!--        <el-checkbox v-model="classificationMusicFile" label="按照专辑名称分文件夹归档音乐歌曲文件"/>-->
          <!--        <el-checkbox v-model="checked3" label="Option 1"/>-->
        </div>
        <div class="area-action" v-if="searchCache &&
          searchCache.page.size > 0 &&
          searchCache?.list.length !== 0
          ">
          <el-button type="primary" @click="downloadAllOfPage">仅下载本页
          </el-button>
          <el-button type="primary" @click="downloadAllPage">下载所有页
          </el-button>
        </div>
      </div>
    </div>
    <div :style="{
      'margin-top': paddingHeadHeight + 'px',
    }" v-if="searchCache === undefined || basicStore.lastSearch.length === 0" class="history">
      <div class="union">
        <i-system-uicons-undo-history />
        <span style="margin-left: 4px">历史搜索</span>
      </div>
      <div class="h-list">
        <div v-for="ind in refbasicStore.searchHistory.value" @click="basicStore.lastSearch = ind" class="search-tag">
          {{ ind }}
        </div>
      </div>
      <div v-if="basicStore.searchHistory.length > 0" class="clear-all-history" @click="basicStore.searchHistory = []">
        <i-icon-park-twotone-clear-format />
      </div>
    </div>
    <!-- :style="{
      height: 'calc(100% - ' + paddingHeadHeight + 'px)',
    }" -->
    <div v-else class="search-list" :style="{
      'margin-top': paddingHeadHeight + 'px',
    }">
      <div style="margin: 10px" v-if="searchCache === undefined || searchCache.list.length === 0" class="error-load">
        <el-empty :description="searchCache?.page.size > 0
          ? '共搜索到' +
          searchCache?.page.size +
          '条数据,但是过滤后没有发现符合条件的数据。请检查搜索过滤条件是否设置正确。'
          : '服务器请求搜索结果失败,请重试。'
          " />
      </div>
      <div class="search-list-a" v-else>
        <div class="container">
          <el-table class="my-tb" :data="searchCache.list" style="width: 100%; z-index: 0">
            <el-table-column :formatter="timeFormat" prop="time_public" label="发表时间" width="120" />
            <el-table-column :show-overflow-tooltip="true" prop="title" label="歌曲名" min-width="300">
              <template #default="scope">
                <div class="title-tip">
                  <div class="flac-tip" v-if="scope.row.extra === 'flac'">
                    无损
                  </div>
                  <div class="name">{{ scope.row.title }}</div>
                </div>
              </template>
            </el-table-column>
            <el-table-column :show-overflow-tooltip="true" :formatter="getSinger" prop="singer.name" label="艺术家"
              width="200" />
            <el-table-column :show-overflow-tooltip="true" prop="album" label="专辑" width="200" />
            <el-table-column :formatter="getFileTypeAndSize" :show-overflow-tooltip="true" prop="notice" label="品质"
              width="250" />
            <el-table-column fixed="right" label="操作">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="handleDown(scope.row)">下载
                </el-button>
                <!--                <el-button link type="primary" size="small">试听</el-button>-->
              </template>
            </el-table-column>
          </el-table>
        </div>
        <div class="bottom" v-if="searchCache">
          <el-pagination v-model:current-page="music_current_page" @update:current-page="page_change" background
            class="tab-split" :page-size="30" layout="prev, pager, next" :total="parseInt(searchCache.page.size + '')" />
          <div class="tips">
            搜索到{{ searchCache.page.size }}条数据,当前第{{
              searchCache.page.cur
            }}页
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
@media screen and (max-width: 550px) {
  .content {
    min-width: auto !important;
    position: relative;
  }

  .head-section {
    z-index: 1;
    position: absolute !important;
    top: 0;
    left: 0;
    right: 0;
    border-bottom: solid 1px var(--qiuchen-text-15);
    margin: 0 !important;
    backdrop-filter: blur(10px);

    .top-tip {
      height: 45px;
      // background-color: #fff;
      margin: 10px 0;
      display: flex;
      align-items: center;
      font-size: 30px !important;
    }

    .area-top {
      width: calc(100% - 20px);
    }

    .options {
      flex-direction: column;
      align-items: start;
    }
  }

  .tips {
    display: none;
  }
}

.content {
  height: 100%;
  width: 100%;
  min-width: 400px;
  display: flex;
  flex-direction: column;
}

.options {
  display: flex;
  align-items: center;
  margin: 10px 0 0 0;
}

.area-action {
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 10px 0;
}

.head-section {
  margin: 10px 0;
  display: flex;

  flex-direction: column;
  align-items: center;
  position: relative;

  .input-with-select {}

  .area-top {
    display: flex;
    flex-direction: column;
    align-items: center;
  }
}

.history {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;

  .union {
    margin: 0 10px;
    display: inline-flex;
    align-items: center;
    font-size: 13px;
  }

  .h-list {
    flex: 1;
    overflow: scroll;
    padding-left: 10px;
    padding-top: 10px;

    .search-tag {
      display: inline-flex;
      font-size: 14px;
      height: 28px;
      padding: 0 20px;
      line-height: 28px;
      border-radius: 5px;
      cursor: pointer;
      transition: all 0.2s;
      box-shadow: 0 0 3px var(--qiuchen-text);
      margin-right: 10px;
      margin-bottom: 10px;

      &:hover {
        box-shadow: 0 0 5px var(--qiuchen-hover-text);
      }
    }
  }

  .clear-all-history {
    position: absolute;
    bottom: 10px;
    right: 10px;
    background-color: var(--qiuchen-normal-white);
    border-radius: 100%;
    display: flex;
    width: 45px;
    height: 45px;
    align-items: center;
    justify-content: center;
    box-shadow: 0 0 5px var(--qiuchen-hover-text);
    cursor: pointer;
    transition: all 0.2s;

    &:hover {
      box-shadow: 0 0 5px rgba($color: #000000, $alpha: 0.5);
    }
  }
}

.search-list-a {
  //background-color: red;
  display: flex;
  flex-direction: column;
  height: 100%;

  .container {
    overflow: hidden;

    .my-tb {
      height: 100%;

      .title-tip {
        display: flex;
        flex-direction: row;
        align-items: center;

        .flac-tip {
          font-size: 12px;
          color: #ffb703;
          border: #ffb703 1px solid;
          line-height: normal;
          margin-right: 8px;
          padding: 0 4px;
          border-radius: 4px;
        }
      }
    }
  }

  .bottom {
    display: flex;
    justify-content: center;
    margin: 10px 0;
    position: relative;
    width: 100%;

    .tips {
      position: absolute;
      left: 10px;
      top: 50%;
      transform: translateY(-50%);
    }
  }
}

.search-list {
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}
</style>
