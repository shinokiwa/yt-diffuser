import { fileURLToPath, URL } from "node:url";

import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig({
    plugins: [vue()],
    resolve: {
        alias: {
            "@": fileURLToPath(new URL("./src", import.meta.url)),
            "@mocks": fileURLToPath(new URL("./specs/mock", import.meta.url)),
        },
    },
    server: {
        host: true,
        // Dockerのバインドマウントでは監視が働かないっぽいのでプーリングを使う
        watch: {
            usePolling: true,
            interval: 1000,
        },
    },
    test: {
        // jest ライクなグローバルテスト API を有効化
        globals: true,
        // happy-dom で DOM をシミュレーション
        environment: "happy-dom",
        include: ["specs/unit/**/*.spec.js"],
        coverage: {
            providers: ["v8"],
            all: true,
            reporter: ["text", "html"],
            exclude: ["specs/**/*"],
        }
    },
});
