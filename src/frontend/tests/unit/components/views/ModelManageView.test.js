// InitializingView.vueのテスト
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'
import { nextTick } from 'vue'

import ModelManageView from '@/components/views/ModelManageView.vue'

describe('ModelManageView モデル管理画面 モデル追加モーダルウィンドウ', () => {

    it ('モデル一覧の＋を押すとモデル追加のモーダルウィンドウを表示する', async ()=> {
        const com = mount(ModelManageView, {
            // Teleportが邪魔なのでスタブにする
            global: {
                stubs: {
                    Teleport: {
                        template: '<slot />'
                    }
                }
            }
        })

        const add = com.find('.new-model')
        expect(add.exists()).toBe(true)
        expect(com.find('#AddModelView').exists()).toBe(false)

        add.trigger('click')
        await nextTick()

        const addModel = com.find('#AddModelView')

        expect(addModel.isVisible()).toBe(true)
    })

    it ('モデル追加のモーダルウィンドウの閉じるボタンを押すとモーダルウィンドウを閉じる', async ()=> {
        const com = mount(ModelManageView, {
            // Teleportが邪魔なのでスタブにする
            global: {
                stubs: {
                    Teleport: {
                        template: '<slot />'
                    }
                }
            }
        })

        const add = com.find('.new-model')
        add.trigger('click')
        await nextTick()

        const addModel = com.find('#AddModelView')

        expect(addModel.isVisible()).toBe(true)

        addModel.find('header > button').trigger('click')
        await nextTick()

        expect(com.find('#AddModelView').exists()).toBe(false)
    })
})