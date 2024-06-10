import { useAPI } from '@/adapters/api'
import { useTempImageStore } from '@/stores/tempimage/tempImageStore'

/**
 * 一時保存画像のユースケースを返す
 * @returns {ReturnType<typeof TempImageUseCase>}
 */
export function useTempImageUseCase() {
  return TempImageUseCase(useAPI(), useTempImageStore())
}

/**
 * 一時保存画像のユースケース
 * @param {ReturnType<typeof useAPI>} api
 * @param {ReturnType<typeof useTempImageStore>} store
 * @returns {Object}
 */
export function TempImageUseCase(api, store) {
  return {
    /**
     * リアクティブな画像リストを取得する
     * @returns {Array} 画像リスト
     */
    getImageList: () => store.imageList,

    /**
     * 一時保存画像を更新する
     */
    async update() {
      const response = await api.get('/api/temp/index')
      store.setImages(response.list)
    },

    /**
     * 一時保存画像を追加する
     * @param {Object} image 画像
     */
    addImage(image) {
      store.addImage(image)
    },

    /**
     * 一時保存画像を削除する
     * @param {Object} image 画像
     */
    removeImage(image) {
      store.removeImage(image)
    }
  }
}
