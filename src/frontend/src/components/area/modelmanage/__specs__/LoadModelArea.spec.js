/**
 * LoadModelArea.vue のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { mount } from '@vue/test-utils'

import { useGenerateStatusMock } from '@mocks/composables/api/generate/status.mock'
vi.mock('@/composables/api/generate/status', () => ({ useGenerateStatus: useGenerateStatusMock }))

import { useModelMock } from '@mocks/composables/api/res/model.mock'
vi.mock('@/composables/api/res/model', () => ({ useModel: useModelMock }))

import ListArea from '@/components/views/modelmanage/ListArea.vue'

describe('ModelListArea モデル一覧', () => {
  it('モデル一覧を表示する。', async () => {
    const { baseModels } = useModelMock()
    const com = mount(ListArea)

    // モデルリストが空の場合
    // 新規追加および現在のモデルのみが表示される
    expect(com.find('li.add-model').exists()).toBe(true)
    expect(com.find('li.current-model').exists()).toBe(true)
    expect(com.find('li.model-item').exists()).toBe(false)

    // モデルリストが空でない場合
    baseModels.value = [
      { model_id: 'test1', model_name: 'テスト1', model_class: 'base-model' },
      { model_id: 'test2', model_name: 'テスト2', model_class: 'lora-model' },
      { model_id: 'test3', model_name: 'テスト3', model_class: 'controlnet-model' }
    ]

    await com.vm.$nextTick()
    expect(com.find('li.add-model').exists()).toBe(true)
    expect(com.find('li.current-model').exists()).toBe(true)
    expect(com.findAll('li.model-item').length).toBe(3)
  })

  it('新規追加ボタンをクリックすると、v-model:detailがaddになる。', async () => {
    let detail = ''
    const com = mount(ListArea, {
      props: {
        detail: detail,
        'onUpdate:detail': (v) => (detail = v)
      }
    })

    com.find('li.add-model').trigger('click')
    await com.vm.$nextTick()
    expect(detail).toBe('add')
  })

  it('statusが空かemptyの時に現在のモデルをクリックすると、v-model:detailが空になる。それ以外の時はcurrentになる。', async () => {
    let detail = 'current'
    const { status } = useGenerateStatusMock()
    status.value = ''
    const com = mount(ListArea, {
      props: {
        detail: detail,
        'onUpdate:detail': (v) => (detail = v)
      }
    })

    com.find('li.current-model').trigger('click')
    await com.vm.$nextTick()
    expect(detail).toBe('')

    detail = 'current'
    status.value = 'emtpy'

    com.find('li.current-model').trigger('click')
    await com.vm.$nextTick()
    expect(detail).toBe('')

    detail = ''
    status.value = 'loading'
    com.find('li.current-model').trigger('click')
    await com.vm.$nextTick()
    expect(detail).toBe('current')
  })

  it('各モデルをクリックすると、v-model:detailがmodelになり、v-model:selectがクリックしたモデルのmodel_nameになる。', async () => {
    let detail = ''
    let select = ''
    const { baseModels } = useModelMock()
    baseModels.value = [
      { model_id: 'test1', model_name: 'テスト1', model_class: 'base-model' },
      { model_id: 'test2', model_name: 'テスト2', model_class: 'lora-model' },
      { model_id: 'test3', model_name: 'テスト3', model_class: 'controlnet-model' }
    ]
    const com = mount(ListArea, {
      props: {
        detail: detail,
        'onUpdate:detail': (v) => (detail = v),
        select: select,
        'onUpdate:select': (v) => (select = v)
      }
    })

    com.findAll('li.model-item').at(0).trigger('click')
    await com.vm.$nextTick()
    expect(detail).toBe('model')
    expect(select).toBe('テスト1')

    com.findAll('li.model-item').at(1).trigger('click')
    await com.vm.$nextTick()
    expect(detail).toBe('model')
    expect(select).toBe('テスト2')

    com.findAll('li.model-item').at(2).trigger('click')
    await com.vm.$nextTick()
    expect(detail).toBe('model')
    expect(select).toBe('テスト3')
  })
})
