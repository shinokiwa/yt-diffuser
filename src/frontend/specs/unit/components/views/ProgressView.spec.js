/**
 * ProgressView.vue のテスト
 */
import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'

import ProgressView from '@/components/views/common/ProgressView.vue'


describe('ProgressView 進捗表示', async () => {
    it ("今のところ何もなし", async ()=> {
        expect(true).toBe(true)
    })
})