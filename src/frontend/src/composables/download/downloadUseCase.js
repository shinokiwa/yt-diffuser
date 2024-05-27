/**
 * ダウンロードAPIのユースケース
 */
import { useAPI } from '@/adapters/api'

/**
 * ダウンロードユースケースを返す
 * @returns {ReturnType<typeof DownloadUseCase>}
 */
export function useDownloadUseCase() {
  return DownloadUseCase(useAPI())
}

/**
 * ダウンロードユースケース
 *
 * @param {ReturnType<typeof useFormStore>} store
 */
export function DownloadUseCase(api) {
  return {
    async startDownload(repo_id, revision) {
      await api.post('/api/download/start', {
        repo_id,
        revision
      })
    }
  }
}
