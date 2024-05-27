import { fileURLToPath } from 'node:url'
import { mergeConfig, defineConfig, configDefaults } from 'vitest/config'
import viteConfig from './vite.config'

export default mergeConfig(
  viteConfig,
  defineConfig({
    test: {
      environment: 'jsdom',

      // jest ライクなグローバルテスト API を有効化
      globals: true,

      root: fileURLToPath(new URL('./', import.meta.url)),
      include: ['src/**/__specs__/*.spec.js'],
      exclude: [...configDefaults.exclude, 'e2e/**'],

      coverage: {
        providers: ['v8'],
        all: true,
        reporter: ['text', 'html']
      }
    }
  })
)
