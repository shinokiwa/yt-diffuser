import { toRef } from 'vue'
import { useAPI } from '@/adapters/api'
import { useProjectStore } from '@/stores/app/'
import { ProjectLayer } from '@/types/project'
import { ImageFile } from '@/types/image'
import { useProjectUseCase } from './projectUseCase'

/**
 * レイヤーのユースケースを返す
 *
 * @returns {ReturnType<typeof ProjectLayerUseCase>}
 */
export function useProjectLayerUseCase() {
  return ProjectLayerUseCase(useAPI(), useProjectStore(), useProjectUseCase())
}

/**
 * レイヤーのユースケース
 *
 * @param {ReturnType<typeof useAPI>} api
 * @param {ReturnType<typeof useProjectStore>} projectStore
 * @param {ReturnType<typeof useProjectUseCase>} projectUseCase
 * @returns
 */
export function ProjectLayerUseCase(api, projectStore, projectUseCase) {
  const project = toRef(projectStore, 'data')
  return {
    /**
     * プロジェクトストアの参照を返す
     */
    getRefs() {
      return {
        project,
        selectedLayer: toRef(projectStore, 'selectedLayer'),
        isOpen: toRef(projectStore, 'isOpen')
      }
    },
    /**
     * レイヤーを取得する
     */
    getLayer(layerId) {
      return project.value.layers.layers[layerId]
    },
    /**
     * レイヤー画像のパスを取得
     *
     * @param {String} layerId
     * @param {String} imageType 表示するイメージファイル (image, i2i, mask)
     * @return {String} 画像のパス 画像が存在しない場合は空文字を返す
     */
    getImageUrl(layerId, imageType) {
      const projectName = project.value.projectName
      const image = project.value.layers.layers[layerId][imageType]

      if (image) {
        return `output/project/${projectName}/layers/${layerId}/${image}`
      } else {
        return ''
      }
    },
    /**
     * レイヤーを選択する
     */
    selectLayer(layerId) {
      projectStore.selectLayer(layerId)
    },

    /**
     * レイヤーを追加する
     */
    async addLayer(layerName) {
      await api.post(`/api/project/${project.value.projectName}/layer`, { layerName })
      await projectUseCase.load(project.value.projectName)
    },

    /**
     * 選択中のレイヤーに画像をアップロードする
     *
     * @param {String} imageType 画像の種類 (image, i2i, mask)
     * @param {File} file 画像ファイル
     */
    async uploadImage(imageType, file) {
      const projectName = project.value.projectName
      const layerId = projectStore.selectedLayer
      await api.upload(`/api/project/${projectName}/layer/${layerId}/${imageType}`, { file })
      await projectUseCase.load(projectName)
    }
  }
}
