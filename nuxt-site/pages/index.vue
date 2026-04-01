<template>
  <section v-if="home">
    <h1>{{ home.title_en }}</h1>
    <h2>{{ home.title_zh }}</h2>
    <p>{{ home.summary_en }}</p>
    <p>{{ home.summary_zh }}</p>
  </section>
</template>

<script setup lang="ts">
const { getPage } = useContent();
const home = getPage("");
</script>
