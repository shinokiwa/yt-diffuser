import { defineStore } from 'pinia'

/**
 * 進捗表示のストア
 */
export const useGenerateProgressStore = defineStore('generate-progress', {
  state: () => ({
    generateTotal: 0,
    generateCount: 0,

    percentage: 0,
    elapsed: 0,
    remaining: 0,
    average: 0
  }),

  actions: {
    /**
     * オブジェクトで一括設定する
     *
     * @param {Object} data 設定するデータ
     */
    setProgress(data) {
      this.generateTotal = data.generateTotal
      this.generateCount = data.generateCount
      this.percentage = data.percentage
      this.elapsed = data.elapsed
      this.remaining = data.remaining
    },

    /**
     * 進捗をリセットする
     */
    resetProgress() {
      this.generateTotal = 0
      this.generateCount = 0
      this.percentage = 0
      this.elapsed = 0
      this.remaining = 0
      this.average = 0
    }
  }
})
