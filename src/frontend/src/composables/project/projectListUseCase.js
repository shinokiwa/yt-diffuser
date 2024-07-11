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
     * プロジェクトを新規作成する
     */
    createProject: async (name, width, height) => {
      const data = {
        name,
        width,
        height
      }
      await api.post('/api/project', data)
      await this.load(name)
    },
    /**
     * プロジェクトの一覧を取得する
     * @returns {Promise<Object>}
     */
    async fetchAll() {
      const data = await api.get('/api/project')
      return data
    },

    /**
     * プロジェクトを読み込む
     *
     * @param {String} projectName プロジェクト名
     * @param {Boolean} withOpen プロジェクトを開くかどうか
     */
    async load(projectName) {
      const data = await api.get('/api/project/' + projectName)
      projectStore.setData(data)
    },

    /**
     * プロジェクトを閉じる
     */
    close() {
      projectStore.close()
    },

    /**
     * 読み込み予約を実行する
     */
    async loadDeffered() {
      if (projectStore.defferedName !== '') {
        await this.load(projectStore.defferedName)
        projectStore.defferedName = ''
      }
    }
  }
  return useCase
}
