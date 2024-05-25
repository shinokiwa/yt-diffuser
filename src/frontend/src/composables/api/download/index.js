/**
 * /api/download に関する処理をまとめたコンポーザブル
 */
import { useApi } from '@/composables/api'
const { get, post } = useApi()

/**
 * ダウンロードを開始する
 */
async function startDownload (repo_id, revision) {
    await post('/api/download/start', {
        repo_id,
        revision
    })
}

export function useDownload () {
    return {
        startDownload
    }
}