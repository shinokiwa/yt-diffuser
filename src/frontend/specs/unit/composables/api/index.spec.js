/**
 * api.jsのテスト
 */
import { test, expect, it } from 'vitest'
import { useApi } from '@/composables/api'

test('テスト項目がないので暫定', () => {

    it('apiを取得できる', () => {
        const { api } = useApi()
        expect(api).not.toBe(null)
    })
})
