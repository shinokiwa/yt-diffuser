/**
 * composables/api/generate/status.jsのテスト
 */
import { describe, it, expect, vi, afterEach } from 'vitest'

import { useToastStoreMock } from '@mocks/composables/store/toast.mock'
vi.mock('@/composables/store/toast', () => ({useToastStore: useToastStoreMock}))

import { useGenerateStatus } from '@/composables/api/generate/status'

// EventSourceのモックを作成
const mockEventSource = vi.fn(function() {
    this.addEventListener = vi.fn((event, listener) => {
      if (event === 'message') {
        this.onmessage = listener;  // onmessageリスナを保存
      }
    });
    this.removeEventListener = vi.fn();
    this.close = vi.fn();
});

// EventSourceのモックをグローバルオブジェクトに割り当て
global.EventSource = mockEventSource;

describe('useGenerateStatus ワーカープロセスのステータスを取得する', () => {

    it('useStatusを呼び出すとSSEに接続して、ステータスを取得できる。', () => {
        const { status } = useGenerateStatus()

        expect(mockEventSource).toHaveBeenCalledWith('/api/generate/status')
        expect(status.value).toEqual('')
    })

    it('SSEからステータスを受信すると、status.valueに値が入る。', () => {
        const { status } = useGenerateStatus()

        const event = {
            data: JSON.stringify({ status: 'exit' })
        }
        mockEventSource.mock.instances[0].onmessage(event)

        expect(status.value).toEqual('empty')
    })
})