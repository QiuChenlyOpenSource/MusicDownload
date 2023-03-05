<script lang="ts" setup>
import {Search} from "@element-plus/icons-vue";
import {ref, onMounted, watch} from "vue";
import {ref2, SystemStore} from "@/store/SystemStore";
import {Api} from "@/utils/Http";
import {
  SearchMusicResult,
  SearchMusicResultSingle,
} from "@/utils/type/BasicType";
import {DividerProps} from "element-plus";

const platform = ref("QQ音乐");
const {basicStore} = SystemStore();
const refbasicStore = ref2(basicStore);
const music_current_page = ref(1);
const headRef = ref();

watch(refbasicStore.lastSearch, (now, old) => {
  if (now.length === 0) {
    searchCache.value = undefined;
    music_current_page.value = 1;
  }
});

function page_change() {
  search();
}

const searchCache = ref<SearchMusicResult>();

const getMusicSinger = (music: SearchMusicResultSingle) => music.singer;
// .map(v => {
// return v.name
// }).join(music.singer.length === 1 ? '' : "&")

/**
 * 检查这首曲子是否不符合过滤标准 true表示曲子可以给用户显示 false反之
 * @param singleMusic
 */
const filterList = (singleMusic: SearchMusicResultSingle) => {
  if (basicStore.config.ignoreNoAlbumSongs) {
    return singleMusic.album !== "未分类专辑";
  }
  if (basicStore.config.onlyMatchSearchKey) {
    return getMusicSinger(singleMusic).indexOf(basicStore.lastSearch) !== -1;
  }
  return true;
};

const search = () => {
  if (
      basicStore.searchHistory.find(
          (v, i, array) => v === basicStore.lastSearch
      ) === undefined
  )
    basicStore.searchHistory.push(basicStore.lastSearch);
  Api.searchMusic(basicStore.lastSearch, music_current_page.value).then((r) => {
    let lst = [] as Array<SearchMusicResultSingle>;
    r.list.forEach((v) => {
      if (filterList(v)) lst.push(v);
    });
    r.list = lst;
    searchCache.value = r;
  });
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

const paddingHeadHeight = ref(0);
onMounted(() => {
  const h = headRef.value as HTMLDivElement;
  paddingHeadHeight.value = h.offsetTop + h.offsetHeight;
});

const handleDown = (data: SearchMusicResultSingle) => {
  console.log(data)
  Api.postDownload(data, {
    onlyMatchSearchKey: basicStore.config.onlyMatchSearchKey,
    ignoreNoAlbumSongs: basicStore.config.ignoreNoAlbumSongs,
    classificationMusicFile: basicStore.config.classificationMusicFile
  })
}
</script>

<template>
  <div class="content">
    <div ref="headRef" class="head-section">
      <h1>搜索</h1>
      <el-input
          v-model="basicStore.lastSearch"
          placeholder="请输入关键词搜索"
          class="input-with-select"
      >
        <template #prepend>
          <el-select
              v-model="platform"
              placeholder="请选择接口"
              style="width: 120px"
          >
            <el-option label="QQ音乐" value="1"/>
            <el-option label="网易云音乐" value="2"/>
            <el-option label="酷我音乐" value="3"/>
          </el-select>
        </template>
        <template #append>
          <el-button :icon="Search" @click="search"/>
        </template>
      </el-input>
      <div class="options">
        <el-checkbox
            v-model="basicStore.config.onlyMatchSearchKey"
            label="仅显示搜索的歌手歌曲"
        />
        <el-checkbox
            v-model="basicStore.config.ignoreNoAlbumSongs"
            label="屏蔽无所属专辑歌曲"
        />
        <!--        <el-checkbox v-model="classificationMusicFile" label="按照专辑名称分文件夹归档音乐歌曲文件"/>-->
        <!--        <el-checkbox v-model="checked3" label="Option 1"/>-->
      </div>
    </div>
    <div
        v-if="searchCache === undefined || basicStore.lastSearch.length === 0"
        class="history"
    >
      <div class="union">
        <i-system-uicons-undo-history/>
        <span style="margin-left: 4px">历史搜索</span>
      </div>
      <div class="h-list">
        <div
            v-for="ind in refbasicStore.searchHistory.value"
            @click="basicStore.lastSearch = ind"
            class="search-tag"
        >
          {{ ind }}
        </div>
      </div>
      <div
          v-if="basicStore.searchHistory.length > 0"
          class="clear-all-history"
          @click="basicStore.searchHistory = []"
      >
        <i-icon-park-twotone-clear-format/>
      </div>
    </div>
    <div
        v-else
        class="search-list"
        :style="{
        height: 'calc(100% - ' + paddingHeadHeight + 'px)',
      }"
    >
      <div
          style="margin: 10px"
          v-if="searchCache === undefined || searchCache.list.length === 0"
          class="error-load"
      >
        <span>{{
            searchCache.page.size > 0
                ? "过滤后没有发现符合条件的数据。"
                : "服务器请求搜索结果失败,请重试。"
          }}</span>
      </div>
      <div class="search-list-a" v-else>
        <span class="search-hint"
        >结果列表[搜索到{{ searchCache.page.size }}条数据,当前第{{
            searchCache.page.cur
          }}页]</span
        >
        <div class="container">
          <el-table
              class="my-tb"
              :data="searchCache.list"
              style="width: 100%; z-index: 0"
          >
            <el-table-column
                :formatter="
                (row:SearchMusicResultSingle) => {
                  return row.time_publish === ''
                    ? '1970-01-01'
                    : row.time_publish;
                }
              "
                prop="time_public"
                label="发表时间"
                width="120"
            />
            <el-table-column
                show-overflow-tooltip="true"
                prop="title"
                label="歌曲名"
                min-width="300"
            />
            <el-table-column
                show-overflow-tooltip="true"
                :formatter="getSinger"
                prop="singer.name"
                label="艺术家"
                width="200"
            />
            <el-table-column
                show-overflow-tooltip="true"
                prop="album"
                label="专辑"
                width="200"
            />
            <el-table-column
                show-overflow-tooltip="true"
                prop="notice"
                label="品质"
                width="180"
            />
            <el-table-column fixed="right" label="操作" width="120">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="handleDown(scope.row)"
                >下载
                </el-button>
                <el-button link type="primary" size="small">试听</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
        <el-pagination
            v-model:current-page="music_current_page"
            @update:current-page="page_change"
            background
            class="tab-split"
            :page-size="30"
            layout="prev, pager, next"
            :total="searchCache.page.size"
        />
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content {
  height: 100%;
  width: 100%;
  min-width: 400px;
  display: flex;
  flex-direction: column;
}

.head-section {
  margin: 10px 0;
  display: flex;

  flex-direction: column;
  align-items: center;

  .input-with-select {
    max-width: 600px;
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

  .search-hint {
    margin: 10px;
    font-size: 15px;
    color: var(--el-checkbox-text-color);
  }

  .container {
    overflow: hidden;

    .my-tb {
      height: 100%;
    }
  }

  .tab-split {
    display: flex;
    justify-content: center;
    margin: 10px 0;
  }
}

.search-list {
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
}


</style>
