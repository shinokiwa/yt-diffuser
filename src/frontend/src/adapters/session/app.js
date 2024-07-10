const STORAGE_KEY = 'appData'

/**
 * セッションストレージを利用したデータ管理を提供する
 *
 * @returns {ReturnType<typeof AppSessionStorage>} セッションストレージを利用したデータ管理
 */
export function useAppSessionStorage() {
  return AppSessionStorage(sessionStorage)
}

/**
 * セッションストレージを利用したデータ管理
 *
 * @param {Storage} storage セッションストレージ
 */
export function AppSessionStorage(storage) {
  return {
    /**
     * セッションストレージからデータを読み込む
     *
     * @returns {Object} データ
     */
    load() {
      const storedData = storage.getItem(STORAGE_KEY)
      return storedData ? JSON.parse(storedData) : {}
    },

    /**
     * データをセッションストレージに保存する
     *
     * @param {Object} data 保存するデータ
     */
    save(data) {
      storage.setItem(STORAGE_KEY, JSON.stringify(data))
    }
  }
}
