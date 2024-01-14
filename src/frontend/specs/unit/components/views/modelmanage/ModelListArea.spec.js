/**
 * components/views/modelmanage/ModelListArea.vue のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import { useGenerateStatusMock } from '@mocks/composables/api/generate/status.mock'
vi.mock('@/composables/api/generate/status', () => ({useGenerateStatus: useGenerateStatusMock}))

import ModelListArea from '@/components/views/modelmanage/ModelListArea.vue'

describe('ModelManageView モデル管理画面 モデル追加モーダルウィンドウ', () => {

    it ('モデル一覧の＋を押すとモデル追加のモーダルウィンドウを表示する', async ()=> {
        const com = mount(ModelListArea, {
            // Teleportが邪魔なのでスタブにする
            global: {
                stubs: {
                    Teleport: {
                        template: '<teleport><slot /></teleport>'
                    }
                }
            }
        })

        const add = com.find('#OpenAddModel')
        expect(add.exists()).toBe(true)
        expect(com.find('#AddModelView').exists()).toBe(false)

        add.trigger('click')
        await com.vm.$nextTick()

        const addModel = com.find('#AddModelView')

        expect(addModel.isVisible()).toBe(true)
    })

    it ('モデル追加のモーダルウィンドウの閉じるボタンを押すとモーダルウィンドウを閉じる', async ()=> {
        const com = mount(ModelListArea, {
            // Teleportが邪魔なのでスタブにする
            global: {
                stubs: {
                    Teleport: {
                        template: '<teleport><slot /></teleport>'
                    }
                }
            }
        })

        const add = com.find('#OpenAddModel')
        add.trigger('click')
        await com.vm.$nextTick()

        const addModel = com.find('#AddModelView')

        expect(addModel.isVisible()).toBe(true)

        addModel.find('header > button').trigger('click')
        await com.vm.$nextTick()

        expect(com.find('#AddModelView').exists()).toBe(false)
    })
})