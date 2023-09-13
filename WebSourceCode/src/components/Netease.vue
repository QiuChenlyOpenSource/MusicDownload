<!--
  - # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
  - # @作者         : 秋城落叶(QiuChenly)
  - # @邮件         : qiuchenly@outlook.com
  - # @文件         : 项目 [qqmusic] - Netease.vue
  - # @修改时间    : 2023-03-20 02:08:45
  - # @上次修改    : 2023/3/20 上午2:08
  -->

<script lang="ts" setup>
import { onMounted, onUnmounted, ref, computed, watch } from "vue";
import { ref2, SystemStore } from "@/store/SystemStore";
import { Api } from "@/utils/Http";
import QrcodeVue from "qrcode.vue";
import UserInfo from "@/component/UserInfo.vue";
import {
  NeteasePlayListSongsList,
  Privileges,
} from "@/utils/type/NetEasePlayListSong";
import { timestampToTime } from "@/utils/Utils";
import { MusicPlayList2List } from "@/utils/type/NeteaseMusicPlayList";
import { ElNotification } from "element-plus";
import MdiCloudCheckOutline from "~icons/mdi/cloud-check-outline";
import SearchMusic from "@/components/SearchMusic.vue";

const { basicStore } = SystemStore();
const user = ref2(basicStore);
const tips = ref("");
const unikey = ref("");
const page = ref(1);
const pageSize = ref(50);
const userPlaylistFetch = ref<Array<NeteasePlayListSongsList>>();

const head = ref<HTMLDivElement>();
const paddingHeadHeight = ref(0);

// import { banner, lyric } from '../Netease'

// const testNetease = () => {
//   banner({ type: 0 }).then((res) => {
//     console.log(res)
//   })
//   lyric({
//     id: '33894312',
//   }).then((res) => {
//     console.log(res)
//   })
// }

const UserFunction = {
  switchLoginQRCode() {
    Api.getNeteaseQRCode().then((r) => {
      unikey.value = r.qrcode.uniKey;
      this.checkLoginState();
    });
  },
  checkLoginState() {
    waitScanInterval = setInterval(async () => {
      let res = await Api.checkESState(unikey.value);
      switch (res.code) {
        case 800:
          tips.value = "验证码过期，自动切换中...";
          UserFunction.switchLoginQRCode();
          clearInterval(waitScanInterval);
          break;
        case 801:
          //等待扫码
          tips.value = "等待用户扫码";
          break;
        case 802:
          //等待确认
          tips.value = "等待确认";
          break;
        case 803:
          clearInterval(waitScanInterval);
          //登录成功
          tips.value = "登录成功";
          basicStore.netease.isLogin = true;
          basicStore.netease.token = res.cookie;
          this.getUserInfo().then((r) => UserFunction.fetchUserPlaylist());
          break;
      }
    }, 2000);
  },
  getUserInfo() {
    return Api.getNetEaseUserInfo().then((r) => {
      basicStore.netease.user = r;
    });
  },
  async initAnonimous() {
    let res = await Api.initAnonimous();
    basicStore.netease.anonimousCookie = res.cookie;
  },
  setUserCookie(ck: string) {
    return Api.setESCookie({
      cookie: ck,
    });
  },
  fetchUserPlaylist() {
    let uid = basicStore.netease.user.profile.userId;
    return Api.getUserPlaylist(uid + "").then((r) => {
      playlist.value = r.list;
      let pid = r.list[0].id;
      totalSize.value = r.list[0].trackCount;
      selectPlaylist.value = pid;

      mPlaylistDropdown.value = playlist.value.map((v) => ({
        value: v,
        label: v.name,
      }));
      return this.fetchPlayListMusic(pid + "");
    });
  },
  fetchPlayListMusic(pid: string) {
    return Api.getMusicListByPlaylistID(pid, page.value, pageSize.value).then(
      (r) => {
        if (r === undefined) return;
        if (r.code === 20001) {
          return;
        }
        userPlaylistFetch.value = r.list;
      }
    );
  },
};

/**
 * 用户扫码监听
 */
let waitScanInterval: any = null;

onMounted(() => {
  if (!basicStore.netease.isLogin) {
    UserFunction.initAnonimous().then((r) => {
      UserFunction.switchLoginQRCode();
    });
  } else {
    let ck = basicStore.netease.token;
    UserFunction.setUserCookie(ck).then((r) => {
      UserFunction.getUserInfo().then((r) => UserFunction.fetchUserPlaylist());
    });
  }
  paddingHeadHeight.value = head.value?.offsetHeight! + head.value?.offsetTop!;
  // testNetease();
});

onUnmounted(() => {
  clearInterval(waitScanInterval);
});

const selectPlaylist = ref();
const totalSize = ref(0);
const playlist = ref<Array<MusicPlayList2List>>();

const page_change = (v: number) => {
  page.value = v;
  UserFunction.fetchPlayListMusic(selectPlaylist.value);
};

