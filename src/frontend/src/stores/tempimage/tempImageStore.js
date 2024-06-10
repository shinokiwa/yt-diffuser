import { defineStore } from 'pinia'

/**
 * 一時保存画像のストア
 */
export const useTempImageStore = defineStore('temp-image', {
  state: () => ({
    /**
     * 一時保存画像のリスト
     */
    imageList: []
  }),

  actions: {
    /**
     * 一時保存画像をセットする
     */
    setImages(images) {
      this.imageList.splice(0, this.imageList.length, ...images)
    },

    /**
     * 一時保存画像を追加する
     *
     * @param {Object} image 画像
     */
    addImage(image) {
      this.imageList.push(image)
    },

    /**
     * 一時保存画像を削除する
     *
     * @param {Object} image 画像
     */
    removeImage(image) {
      const index = this.imageList.findIndex((item) => item === image)
      this.imageList.splice(index, 1)
    }
  }
})
