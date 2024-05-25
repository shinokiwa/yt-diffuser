// notification.js のテスト
import { describe, it, expect, vi } from 'vitest'

import { useNotificationStore } from '@/composables/store/notification'

describe('notification 通知の状態管理', () => {
        
    const {
        notificationList,
        addNotification,
        removeNotification,
        clearNotification
    } = useNotificationStore()

    it ('初期状態は空', () => {
        expect(notificationList.value).toEqual([])
    })

    describe('addNotification 通知の追加', () => {
        it ('通知を追加できる', () => {
            addNotification('test')
            expect(notificationList.value).toEqual(['test'])
        })
    })

    describe('notification.remove 通知の削除', () => {
        it ('通知を削除できる', () => {
            notificationList.value = ['test', 'test2', 'test3', 'test4']
            removeNotification(0)
            expect(notificationList.value).toEqual(['test2', 'test3', 'test4'])

            removeNotification(1)
            expect(notificationList.value).toEqual(['test2', 'test4'])
        })
    })

    describe('notification.clear 通知のクリア', () => {
        it ('通知をクリアできる', () => {
            notificationList.value = ['test', 'test2', 'test3', 'test4']
            clearNotification()
            expect(notificationList.value).toEqual([])
        })
    })
})

