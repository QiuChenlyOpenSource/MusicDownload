<template>
  <div class="user-info">
    <el-avatar class="avatar" :size="100" :src="userInfo.profile.avatarUrl" />
    <div class="bg" :style="{
      background: 'no-repeat center/cover url(' + userInfo.profile.backgroundUrl + ')'
    }"></div>
    <div class="info-area">
      <div>UID {{ userInfo.profile.userId }}</div>
      <div class="tag">
        {{
          userInfo.profile.vipType === 0 ? "非会员" : "会员" + userInfo.profile.viptypeVersion + "级别"
        }}
      </div>
      <div class="area">
        <div class="nickname">{{ userInfo.profile.nickname }}</div>
      </div>
      <div class="reg-time">注册时间 {{ timestampToTime(userInfo.profile.createTime) }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { NetEaseUserInfo } from "@/utils/type/UserInfoDetail";
import { timestampToTime } from "../utils/Utils";

defineProps<{
  userInfo: NetEaseUserInfo
}>()
</script>

<style lang="scss" scoped>
$shadow: 0 0 10px rgba(0, 0, 0, .4);

.user-info {
  margin: 50px 10px 10px 10px;
  min-height: 150px;
  min-width: 600px;
  backdrop-filter: blur(20px);
  position: relative;
  color: azure;
  padding: 10px 0;

  .bg {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: -1;
    border-radius: 8px;
    box-shadow: $shadow;
    overflow: hidden;

    &::before {
      content: '';
      //background-color: #000;
      width: 100%;
      height: 100%;
      display: block;
      backdrop-filter: blur(10px) brightness(60%);
    }
  }

  .avatar {
    position: absolute;
    left: 50%;
    top: -50px;
    transform: translateX(-50%);
    box-shadow: $shadow;
  }

  .info-area {
    width: 100%;
    height: calc(100% - 50px);
    margin-top: 50px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;

    .tag {
      display: inline-flex;
      border-radius: 4px;
      font-size: 6pt;
      align-items: center;
      padding: 2px 8px;
      margin-right: 8px;
      background-color: #c1121f;
      color: var(--qiuchen-normal-black);
    }

    .area {
      display: flex;
      flex-direction: column;


      .nickname {
        font-size: 35px;
      }
    }

    .reg-time {
      font-size: 14px;
      color: var(--qiuchen-normal-white);
    }
  }
}
</style>