const handleDown = (music: NeteasePlayListSongsList) => {
  Api.postDownload(music, {
    ...basicStore.config,
    platform: "wyy",
  }).then((r) => {
    if (r.code === 200) {
      ElNotification({
        title: "成功",
        message: "成功提交任务: " + music.author_simple + " - " + music.title,
        type: "success",
      });
    }
  });
};

const logout = () => {
  Api.esLogout().then((r) => {
    basicStore.netease.isLogin = false;
    basicStore.netease.token = "";
    UserFunction.initAnonimous().then((r) => {
      UserFunction.switchLoginQRCode();
    });
  });
};

const mPlaylistDropdown = ref<
  Array<{
    value: MusicPlayList2List;
    label: string;
  }>
>([]);

const loadUserPlaylist = (currentSelectItemIndex: number) => {
  console.log(currentSelectItemIndex);
  for (let i of mPlaylistDropdown.value) {
    if (i.value.id === currentSelectItemIndex) {
      // select value
      totalSize.value = i.value.trackCount;
    }
  }
  page_change(1);
};

const getFeeType = (row: NeteasePlayListSongsList) => {
  let tip = "未知";
  let res = tb6V(row.privileges);
  if (res === 100) return "暂无版权";
  switch (row.fee) {
    case 0:
      tip = "免费歌曲";
      break;
    case 1:
      tip = "会员播放";
      break;
    case 4:
      tip = "购买专辑";
      break;
    case 8:
      tip = "会员下载";
      break;
    default:
      tip = "未知类型" + row.fee;
      break;
  }
  return tip;
};

/**
 * 好像是检查是否为灰色歌曲的 逆向出来的函数
 * @param eD1x
 * @param action
 */
const tb6V = function (eD1x: Privileges, action: string = "") {
  if (eD1x) {
    if (action === "download") {
      return 0;
    }
    if (eD1x.pl <= 0 && (eD1x.fee > 63 || eD1x.flag > 4095)) {
      return 1e4;
    }
    if (
      action == "download" &&
      eD1x.dl <= 0 &&
      (eD1x.fee > 63 || eD1x.flag > 4095)
    ) {
      return 10001;
    }
    if (eD1x.st != null && eD1x.st < 0) {
      return 100; //由于版权保护，您所在的地区暂时无法使用。
    }
    if (eD1x.fee > 0 && eD1x.fee !== 8 && eD1x.payed === 0 && eD1x.pl <= 0)
      return 10; //唱片公司要求，当前歌曲须付费使用。
    if (eD1x.fee === 16 || (eD1x.fee === 4 && eD1x.flag & 2048)) return 11; //版权方要求，该歌曲须下载后播放
    if ((eD1x.fee === 0 || eD1x.payed) && eD1x.pl > 0 && eD1x.dl === 0)
      return 1e3;
    if (eD1x.pl === 0 && eD1x.dl === 0) return 100; //由于版权保护，您所在的地区暂时无法使用。
    return 0;
  } else {
    // var eG1x = bi0x.status != null ? bi0x.status : bi0x.st != null ? bi0x.st : 0;
    // if (bi0x.status >= 0)
    //   return 0;
    // if (bi0x.fee > 0)
    //   return 10;
    // return 100
    return -1;
  }
};

const matchMusic = ref(false);
const waitMatchMusic = ref<NeteasePlayListSongsList>(
  {} as NeteasePlayListSongsList
);
const willSearchString = ref("");
const handleMatch = (song: NeteasePlayListSongsList) => {
  waitMatchMusic.value = song;
  matchMusic.value = true;
  willSearchString.value =
    song.author_simple + " " + song.title + " " + song.album;
};
</script>

