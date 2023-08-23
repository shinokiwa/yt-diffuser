import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
            //"@/": `${__dirname}/src/`,
        },
    },
    server: {
        host: true,
        // Dockerのバインドマウントでは監視が働かないっぽいのでプーリングを使う
        watch: {
            usePolling: true,
        },
    },
    test: {
        // jest ライクなグローバルテスト API を有効化
        globals: true,
        // happy-dom で DOM をシミュレーション
        environment: "happy-dom",
        include: ["tests/unit/**/*.test.js"]
    },
});
