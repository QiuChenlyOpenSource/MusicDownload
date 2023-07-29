<script lang="ts" setup>
import { Api } from '../utils/Http';
import { onMounted, ref } from 'vue';

const isSelect = ref(0)

onMounted(() => {
  Api.getLocalFiles().then(r => {
    console.log(r);
  })
})

</script>

<template>
  <div class="content">
    <div class="meta-title">下载管理</div>
    <div class="view-options">
      <div :class="{
        'isCheckedStyle': isSelect == 0
      }">按文件夹</div>
      <div :class="{
        'isCheckedStyle': isSelect == 1
      }">按专辑</div>
      <div :class="{
        'isCheckedStyle': isSelect == 2
      }">按歌手</div>
      <div :class="{
        'isCheckedStyle': isSelect == 3
      }">不分类</div>
    </div>
    <div class="songer-list">
      <div>暂无数据。</div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.content {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  flex-shrink: 1;

  .songer-list {
    flex: 1;
    background-color: rgba($color: #000000, $alpha: .1);
    margin: 10px;
    padding: 5px;
    box-sizing: border-box;
  }

  .meta-title {
    font-size: 30px;
    height: 45px;
    margin: 10px;
  }

  .view-options {
    margin: 0 10px;
    display: flex;
    box-shadow: 0 2px 10px rgba($color: #000000, $alpha: .2);
    border-radius: 8px;
    max-width: 600px;
    min-width: 400px;

    .isCheckedStyle {
      color: white;
      background-color: rgba($color: #000, $alpha: .85);
    }

    div {
      flex: 1;
      display: flex;
      justify-content: center;
      align-items: center;
      height: 35px;
      color: black;
      background-color: rgba($color: #fff, $alpha: .65);
      font-size: 13px;
      cursor: pointer;
      transition: all .2s;
      border-right: solid 0.5px rgba($color: #000000, $alpha: .1);

      &:hover {
        color: white;
        background-color: rgba($color: #000, $alpha: .85);
      }

      &:nth-of-type(1) {
        border-radius: 8px 0 0 8px;
      }

      &:nth-last-of-type(1) {
        border-radius: 0 8px 8px 0;
      }
    }
  }
}
</style>