<template>
  <div class="content">
    <el-dialog class="dialog-attr" destroy-on-close align-center width="90%" v-model="matchMusic"
      :title="'查找歌曲 - ' + waitMatchMusic.title">
      <search-music :search="willSearchString" />
    </el-dialog>
    <div ref="head" class="head">
      网易云 -
      {{
        user.netease.value.isLogin
        ? user.netease.value.user.profile.nickname
        : "请登录"
      }}
    </div>
    <div class="areas" :style="{
          height: 'calc(100vh - ' + paddingHeadHeight + 'px)',
        }">
      <div v-if="!user.netease.value.isLogin" class="no-login">
        <div>{{ tips }}</div>
        <qrcode-vue :value="'http://music.163.com/login?codekey=' + unikey" :size="200" level="H"></qrcode-vue>
      </div>
      <div v-else class="login">
        <UserInfo :user-info="user.netease.value.user" />
        <div class="list-content">
          <el-select-v2 filterable class="playlist" v-model="selectPlaylist" value-key="value.id"
            :options="mPlaylistDropdown" placeholder="选择一个歌单" @change="loadUserPlaylist" size="large">
            <template #default="{ item }">
              <div class="select-list">
                <el-avatar size="small" class="list-img" :src="item.value.coverImgUrl" />
                <div class="list-right">
                  <span class="list-name">{{ item.value.name }}</span>
                  <span class="list-size">{{ item.value.trackCount }}首</span>
                </div>
              </div>
            </template>
          </el-select-v2>
          <span class="search-hint">结果列表[搜索到{{ totalSize }}条数据,当前第{{ page }}页]</span>
          <div @click="logout">退出登录</div>
          <el-table class="my-tb" :data="userPlaylistFetch" style="width: 100%; z-index: 0">
            <el-table-column :formatter="(row: NeteasePlayListSongsList) => {
              return timestampToTime(row.publishTime).split(' ')[0]
            }
              " prop="publishTime" label="发表时间" width="120" />
            <el-table-column :show-overflow-tooltip="true" prop="docid" label="版权" width="100">
              <template #default="scope">
                <div class="title-tip">
                  <div class="fee-tip" :class="{
                    'vip-tip': scope.row.fee === 1 || scope.row.fee === 4,
                    'no-ip-tip': tb6V(scope.row.privileges) === 100,
                    'vip-down': scope.row.fee === 8,
                  }">
                    {{ getFeeType(scope.row) }}
                  </div>
                </div>
              </template>
            </el-table-column>
            <el-table-column :show-overflow-tooltip="true" prop="title" label="歌曲名" min-width="300">
              <template #default="scope">
                <div class="title-tip">
                  <div class="flac-tip" v-if="scope.row.extra === 'flac'">
                    无损
                  </div>
                  <div class="name">{{ scope.row.title }}</div>
                  <MdiCloudCheckOutline v-if="scope.row.cloud" style="margin-left: 10px" />
                </div>
              </template>
            </el-table-column>
            <el-table-column :show-overflow-tooltip="true" :formatter="(row: NeteasePlayListSongsList) => {
              return row.author.map(v => v.name).join(' / ')
            }" prop="singer.name" label="艺术家" width="200" />
            <el-table-column :show-overflow-tooltip="true" prop="album" label="专辑" width="200" />
            <el-table-column fixed="right" label="操作">
              <template #default="scope">
                <el-button :type="tb6V(scope.row.privileges) === 100 ? 'info' : 'primary'
                  " size="small" @click="
    tb6V(scope.row.privileges) === 100
      ? null
      : handleDown(scope.row)
    ">下载
                </el-button>
                <el-button v-if="tb6V(scope.row.privileges) === 100" type="warning" size="small"
                  @click="handleMatch(scope.row)">在线匹配
                </el-button>
                <!--                <el-button link type="primary" size="small">试听</el-button>-->
              </template>
            </el-table-column>
          </el-table>
          <el-pagination v-model:current-page="page" @update:current-page="page_change" background class="tab-split"
            :page-size="pageSize" layout="prev, pager, next" :total="totalSize" />
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  box-sizing: border-box;
}

.head {
  margin-left: 10px;
  padding-top: 10px;
  font-size: 2.5em;
  font-weight: bolder;
}

.title-tip {
  display: flex;
  flex-direction: row;
  align-items: center;

  .name {}

  .flac-tip {
    font-size: 12px;
    color: #ffb703;
    border: #ffb703 1px solid;
    line-height: normal;
    margin-right: 8px;
    padding: 0 4px;
    border-radius: 4px;
  }

  .fee-tip {
    padding: 4px 10px;
    color: #fff;
    background-color: #a480cf;
    font-size: 12px;
    line-height: normal;
    margin-right: 8px;
    border-radius: 4px;
    font-weight: bolder;
  }

  .vip-down {
    background-color: #788bff;
  }

  .vip-tip {
    background-color: #d00000;
  }

  .no-ip-tip {
    background-color: #a9aca9;
  }
}

.login {
  height: calc(100%);
  display: flex;
  flex-direction: column;

  .list-content {
    flex: 1; //全部撑开
    display: flex;
    flex-direction: column;
    overflow: hidden;
    padding: 0 0 10px 0;

    .playlist {
      margin: 0 10px;
    }

    .my-tb {
      height: 100%;
    }

    .search-hint {
      font-size: 14px;
      color: var(--qiuchen-normal-black);
      margin: 10px 0 0 10px;
    }

    .tab-split {
      margin-top: 10px;
      display: flex;
      justify-content: center;
    }
  }
}

.no-login {}

.dialog-attr {
  height: 80vh;
  overflow: hidden;

  :deep(.el-dialog__body) {
    padding: 0 !important;
  }
}

.select-list {
  display: flex;
  flex-direction: row;
  height: auto;
  align-items: center;

  .list-img {}

  .list-right {
    margin-left: 10px;
    display: flex;
    flex-direction: column;

    span {
      padding: 0;
      margin: 0;
      height: auto;
      line-height: normal;
    }
  }

  .list-name {
    color: var(--qiuchen-normal-black);
  }

  .list-size {
    font-size: 6pt;
  }

  .list-img {}
}
</style>
