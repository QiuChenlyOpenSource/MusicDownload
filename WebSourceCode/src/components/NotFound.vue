<template>
  <div class="error">
    <h1>404 - 没有找到你想要的页面。</h1>
    <h3>{{ route.fullPath }}</h3>
    <router-link to="/">-> Go Home</router-link>
  </div>
</template>

<script setup lang="ts">
import { useRoute } from "vue-router";

let route = useRoute();
</script>

<style lang="scss" scoped>
.error {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100%;
}
</style>
