import { toRef } from 'vue'
import { useAPI } from '@/adapters/api'
import { useProjectStore } from '@/stores/app/'

/**
 * プロジェクト一覧のユースケースを返す
 *
 * @returns {ReturnType<typeof ProjectListUseCase>}
 */
export function useProjectListUseCase() {
  return ProjectListUseCase(useAPI(), useProjectStore())
}

/**
 * プロジェクト一覧のユースケース
 * @param {ReturnType<typeof useAPI>} api
 * @param {ReturnType<typeof useProjectStore>} projectStore
 * @returns {Object}
 */
export function ProjectListUseCase(api, projectStore) {
  const useCase = {
    /**
     * プロジェクトストアの参照を返す
     */
    getRefs() {
      return {
        project: toRef(projectStore, 'data'),
        isOpen: toRef(projectStore, 'isOpen')
      }
    },

    /**
     * プロジェクトの一覧を取得する
     * @returns {Promise<Object>}
     */
    async fetchAll() {
      const data = await api.get('/api/project')
      return data
    }
  }
  return useCase
}
