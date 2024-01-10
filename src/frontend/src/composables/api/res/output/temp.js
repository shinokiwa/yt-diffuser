/**
 * 一時保存リソース関連の処理をまとめたコンポーザブル
 */
import { ref } from 'vue'
import { useApi } from '@/composables/api'

const imageList = ref ([])
let source = null


/**
 * リソース一覧を更新する
 */
function refresh () {
    imageList.value = []
    close()

    source = new EventSource('/api/res/output/temp')
    source.onmessage = (event) => {
        if (event.data.length > 0) {
            const data = JSON.parse(event.data)

            if (data.type === 'delete' || data.type === 'modify') {
                imageList.value = imageList.value.filter((item) => {
                    return item.url !== data.target
                })
            }
    
            if (data.type === 'create' || data.type === 'list' || data.type === 'modify') {
                imageList.value.push({
                    id: imageList.value.length,
                    url: data.target,
                    timestamp: new Date().getTime(),
                })
            }

            // 名前逆順でソートする
            imageList.value = imageList.value.sort((a, b) => {
                return a.url < b.url ? 1 : -1
            })
        }
    }
}

/**
 * 一覧表示ストリームを閉じる
 */
function close () {
    if (source && source.readyState !== EventSource.CLOSED) {
        source.close()
    }
}


/**
 * 一時保存リソースを全て削除する
 * @returns 
 */
function deleteAll () {
    const {del} = useApi()
    return del('/api/res/output/temp')
}

/**
 * 選択したリソースを削除する
 * @returns 
 */
function deleteSelected (targets) {
    const {del} = useApi()

    targets.forEach((target) => {
        del('/api/res/output/temp/' + target)
    })
    imageList.value = imageList.value.filter((item) => {
        return !targets.includes(item.url)
    })
}


export function useTemp() {
    return {
        imageList,
        refresh,
        close,
        deleteAll,
        deleteSelected
    }
}