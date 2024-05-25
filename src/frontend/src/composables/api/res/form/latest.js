/**
 * 最新のフォームデータを取得・更新するAPI
 */
import { useApi } from '@/composables/api'
import { useFormStore } from '@/composables/store/form'

const { get, post } = useApi()

/**
 * キャメルケースからスネークケースへ変換する
 * 
 * @param {*} str 変換する文字列
 * @returns スネークケースに変換された文字列
 */
function camelToSnake(str) {
    return str.replace(/([A-Z])/g, '_$1').toLowerCase();
}
  
/**
 * スネークケースからキャメルケースへ変換する
 * 
 * @param {*} str 変換する文字列
 * @returns キャメルケースに変換された文字列
 */
function snakeToCamel(str) {
    return str.replace(/(_\w)/g, m => m[1].toUpperCase());
}

/**
 * 最新のフォームデータを取得し、store/form.jsに反映する
 */
async function getLatestForm () {
    const response = await get('/api/res/form/latest')
    const data = await response.json()

    const forms = useFormStore()
    for (const key in data) {
        const camelKey = snakeToCamel(key)
        if (camelKey in forms){
            forms[camelKey].value = data[key]
        }
    }
}


/**
 * フォームデータを更新する。
 * キャメルケースのキーをスネークケースに変換して送信するため、
 * キー名を合わせる必要がある。
 * 
 * @param {Object} forms フォーム名をキーとしたフォームデータのオブジェクト
 */
async function updateLatestForm (forms) {
    const data = {}

    for (const key in forms) {
        const snakeKey = camelToSnake(key)
        data[snakeKey] = forms[key].value
    }
    
    await post ('/api/res/form/latest', data)
}

export function useLatestForm () {
    return {
        getLatestForm,
        updateLatestForm
    }
}