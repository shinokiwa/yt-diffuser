import { toRef } from 'vue'
import { useAPI } from '@/adapters/api'
import { useProjectStore } from '@/stores/app/'
import { useAppStateUseCase } from './appStateUseCase'
import { VIEW_IDS } from '@/types/enum/view'
import { ImageFile } from '@/types/image'

/**
 * プロジェクトのユースケースを返す
 */
export function useProjectUseCase() {
  return ProjectUseCase(useAPI(), useProjectStore(), useAppStateUseCase())
}

/**
 * プロジェクトのユースケース
 * @param {ReturnType<typeof useAPI>} api
 * @param {ReturnType<typeof useProjectStore>} projectStore
 * @param {ReturnType<typeof useAppStateUseCase>} appState
 * @returns {Object}
 */
export function ProjectUseCase(api, projectStore, appState) {
  const useCase = {
    /**
     * プロジェクトストアの参照を返す
     */
    getRefs() {
      return {
        project: toRef(projectStore, 'data'),
        selectedLayer: toRef(projectStore, 'selectedLayer'),
        isOpen: toRef(projectStore, 'isOpen')
      }
    },
    /**
     * レイヤー画像のパスを取得
     *
     * @param {Project} project
     * @param {String} layerId
     * @param {ImageFile} image 表示するイメージファイル
     */
    getImageUrl(project, layerId, image) {
      return `output/project/${project.projectName}/layers/${layerId}/${image}`
    },
    /**
     * プロジェクトを新規作成する
     */
    createProject: async (name, width, height) => {
      await api.post('/api/project', {
        name,
        width,
        height
      })
      this.open()
    },
    /**
     * プロジェクトの一覧を取得する
     * @returns {Promise<Object>}
     */
    async fetchAll() {
      const data = await api.get('/api/project')
      return data
    },

    /**
     * プロジェクトを読み込む
     *
     * @param {String} projectName プロジェクト名
     * @param {Boolean} withOpen プロジェクトを開くかどうか
     */
    async load(projectName, withOpen = true) {
      const data = await api.get('/api/project/' + projectName)
      projectStore.setData(data)
      if (withOpen) this.open()
    },

    /**
     * 読み込んだプロジェクトを展開する
     */
    open() {
      //editorStateStore.changeMainImage()
      appState.changeView(VIEW_IDS.EDITOR)
    },

    /**
     * プロジェクトを閉じる
     */
    close() {
      projectStore.close()
    },

    /**
     * レイヤーを選択する
     */
    selectLayer(layerId) {
      projectStore.selectLayer(layerId)
    }
  }

  if (projectStore.defferedName !== '') {
    useCase.load(projectStore.defferedName)
    projectStore.defferedName = ''
  }
  return useCase
}
