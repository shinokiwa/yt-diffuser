/**
 * status.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { useStatusStore } from '@/composables/store/status'

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

describe('useStatusStore ワーカープロセスのステータスを取得し保持するストアコンポーザブル', () => {

    it('useStatusを呼び出すとSSEに接続して、ステータスを取得できる。', () => {
        const { status } = useStatusStore()

        expect(mockEventSource).toHaveBeenCalledWith('/api/sse/status')
        expect(status.value).toEqual('')
    })

    it('SSEからステータスを受信すると、status.valueに値が入る。', () => {
        const { status } = useStatusStore()

        console.log(mockEventSource.mock.instances[0].onmessage)

        const event = {
            data: 'test'
        }

        mockEventSource.mock.instances[0].onmessage(event)

        expect(status.value).toEqual('test')
    })
})