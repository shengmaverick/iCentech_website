<template>
  <div>
    <header style="border-bottom: 1px solid #e5e7eb; padding: 14px 20px;">
      <strong style="margin-right: 16px;">iCentech</strong>
      <NuxtLink
        v-for="item in navigation"
        :key="item.key"
        :to="item.slug ? `/${item.slug}` : '/'"
        style="margin-right: 10px; color: #334155;"
      >
        {{ item.label_en }} / {{ item.label_zh }}
      </NuxtLink>
    </header>
    <main style="max-width: 900px; margin: 40px auto; padding: 0 16px;">
      <NuxtPage />
    </main>
  </div>
</template>

<script setup lang="ts">
const { navigation } = useContent();
</script>
