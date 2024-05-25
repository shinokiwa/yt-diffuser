/**
 * NotificationView.vue のテスト
 */
import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest'
import { mount } from '@vue/test-utils'
import { ref } from 'vue'

import { useNotificationAreaStoreMock } from '@mocks/composables/store/notificationArea.mock'
vi.mock('@/composables/store/notificationArea', () => ({useNotificationAreaStore: useNotificationAreaStoreMock}))

import { useNotificationStoreMock } from '@mocks/composables/store/notification.mock'
vi.mock('@/composables/store/notification', () => ({useNotificationStore: useNotificationStoreMock}))

import { useToastStoreMock } from '@mocks/composables/store/toast.mock'
vi.mock('@/composables/store/toast', () => ({useToastStore: useToastStoreMock}))

import NotificationView from '@/components/views/NotificationView.vue'

// setTimeoutを使うので、useFakeTimersを使う
beforeEach(() => {
    vi.useFakeTimers()
})


afterEach(() => {
    vi.resetAllMocks()
    vi.useRealTimers()
})

describe('NotificationView 通知画面', async () => {

    await describe('通知画面の表示、非表示', async () => {

        await it ('通知ボタンを押す(notificationStateがtrueになる)と通知画面を表示する', async ()=> {
            const { notificationAreaState } = useNotificationAreaStoreMock()

            const com = mount(NotificationView)
    
            const notification = com.find('.notification-panel')

            notificationAreaState.value = false
            await com.vm.$nextTick()

            expect(notification.exists()).toBe(true)
            expect(notification.classes()).not.toContain('show')
    
            notificationAreaState.value = true
            await com.vm.$nextTick()
    
            expect(notification.classes()).toContain('show')

            com.unmount()
        })
    })

    await describe('トースト表示', async () => {
        await it ('トーストがキューに追加されると、トーストを表示する', async ()=> {
            const { toastQueue, getToastQueue } = useToastStoreMock()
            // getToastQueueを呼び出すと、キューから要素を取り出すようにする
            getToastQueue.mockImplementation(() => toastQueue.value.shift())

            const com = mount(NotificationView)
            const toast = com.find('.toast')

            // トーストの表示状態はshowクラスの有無で判断する
            expect(toast.classes()).not.toContain('show')

            toastQueue.value = ['test message1', 'test message2']
            await com.vm.$nextTick()

            expect(toast.classes()).toContain('show')
            expect(toast.text()).toBe('test message1')

            // 3秒後にトーストが消える
            vi.advanceTimersByTime(3000)
            await com.vm.$nextTick()
            expect(toast.classes()).not.toContain('show')

            // トーストが残っている場合は、0.5秒後に次のトーストを表示する
            vi.advanceTimersByTime(500)
            await com.vm.$nextTick()
            expect(toast.classes()).toContain('show')
            expect(toast.text()).toBe('test message2')

            // 3秒後にトーストが消える
            vi.advanceTimersByTime(3000)
            await com.vm.$nextTick()
            expect(toast.classes()).not.toContain('show')

            // トーストが残っていない場合は、次のトーストを表示しない
            vi.advanceTimersByTime(500)
            await com.vm.$nextTick()
            expect(toast.classes()).not.toContain('show')
    
            // 毎回アンマウントしないとwatchが残ってしまう
            com.unmount()
        })
    })



})
