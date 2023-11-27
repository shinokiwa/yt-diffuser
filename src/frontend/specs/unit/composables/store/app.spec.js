// app.js のテスト
import { describe, it, expect, vi } from 'vitest'

import { useAppStore } from '@/composables/store/app'

describe('アプリケーションの状態管理', () => {
        
        const { readyState, ready} = useAppStore()

        it ('初期状態はfalse。', () => {
            expect(readyState.value).toBe(false)
        })

        it ('readyを実行するとローディング完了（true）になる。', () => {
            ready()
            expect(readyState.value).toBe(true)
        })
    
})