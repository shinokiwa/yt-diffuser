// notification.js のテスト
import { describe, it, expect, vi } from 'vitest'


import { useNotificationStoreMock } from '@mocks/composables/store/notification.mock'
vi.mock('@/composables/store/notification', () => ({useNotificationStore: useNotificationStoreMock}))

import { useToastStore } from '@/composables/store/toast'

describe('toast トーストのキュー', () => {
            
        const {
            toastQueue,
            putToastQueue,
            getToastQueue,
        } = useToastStore()
    
        it ('初期状態は空', () => {
            expect(toastQueue.value).toEqual([])
        })
    
        describe('putToastQueue トーストキューの追加', () => {
            it ('トーストキューを追加できる', () => {
                putToastQueue('test')
                expect(toastQueue.value).toEqual(['test'])
            })
    
            it ('通知リストにも追加できる', () => {
                const { notificationList } = useNotificationStoreMock()
                toastQueue.value = []
                notificationList.value = []

                putToastQueue('test', true)
                putToastQueue('test2', false)

                expect(toastQueue.value).toEqual(['test', 'test2'])
                expect(notificationList.value).toEqual(['test'])
            })
        })
    
        describe('toast.get トーストキューから内容を取り出す', () => {
            it ('トーストキューから内容を取り出す', () => {
                toastQueue.value = ['test', 'test2']

                expect(getToastQueue()).toEqual('test')
                expect(toastQueue.value).toEqual(['test2'])

                expect(getToastQueue()).toEqual('test2')
                expect(toastQueue.value).toEqual([])

                expect(getToastQueue()).toEqual(undefined)
                expect(toastQueue.value).toEqual([])
            })
        })
})