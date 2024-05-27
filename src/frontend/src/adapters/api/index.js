/**
 * API呼び出しドライバー
 */
import { toCamelCase, toSnakeCase } from './convert'
import { createPath } from './path'

/**
 * APIアダプターを返す
 *
 * @returns {ReturnType<typeof API>}
 */
export function useAPI() {
  // fetch関数はthisの参照が変わるとエラーになるので、
  // クロージャを使ってfetch関数を保持する
  return API((url, options) => {
    return fetch(url, options)
  })
}

/**
 * APIアダプター
 *
 * @return {Object}
 */
export function API(fetch) {
  return {
    /**
     * GETリクエスト
     * 基本的にデータ取得用
     *
     * @param {String} path APIのパス
     * @param {Object} params クエリストリングスとして付与するパラメータ
     * @returns {Promise<Object>} APIのレスポンス(JSONオブジェクト、キャメルケース変換済み)
     */
    async get(path, params) {
      const apiPath = createPath(path, params)
      const response = await fetch(apiPath)
      const json = toCamelCase(await response.json())
      const data = json.data
      return data
    },

    /**
     * POSTリクエスト
     * データ登録用
     *
     * @param {String} path APIのパス
     * @param {Object} params 送信するデータ
     * @returns {Promise<Object>} APIのレスポンス(JSONオブジェクト)
     */
    async post(path, params) {
      const inputData = toSnakeCase(params)

      const response = await fetch(path, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(inputData)
      })
      const json = toCamelCase(await response.json())
      const outputData = json.data
      return outputData
    },

    /**
     * POSTリクエスト (ファイルアップロード用)
     *
     * もうちょっと工夫がいる
     *
     * @param {String} path APIのパス
     * @param {Object} data 送信するデータ
     */
    async upload(path, data) {
      const response = await this.fetch(path, {
        method: 'POST',
        body: data
      })
      return await response.json()
    },

    /**
     * DELETEリクエスト
     * deleteが予約語なのでdelにしている
     *
     * @param {*} path APIのパス
     * @returns {Promise<Object>} APIのレスポンス(JSONオブジェクト)
     */
    async del(path) {
      const response = await this.fetch(path, {
        method: 'DELETE'
      })
      return await response.json()
    }
  }
}
