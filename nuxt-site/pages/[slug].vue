<template>
  <section v-if="page">
    <h1>{{ page.title_en }}</h1>
    <h2>{{ page.title_zh }}</h2>
    <p>{{ page.summary_en }}</p>
    <p>{{ page.summary_zh }}</p>
  </section>
  <section v-else>
    <h1>Not Found</h1>
  </section>
</template>

<script setup lang="ts">
const route = useRoute();
const { getPage } = useContent();
const page = getPage(String(route.params.slug || ""));
</script>
