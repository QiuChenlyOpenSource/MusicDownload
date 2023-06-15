<!--
  - # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
  - # @作者         : 秋城落叶(QiuChenly)
  - # @邮件         : qiuchenly@outlook.com
  - # @文件         : 项目 [qqmusic] - Cloud.vue
  - # @修改时间    : 2023-03-15 12:28:41
  - # @上次修改    : 2023/3/15 上午12:28
  -->

<script lang="ts" setup>
import { reactive, ref, watch, computed } from "vue";
import { Api } from "@/utils/Http";
import { CloudResponse, List } from "@/utils/type/CloudResponse";
import { timestampToTime } from "@/utils/Utils";
import { SearchMusicResultSingle } from "@/utils/type/BasicType";
import { SystemStore } from "@/store/SystemStore";
import { ElNotification } from "element-plus";

const lst = ref<CloudResponse>();
const modifyMusicInfo = ref(false);

const fetchAllSongs = () => {
  Api.getNeteaseCloud().then((r) => {
    lst.value = {} as CloudResponse;
    lst.value = r;
  });
};

const handleDel = (row: List) => {
  Api.delNeteaseCloud().then((r) => {});
  console.log(row);
};

const formLabelWidth = "140px";
const searchKey = ref("");
const filterText = ref("");
const musicID = ref();
const { basicStore } = SystemStore();

const searchLstCache = ref<SearchMusicResultSingle[]>();

watch(searchKey, (value, oldValue, onCleanup) => {
  console.log(value);
  Api.searchMusic(encodeURIComponent(value), 1, "wyy", 100).then((r) => {
    musicID.value = undefined;
    searchLstCache.value = r.list;
    console.log(searchLstCache.value);
  });
});

const tableLst = computed(() =>
  lst.value?.list.filter((data) => data.fileName.includes(filterText.value))
);

const getSongDesc = (item: SearchMusicResultSingle) => {
  return item.singer + " - " + item.title + " ｜ " + item.album;
};

let waitModifyData = ref<List>({} as List);
const handleModify = (row: List) => {
  waitModifyData.value = row;
  modifyMusicInfo.value = !modifyMusicInfo.value;
  searchKey.value =
    waitModifyData.value.songName + " " + waitModifyData.value.artist;
  console.log(row);
};

const submitModify = (asid: number) => {
  Api.bindSid2Asid({
    sid: waitModifyData.value.songId,
    asid: asid,
    uid: basicStore.netease.user.account.id,
  }).then((r) => {
    if (r.code === 200) {
      ElNotification({
        title: "成功",
        message: "修改信息成功。",
        type: "success",
      });
      modifyMusicInfo.value = !modifyMusicInfo.value;
    } else {
      ElNotification({
        title: "错误",
        message: r.message,
        type: "error",
      });
    }
  });
};

fetchAllSongs();
</script>

<template>
  <div class="content" v-if="lst">
    <h1>云盘歌曲纠错 {{ lst.hasMore ? "有更多" : "没有更多" }}</h1>
    <el-table class="my-tb" :data="tableLst" style="width: 100%; z-index: 0">
      <el-table-column
        :formatter="
                (row:List) => {
                  return timestampToTime(row.addTime).split(' ')[0]
                }
              "
        prop="publishTime"
        label="上传时间"
        width="120"
      />
      <el-table-column
        :show-overflow-tooltip="true"
        prop="songName"
        label="歌曲名"
        min-width="300"
      />
      <el-table-column
        :show-overflow-tooltip="true"
        :formatter="(row:List) => {
                  return row.artist
                }"
        prop="singer.name"
        label="艺术家"
        width="200"
      />
      <el-table-column
        :show-overflow-tooltip="true"
        prop="album"
        label="专辑"
        width="200"
      />
      <el-table-column fixed="right" min-width="100">
        <template #header>
          <el-input
            v-model="filterText"
            size="default"
            placeholder="输入过滤歌曲"
          />
        </template>
        <template #default="scope">
          <el-button
            type="primary"
            size="small"
            @click="handleModify(scope.row)"
            >修改
          </el-button>
          <el-button type="danger" size="small" @click="handleDel(scope.row)"
            >删除
          </el-button>
          <!--                <el-button link type="primary" size="small">试听</el-button>-->
        </template>
      </el-table-column>
    </el-table>
  </div>
  <el-dialog
    v-model="modifyMusicInfo"
    :title="'修改歌曲匹配信息 - ' + waitModifyData.fileName"
  >
    <el-form>
      <el-form-item label="当前歌曲识别信息" :label-width="formLabelWidth">
        <el-descriptions :title="waitModifyData.fileName" :column="3" border>
          <el-descriptions-item label="歌曲名" label-align="right" align="left"
            >{{ waitModifyData.songName }}
          </el-descriptions-item>
          <el-descriptions-item label="歌手" label-align="right" align="left"
            >{{ waitModifyData.artist }}
          </el-descriptions-item>
          <el-descriptions-item label="专辑" label-align="right" align="center"
            >{{ waitModifyData.album }}
          </el-descriptions-item>
          <el-descriptions-item label="文件名" label-align="right" align="left">
            <el-tag size="small">{{ waitModifyData.fileName }}</el-tag>
          </el-descriptions-item>
          <el-descriptions-item
            label="参考搜索词"
            label-align="right"
            align="left"
          >
            {{ waitModifyData.songName + " " + waitModifyData.artist }}
          </el-descriptions-item>
        </el-descriptions>
      </el-form-item>
      <el-form-item label="搜索歌曲名称" :label-width="formLabelWidth">
        <el-input v-model="searchKey" autocomplete="off" />
      </el-form-item>
      <el-form-item label="服务器结果" :label-width="formLabelWidth">
        <el-select v-model="musicID" placeholder="请选择一个搜索结果">
          <el-option
            v-for="inx in searchLstCache"
            :label="getSongDesc(inx)"
            :value="inx.musicid"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="指定歌曲ID" :label-width="formLabelWidth">
        <el-input v-model="musicID" autocomplete="off" />
      </el-form-item>
    </el-form>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="modifyMusicInfo = false">取消</el-button>
        <el-button type="danger" @click="submitModify(0)">取消匹配</el-button>
        <el-button type="primary" @click="submitModify(musicID)">
          确认匹配
        </el-button>
      </span>
    </template>
  </el-dialog>
</template>

<style lang="scss" scoped>
.content {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
}
</style>
