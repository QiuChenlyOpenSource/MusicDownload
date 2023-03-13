<!--
  - # Copyright (c) 2023. 秋城落叶, Inc. All Rights Reserved
  - # @作者         : 秋城落叶(QiuChenly)
  - # @邮件         : 1925374620@qq.com
  - # @文件         : 项目 [qqmusic] - Netease.vue
  - # @修改时间    : 2023-03-14 12:27:54
  - # @上次修改    : 2023/3/14 上午12:27
  -->

<script lang="ts" setup>
import {onMounted, onUnmounted, ref, computed, watch} from "vue";
import {ref2, SystemStore} from "@/store/SystemStore";
import {Api} from "@/utils/Http";
import QrcodeVue from 'qrcode.vue';
import UserInfo from "@/component/UserInfo.vue";
import {NeteasePlayListSongsList} from "@/utils/type/NetEasePlayListSong";
import {timestampToTime} from "@/utils/Utils";
import {MusicPlayList2List} from "@/utils/type/NeteaseMusicPlayList";
import {ElNotification} from "element-plus";

const {basicStore} = SystemStore()
const user = ref2(basicStore)
const tips = ref("")
const unikey = ref("")
const page = ref(1)
const pageSize = ref(50)
const userPlaylistFetch = ref<Array<NeteasePlayListSongsList>>()

const head = ref<HTMLDivElement>()
const paddingHeadHeight = ref(0)

const UserFunction = {
  switchLoginQRCode() {
    Api.getNeteaseQRCode().then(r => {
      unikey.value = r.qrcode.uniKey
      this.checkLoginState()
    })
  },
  checkLoginState() {
    waitScanInterval = setInterval(async () => {
      let res = await Api.checkESState(unikey.value)
      switch (res.code) {
        case 800:
          tips.value = "验证码过期，自动切换中..."
          UserFunction.switchLoginQRCode()
          clearInterval(waitScanInterval)
          break
        case 801:
          //等待扫码
          tips.value = "等待用户扫码"
          break;
        case 802:
          //等待确认
          tips.value = "等待确认"
          break;
        case 803:
          clearInterval(waitScanInterval)
          //登录成功
          tips.value = "登录成功"
          basicStore.netease.isLogin = true
          basicStore.netease.token = res.cookie
          this.getUserInfo();
          break;
      }
    }, 2000)
  },
  getUserInfo() {
    return Api.getNetEaseUserInfo().then(r => {
      basicStore.netease.user = r
    })
  },
  async initAnonimous() {
    let res = await Api.initAnonimous()
    basicStore.netease.anonimousCookie = res.cookie
  },
  setUserCookie(ck: string) {
    return Api.setESCookie({
      cookie: ck
    })
  },
  fetchUserPlaylist() {
    let uid = basicStore.netease.user.profile.userId
    return Api.getUserPlaylist(uid + '').then(r => {
      playlist.value = r.list
      let pid = r.list[0].id
      totalSize.value = r.list[0].trackCount
      selectPlaylist.value = pid

      mPlaylistDropdown.value = playlist.value.map(v => ({
        value: v,
        label: v.name,
      }))
      return this.fetchPlayListMusic(pid + '')
    })
  },
  fetchPlayListMusic(pid: string) {
    return Api.getMusicListByPlaylistID(pid, page.value, pageSize.value).then(r => {
      if (r === undefined) return
      if (r.code === 20001) {
        return
      }
      userPlaylistFetch.value = r.list
    })
  },
}

/**
 * 用户扫码监听
 */
let waitScanInterval = -1

onMounted(() => {
  if (!basicStore.netease.isLogin) {
    UserFunction.initAnonimous().then(r => {
      UserFunction.switchLoginQRCode()
    })
  } else {
    let ck = basicStore.netease.token;
    UserFunction.setUserCookie(ck).then(r => {
      UserFunction.getUserInfo().then(r => UserFunction.fetchUserPlaylist())
    });
  }
  paddingHeadHeight.value = head.value?.offsetHeight! + head.value?.offsetTop!
})

