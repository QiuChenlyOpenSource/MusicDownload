<script setup lang="ts">
import { ref } from "vue";
import { Api } from "@/utils/Http";

defineProps<{ msg: string }>();

const count = ref(0);

const clickEnv = () => {
  count.value++;
  Api.status().then((r) => {
    console.log(r);
  });
};
</script>

<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <el-button @click="clickEnv">count is {{ count }}</el-button>
    <p>
      Edit
      <code>components/HelloWorld.vue</code> to test HMR
    </p>
  </div>
</template>

<style scoped>
.card {
  display: flex;
  flex-direction: column;
  align-items: center;
}
</style>
