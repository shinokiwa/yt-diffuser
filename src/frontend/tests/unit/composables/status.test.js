/**
 * status.jsのテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { useStatus } from '@/composables/status'

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

describe('プロセスステータスを取得するSSEのコンポーザブル', () => {

    it('useStatusを呼び出すとSSEに接続して、ステータスを取得できる。', () => {
        const { status } = useStatus()

        expect(mockEventSource).toHaveBeenCalledWith('/api/status')
        expect(status.value).toEqual('')
    })

    it('SSEからステータスを受信すると、status.valueに値が入る。', () => {
        const { status } = useStatus()

        console.log(mockEventSource.mock.instances[0].onmessage)

        const event = {
            data: {
                status: 'test'
            }
        }

        mockEventSource.mock.instances[0].onmessage(event)

        expect(status.value).toEqual('test')
    })
})