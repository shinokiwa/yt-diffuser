/**
 * APIとUIのデータの変換を行うユーティリティ
 */

/**
 * データを再帰的にスネークケースに変換して返す
 *
 * @param {Object | Array} data 変換するデータ
 * @returns {Object | Array} スネークケースに変換されたデータ
 */
export function toSnakeCase(data) {
  if (Array.isArray(data)) {
    return data.map((item) => toSnakeCase(item))
  } else if (data !== null && typeof data === 'object') {
    const snakeData = {}
    for (const key in data) {
      const snakeKey = key.replace(/([A-Z])/g, '_$1').toLowerCase()
      snakeData[snakeKey] = toSnakeCase(data[key])
    }
    return snakeData
  } else {
    return data
  }
}

/**
 * データを再帰的にキャメルケースに変換して返す
 *
 * @param {Object | Array} data 変換するデータ
 * @returns {Object | Array} キャメルケースに変換されたデータ
 */
export function toCamelCase(data) {
  if (Array.isArray(data)) {
    return data.map((item) => toCamelCase(item))
  } else if (data !== null && typeof data === 'object') {
    const camelData = {}
    for (const key in data) {
      const camelKey = key.replace(/(_\w)/g, (m) => m[1].toUpperCase())
      if (typeof data[key] === 'object') {
        camelData[camelKey] = toCamelCase(data[key])
      } else {
        camelData[camelKey] = data[key]
      }
    }
    return camelData
  } else {
    return data
  }
}
