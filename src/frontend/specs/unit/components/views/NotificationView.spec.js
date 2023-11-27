/**
 * NotificationView.vue のテスト
 */
import { describe, it, expect, vi, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'

import NotificationView from '@/components/views/NotificationView.vue'

const mocks = {
    newNotifications: ref([]),
    hideNotificationArea: vi.fn(),
    notificationState: ref(false),
    clearNewNotifications: vi.fn()
}

vi.mock('@/composables/store/notification', () => {
    return { useNotificationStore: () => { return mocks } }
})

afterEach(() => {
    vi.resetAllMocks()
})

describe('NotificationView 通知画面', async () => {

    await describe('通知画面の表示、非表示', async () => {

        await it ('通知ボタンを押す(notificationStateがtrueになる)と通知画面を表示する', async ()=> {
            const com = mount(NotificationView)
    
            const notification = com.find('.notification-panel')

            mocks.notificationState.value = false
            await com.vm.$nextTick()

            expect(notification.exists()).toBe(true)
            expect(notification.classes()).not.toContain('show')
    
            mocks.notificationState.value = true
            await com.vm.$nextTick()
    
            expect(notification.classes()).toContain('show')

            com.unmount()
        })
    })

    await describe('通知画面の内容', async () => {
        await it ('通知が追加されると通知画面に表示する', async ()=> {
            const com = mount(NotificationView)
    
            mocks.newNotifications.value = [{id: 'test1', message: 'test message1'}, {id: 'test2', message: 'test message2'}]
            await com.vm.$nextTick()
    
            expect(com.findAll('.notifications li').length).toBe(2)
            expect(com.findAll('.notifications li')[0].text()).toBe('test message1')
    
            // 毎回アンマウントしないとwatchが残ってしまう
            com.unmount()
        })
    })



})
