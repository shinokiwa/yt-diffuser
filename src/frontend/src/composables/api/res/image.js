/**
 * 画像リソース関連の処理をまとめたコンポーザブル
 */

/**
 * 画像一覧を取得するSSE
 */
function getImageList (path, callback) {
    const source = new EventSource('/api/res/output/' + path)
    source.onmessage = (event) => {
        if (event.data.length > 0) {
            const data = JSON.parse(event.data)
            callback(data)
        }
    }
    return source
}

export function useImage() {
    return {
        getImageList
    }
}