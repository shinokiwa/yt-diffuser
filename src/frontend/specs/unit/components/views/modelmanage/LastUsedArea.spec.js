/**
 * components/views/modelmanage/LastUsedArea.vue のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import { useModelMock } from '@mocks/composables/api/res/model.mock'
vi.mock('@/composables/api/res/model', () => ({useModel: useModelMock}))

import { useGenerateProcessMock } from '@mocks/composables/api/generate/process.mock'
vi.mock('@/composables/api/generate/process', () => ({useGenerateProcess: useGenerateProcessMock}))

import LastUsedArea from '@/components/views/modelmanage/LastUsedArea.vue'

describe('LastUsedArea 前回使用モデル', () => {
    it ('前回使用モデルを表示する。', async ()=> {
        const { lastUsedModel } = useModelMock()
        const com = mount (LastUsedArea)

        // 前回使用モデルが空の場合
        expect(com.find('.last-used-model').exists()).toBe(false)

        // 前回使用モデルが空でない場合
        lastUsedModel.value = {
            base: {model_name: 'テスト1', revision: 'base_revision', model_class: 'base-model'},
            lora: {model_name: 'テスト2', revision: 'lora_revision', model_class: 'lora-model'},
            controlnet: {model_name: 'テスト3', revision: 'control_revision', model_class: 'controlnet-model'},
        }

        await com.vm.$nextTick()
        expect(com.find('.last-used-model').exists()).toBe(true)
    })

    it ('前回使用モデルをクリックすると、loadModelが実行される。', async ()=> {
        const { lastUsedModel } = useModelMock()
        const { loadModel } = useGenerateProcessMock()
        lastUsedModel.value = {
            base: {model_name: 'テスト1', revision: 'base_revision', model_class: 'base-model'},
            lora: {model_name: 'テスト2', revision: 'lora_revision', model_class: 'lora-model'},
            controlnet: {model_name: 'テスト3', revision: 'control_revision', model_class: 'controlnet-model'},
        }
        const com = mount (LastUsedArea)

        await com.find('.last-used-model button').trigger('click')
        expect(loadModel).toHaveBeenCalledWith('テスト1', 'base_revision')
    })

})