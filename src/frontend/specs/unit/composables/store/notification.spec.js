// notification.js のテスト
import { describe, it, expect, vi } from 'vitest'

import { useNotificationStore } from '@/composables/store/notification'

describe('notification 通知の状態管理', () => {
        
    const { notification } = useNotificationStore()

    it ('初期状態は空', () => {
        expect(notification.getList().value).toEqual([])
    })

    describe('notification.add 通知の追加', () => {
        it ('通知を追加できる', () => {
            notification.add('test')
            expect(notification.getList().value).toEqual(['test'])
        })
    })

    describe('notification.remove 通知の削除', () => {
        it ('通知を削除できる', () => {
            notification.getList().value = ['test', 'test2', 'test3', 'test4']
            notification.remove(0)
            expect(notification.getList().value).toEqual(['test2', 'test3', 'test4'])

            notification.remove(1)
            expect(notification.getList().value).toEqual(['test2', 'test4'])
        })
    })

    describe('notification.clear 通知のクリア', () => {
        it ('通知をクリアできる', () => {
            notification.getList().value = ['test', 'test2', 'test3', 'test4']
            notification.clear()
            expect(notification.getList().value).toEqual([])
        })
    })
})

describe('toast トーストのキュー', () => {
            
        const { toast, notification } = useNotificationStore()
    
        it ('初期状態は空', () => {
            expect(toast.getQueue().value).toEqual([])
        })
    
        describe('toast.put トーストキューの追加', () => {
            it ('トーストキューを追加できる', () => {
                toast.put('test')
                expect(toast.getQueue().value).toEqual(['test'])
            })
    
            it ('通知リストにも追加できる', () => {
                toast.getQueue().value = []
                notification.getList().value = []

                toast.put('test', true)
                toast.put('test2', false)

                expect(toast.getQueue().value).toEqual(['test', 'test2'])
                expect(notification.getList().value).toEqual(['test'])
            })
        })
    
        describe('toast.get トーストキューから内容を取り出す', () => {
            it ('トーストキューから内容を取り出す', () => {
                toast.getQueue().value = ['test', 'test2']

                expect (toast.get()).toEqual('test')
                expect(toast.getQueue().value).toEqual(['test2'])

                expect (toast.get()).toEqual('test2')
                expect(toast.getQueue().value).toEqual([])

                expect (toast.get()).toEqual(undefined)
                expect(toast.getQueue().value).toEqual([])
            })
        })
})