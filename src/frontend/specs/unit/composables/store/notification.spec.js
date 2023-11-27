// notification.js のテスト
import { describe, it, expect, vi } from 'vitest'

import { useNotificationStore } from '@/composables/store/notification'

describe('通知の状態管理', () => {
        
    const {
        newNotifications,
        addNewNotification,
        clearNewNotifications,
        toggleNotificationArea,
        notificationState,
        showNotificationArea,
        hideNotificationArea
    } = useNotificationStore()

    describe ('通知エリアの表示状態', () => {
        it ('初期状態は非表示', () => {
            expect(notificationState.value).toBe(false)
        })

        it ('showNotificationAreaで通知エリアを表示できる', () => {
            showNotificationArea()
            expect(notificationState.value).toBe(true)
        })

        it ('hideNotificationAreaで通知エリアを非表示にできる', () => {
            hideNotificationArea()
            expect(notificationState.value).toBe(false)
        })

        it ('toggleNotificationAreaで通知エリアの表示状態を切り替えられる', () => {
            toggleNotificationArea()
            expect(notificationState.value).toBe(true)
            toggleNotificationArea()
            expect(notificationState.value).toBe(false)
        })
    })

    describe('新規通知の管理', () => {
        it ('初期状態は空', () => {
            expect(newNotifications.value).toEqual([])
        })
    
        it ('addNewNotificationで通知を追加できる', () => {
            addNewNotification('test')
            expect(newNotifications.value).toEqual(['test'])
        })
    
        it ('clearNewNotificationで通知を削除できる', () => {
            clearNewNotifications('test')
            expect(newNotifications.value).toEqual([])
        })
    })
})