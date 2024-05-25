/**
 * composables/store/form.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'

import { useFormStore } from '@/composables/store/form'

describe('useFormStore フォームの状態を管理するストアコンポーザブル', () => {
    it('useFormStoreを呼び出すと、フォームの状態を管理するストアが返される。', () => {
        // ロジックは特に無いため、呼び出しのみテスト
        const form = useFormStore()
    })
})