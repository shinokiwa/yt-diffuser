/**
 * composables/api/index.jsのテスト
 */
import { describe, expect, it } from 'vitest'
import { useApi } from '@/composables/api'

describe('テスト項目がないので暫定', () => {

    it('暫定項目', () => {
        const { get } = useApi()
        expect(get).not.toBe(null)
    })
})
