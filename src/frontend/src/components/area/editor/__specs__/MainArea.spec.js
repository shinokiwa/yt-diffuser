import { describe, it, expect, vi } from 'vitest'
import { shallowMount } from '@vue/test-utils'
import { ref } from 'vue'

import MainArea from '../MainArea.vue'

let isOpen = ref(false)
vi.mock('@/composables', () => {
  return {
    useProjectUseCase: () => ({
      getRefs: () => ({
        project: {
          projectName: 'test'
        },
        isOpen
      })
    }),
    useEditorStateUseCase: () => ({
      getRefs: () => ({
        mainArea: 'project'
      })
    })
  }
})

describe('MainArea エディターのメイン画像表示領域', () => {
  it('プロジェクトを開いているかどうかが表示される。', () => {
    let wrapper = shallowMount(MainArea, {
      global: {
        stubs: {
          '*': true,
          WindowFrame: false
        }
      }
    })
    expect(wrapper.find('div.project-info').text()).toBe('プロジェクトが開かれていません')

    isOpen.value = true
    wrapper = shallowMount(MainArea, {
      global: {
        stubs: {
          '*': true,
          WindowFrame: false
        }
      }
    })
    expect(wrapper.find('div.project-info').text()).toBe('プロジェクト名: test')
  })
})
