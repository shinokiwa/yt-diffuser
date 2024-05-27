/**
 * サーバーステータスのストア
 *
 */
import { defineStore } from 'pinia'
import { toRef } from 'vue'

/**
 * サーバーステータス管理のストアを返す
 */
export const useServerStatusStore = defineStore('server-status', {
  state: () => ({
    /**
     * サーバーステータス
     */
    data: {
      health: 'ng',
      downloader: 'idle',
      generator: 'idle'
    },

    /**
     * 接続済みか
     *
     * @type {Boolean} 一度でもヘルスチェックが成功したらtrueになる
     */
    isConnected: false,

    /**
     * ヘルスチェックタイマーインスタンス
     */
    timer: null
  }),

  getters: {
    /**
     * リアクティブな参照を返す
     * @returns {Object} refs
     * @returns {Object.Ref} refs.isConnected 接続済みか
     */
    refs() {
      return {
        isConnected: toRef(this, 'isConnected')
      }
    }
  },

  actions: {
    /**
     * サーバーステータスを更新する。
     *
     * @param {Object} status サーバーステータス
     */
    setStatus(status) {
      this.data.health = status?.health
      this.data.downloader = status?.downloader
      this.data.generator = status?.generator
    },

    /**
     * 接続済みにする。
     *
     * @returns {void}
     */
    connected() {
      this.isConnected = true
    },

    /**
     * タイマーを保持する。
     * 定期的にヘルスチェックを行う時に使用する。
     *
     * @param {*} timer setTimeoutの戻り値
     * @returns {void}
     */
    setTimer(timer) {
      this.timer = timer
    }
  }
})
