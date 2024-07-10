import { toRef, onMounted, onUnmounted } from 'vue'
import { useAPI } from '@/adapters/api'
import { useTempImageStore } from '@/stores/tempimage/tempImageStore'
import { ImageFile } from '@/types/image'

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
  let source = null
  const pendings = {}

  return {
    /**
     * リアクティブな参照を取得する
     * @returns {Array} 画像リスト
     */
    getRefs: () => ({
      imageList: toRef(store, 'imageList'),
      selectedIndex: toRef(store, 'selectedIndex')
    }),
    /**
     * EventSourceを接続する
     */
    useStream() {
      onMounted(() => {
        if (source === null) {
          source = new EventSource('/api/temp/')

          source.onmessage = (event) => {
            const data = JSON.parse(event.data)
            if (data.event_type === 'modified' || data.event_type === 'created') {
              // 1秒間の間に同じファイル名で複数回イベントが発生した場合、最後のイベントのみを処理する
              if (pendings[data.filename]) {
                clearTimeout(pendings[data.filename])
              }
              pendings[data.filename] = setTimeout(() => {
                store.addImage(data.filename)
                delete pendings[data.filename]
              }, 1000)
            }
          }
        }
      })

      onUnmounted(() => {
        if (source) {
          source.close()
        }
      })
    },

    /**
     * 一時保存画像を選択する
     * @param {ImageFile} image
     */
    selectImage(image) {
      store.selectImage(image)
    },

    /**
     * 一時保存画像を更新する
     */
    async update() {
      const response = await api.get('/api/temp/')
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
    async deleteImage() {
      store.imageList.forEach(async (img) => {
        if (img.selected === true) {
          await api.del(`/api/temp/${img.name}`)
          store.removeImage(img)
        }
      })
    }
  }
}
