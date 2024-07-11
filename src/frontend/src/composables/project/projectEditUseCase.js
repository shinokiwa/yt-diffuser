import { toRef } from 'vue'
import { useAPI } from '@/adapters/api'
import { useProjectStore } from '@/stores/app/'
import { ImageFile } from '@/types/image'

/**
 * プロジェクト編集のユースケースを返す
 */
export function useProjectEditUseCase() {
  return ProjectEditUseCase(useAPI(), useProjectStore())
}

/**
 * プロジェクト編集のユースケース
 * @param {ReturnType<typeof useAPI>} api
 * @param {ReturnType<typeof useProjectStore>} projectStore
 * @returns {Object}
 */
export function ProjectEditUseCase(api, projectStore) {
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
     * @param {String} projectName
     * @param {String} layerId
     * @param {ImageFile} image 表示するイメージファイル
     */
    getImageUrl(projectName, layerId, image) {
      return `output/project/${projectName}/layers/${layerId}/${image}`
    },
    /**
     * レイヤーを選択する
     */
    selectLayer(layerId) {
      projectStore.selectLayer(layerId)
    }
  }
  return useCase
}
