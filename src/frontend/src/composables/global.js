/**
 * フロントエンド全体に影響するグローバルコンポーザブル
 */
import { ref } from 'vue'

import { useModel } from '@/composables/model'

const currentView = ref('initialize')

/**
 * 初期化処理
 * 
 * 前回使用モデルを取得
 * 取得できた場合は生成ビュー表示
 * モデル一覧を取得
 * モデルがある場合はモデルセットアップ表示
 * モデルがない場合はモデル管理表示
 * @returns void
 */
async function init () {
    const {loadModels, baseModels} = useModel()
    await loadModels()

    if (currentView.value =='initialize' && baseModels.value.length == 0) {
        currentView.value = 'modelmanage'
    }
}

export function useGlobals() {
    return {
        currentView,

        init
    }
}