onUnmounted(() => {
  clearInterval(waitScanInterval)
})

const selectPlaylist = ref()
const totalSize = ref(0)
const playlist = ref<Array<MusicPlayList2List>>()

const page_change = (v: number) => {
  page.value = v
  UserFunction.fetchPlayListMusic(selectPlaylist.value)
}

const handleDown = (music: NeteasePlayListSongsList) => {
  Api.postDownload(music, {
    ...basicStore.config,
    platform: 'wyy'
  }).then(r => {
    if (r.code === 200) {
      ElNotification({
        title: '成功',
        message: '成功提交任务: ' + music.author_simple + " - " + music.title,
        type: 'success',
      })
    }
  })
}

const mPlaylistDropdown = ref<Array<{
  value: MusicPlayList2List,
  label: string,
}>>([])

const loadUserPlaylist = (currentSelectItemIndex: number) => {
  console.log(currentSelectItemIndex)
  for (let i of mPlaylistDropdown.value) {
    if (i.value.id === currentSelectItemIndex) {
      // select value
      totalSize.value = i.value.trackCount
    }
  }
  page_change(1)
}
</script>

<template>
  <div class="content">
    <div ref="head" class="head">网易云 - {{
        user.netease.value.isLogin ? user.netease.value.user.profile.nickname : "请登录"
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
        <UserInfo :user-info="user.netease.value.user"/>
        <div class="list-content">
          <el-select-v2
              filterable
              class="playlist"
              v-model="selectPlaylist"
              value-key="value.id"
              :options="mPlaylistDropdown"
              placeholder="选择一个歌单"
              @change="loadUserPlaylist"
              size="large"
          >
            <template #default="{ item }">
              <div class="select-list">
                <el-avatar size="small" class="list-img" :src="item.value.coverImgUrl"/>
                <div class="list-right">
                  <span class="list-name">{{ item.value.name }}</span>
                  <span class="list-size">{{ item.value.trackCount }}首</span>
                </div>
              </div>
            </template>
          </el-select-v2>
          <span class="search-hint">结果列表[搜索到{{ totalSize }}条数据,当前第{{
              page
            }}页]</span>
          <el-table
              class="my-tb"
              :data="userPlaylistFetch"
              style="width: 100%; z-index: 0"
          >
            <el-table-column
                :formatter="
                (row:NeteasePlayListSongsList) => {
                  return timestampToTime(row.publishTime).split(' ')[0]
                }
              "
                prop="publishTime"
                label="发表时间"
                width="120"
            />
            <el-table-column
                :show-overflow-tooltip="true"
                prop="title"
                label="歌曲名"
                min-width="300"
            />
            <el-table-column
                :show-overflow-tooltip="true"
                :formatter="(row:NeteasePlayListSongsList) => {
                  return row.author.map(v=>v.name).join(' / ')
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
            <el-table-column fixed="right" label="操作" width="120">
              <template #default="scope">
                <el-button link type="primary" size="small" @click="handleDown(scope.row)"
                >下载
                </el-button>
                <!--                <el-button link type="primary" size="small">试听</el-button>-->
              </template>
            </el-table-column>
          </el-table>
          <el-pagination
              v-model:current-page="page"
              @update:current-page="page_change"
              background
              class="tab-split"
              :page-size="pageSize"
              layout="prev, pager, next"
              :total="totalSize"
          />
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
      color: var(--qiuchen-normal-white);
      margin: 10px 0 0 10px;
    }

    .tab-split {
      margin-top: 10px;
      display: flex;
      justify-content: center;
    }
  }
}

.no-login {

}

.select-list {
  display: flex;
  flex-direction: row;
  height: auto;
  align-items: center;

  .list-img {

  }

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

  .list-img {

  }

}
</style>
