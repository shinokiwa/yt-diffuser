/**
 * APIドライバー用 パス処理系ユーティリティ
 */

/**
 * パス文字列とオブジェクトからGETクエリストリングを生成する
 *
 * @param {string} path パス文字列
 * @param {Object} params GETクエリストリングとして付与するパラメータ
 * @returns {string} GETクエリストリング付きパス
 */
export function createPath(path, params = {}) {
  let url = path
  if (params) {
    const query = []
    for (const key in params) {
      query.push(`${key}=${params[key]}`)
    }

    if (query.length > 0) {
      url += '?' + query.join('&')
    }
  }

  return url
}
