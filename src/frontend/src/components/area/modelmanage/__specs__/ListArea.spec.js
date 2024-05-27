/**
 * ListArea.vue のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

vi.mock('@/composables/model/modelUseCase')
import { ModelUseCase } from '@/composables/model/modelUseCase'

import ListArea from '../ListArea.vue'

describe('ModelListArea モデル一覧', () => {
  describe('一覧表示', () => {
    it('モデル一覧を表示する。', async () => {
      let com = mount(ListArea)

      await com.vm.$nextTick()

      // モデルリストが空の場合
      // 新規追加および現在のモデルのみが表示される
      expect(com.find('li.add-model').exists()).toBe(true)
      expect(com.find('li.current-model').exists()).toBe(true)
      expect(com.find('li.model-item').exists()).toBe(false)
      expect(ModelUseCase.fetchAll).toHaveBeenCalled()

      // モデルリストが空でない場合
      const { baseModels, loraModels, controlNetModels } = ModelUseCase.getRefs()

      baseModels.value = [
        { modelName: 'テスト1', modelClass: 'base-model' },
        { modelName: 'テスト2', modelClass: 'lora-model' },
        { modelName: 'テスト3', modelClass: 'controlnet-model' }
      ]

      await com.vm.$nextTick()
      expect(com.find('li.add-model').exists()).toBe(true)
      expect(com.find('li.current-model').exists()).toBe(true)
      expect(com.findAll('li.model-item').length).toBe(3)
    })
  })

  describe('新規追加ボタン', () => {
    it('新規追加ボタンをクリックすると、v-model:viewModeがaddになる。', async () => {
      let viewMode = ''
      const com = mount(ListArea, {
        props: {
          viewMode: viewMode,
          'onUpdate:viewMode': (v) => (viewMode = v)
        }
      })

      com.find('li.add-model').trigger('click')
      await com.vm.$nextTick()
      expect(viewMode).toBe('add')
    })
  })

  describe('現在のモデル', () => {
    it('現在のモデルをクリックすると、v-model:viewModeがcurrentになる。', async () => {
      let viewMode = ''
      const com = mount(ListArea, {
        props: {
          viewMode: viewMode,
          'onUpdate:viewMode': (v) => (viewMode = v)
        }
      })

      com.find('li.current-model').trigger('click')
      await com.vm.$nextTick()
      expect(viewMode).toBe('current')
    })
  })

  describe('各モデル', () => {
    it('各モデルをクリックすると、v-model:viewModeがdetailになり、v-model:selectedModelがクリックしたモデルのmodelNameになる。', async () => {
      let viewMode = ''
      let selectedModel = ''
      const { baseModels } = ModelUseCase.getRefs()
      baseModels.value = [
        { modelName: 'テスト1', modelClass: 'base-model' },
        { modelName: 'テスト2', modelClass: 'lora-model' },
        { modelName: 'テスト3', modelClass: 'controlnet-model' }
      ]
      const com = mount(ListArea, {
        props: {
          viewMode: viewMode,
          selectedModel: selectedModel,
          'onUpdate:viewMode': (v) => (viewMode = v),
          'onUpdate:selectedModel': (v) => (selectedModel = v)
        }
      })

      com.findAll('li.model-item').at(0).trigger('click')
      await com.vm.$nextTick()
      expect(viewMode).toBe('detail')
      expect(selectedModel).toBe('テスト1')

      com.findAll('li.model-item').at(1).trigger('click')
      await com.vm.$nextTick()
      expect(viewMode).toBe('detail')
      expect(selectedModel).toBe('テスト2')

      com.findAll('li.model-item').at(2).trigger('click')
      await com.vm.$nextTick()
      expect(viewMode).toBe('detail')
      expect(selectedModel).toBe('テスト3')
    })
  })
})
