export default defineNuxtConfig({
  compatibilityDate: "2026-03-31",
  devtools: { enabled: true },
  app: {
    head: {
      link: [
        { rel: "icon", type: "image/png", sizes: "32x32", href: "/favicon.png" },
        { rel: "icon", type: "image/png", sizes: "192x192", href: "/icon-192.png" },
        { rel: "apple-touch-icon", sizes: "180x180", href: "/apple-touch-icon.png" },
      ],
    },
  },
});
