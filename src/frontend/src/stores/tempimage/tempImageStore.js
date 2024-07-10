import { defineStore } from 'pinia'
import { ImageFile } from '@/types/image'

/**
 * 一時保存画像のストア
 */
export const useTempImageStore = defineStore('temp-image', {
  state: () => ({
    /**
     * 一時保存画像のリスト
     */
    imageList: [],
    selectedIndex: -1
  }),

  actions: {
    /**
     * 一時保存画像をセットする
     *
     * @param {Array} images ファイル名のリスト
     */
    setImages(images) {
      this.imageList.splice(0, this.imageList.length)
      images.forEach((image) => {
        this.addImage(image)
      })
    },

    /**
     * 一時保存画像を追加する
     *
     * @param {string} filename ファイル名
     */
    addImage(filename) {
      const image = new ImageFile({ name: filename, path: '/output/temp/' })
      const index = this.findImage(filename)
      if (index !== -1) {
        this.imageList[index] = image
      } else {
        this.imageList.push(image)
        // ファイル名降順にソート
        const newList = this.imageList.sort((a, b) => {
          if (a.name < b.name) {
            return 1
          } else {
            return -1
          }
        })
        this.imageList.splice(0, this.imageList.length, ...newList)
      }
    },

    /**
     * 一時保存画像を削除する
     *
     * @param {ImageFile} image
     */
    removeImage(image) {
      const index = this.findImage(image.name)
      if (index !== -1) {
        this.imageList.splice(index, 1)
      }
    },

    /**
     * ファイル名で一時保存画像を検索する
     *
     * @param {string} filename ファイル名
     * @returns {number} インデックス
     */
    findImage(filename) {
      return this.imageList.findIndex((image) => image.name === filename)
    },

    /**
     * 一時保存画像を選択する
     *
     * @param {ImageFile} image
     */
    selectImage(image, add = false) {
      this.selectedIndex = this.findImage(image.name)
      if (this.selectedIndex === -1) {
        return
      }
      if (add) {
        this.imageList[this.selectedIndex].selected = true
      } else {
        this.imageList.forEach((img) => {
          img.selected = false
        })
        this.imageList[this.selectedIndex].selected = true
      }
    }
  }
})
