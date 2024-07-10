import { VIEW_IDS } from '@/types/enum/view'
import { useAppSessionStorage } from '@/adapters/session/app'
import { useAppStateStore, useEditorStateStore, useProjectStore } from '@/stores/app'

/**
 * セッションストレージのユースケース
 *
 * @returns {ReturnType<typeof InitializeUseCase>}
 */
export function useSessionStorageUseCase() {
  return SessionStorageUseCase(
    useAppSessionStorage(),
    useAppStateStore(),
    useEditorStateStore(),
    useProjectStore()
  )
}

/**
 * セッションストレージのユースケース
 *
 * @param {ReturnType<typeof useAppSessionStorage>} storage
 * @param {ReturnType<typeof useAppStateStore>} appStore
 * @param {ReturnType<typeof useEditorStateStore>} editorStore
 * @param {ReturnType<typeof useProjectStore>} projectStore
 * @returns {Object}
 */
export function SessionStorageUseCase(storage, appStore, editorStore, projectStore) {
  return {
    load() {
      const storedData = storage.load()
      appStore.currentView = storedData.currentView || VIEW_IDS.EDITOR
      editorStore.mainArea = storedData.mainArea || editorStore.mainArea
      editorStore.mainImage = storedData.mainImage || editorStore.mainImage

      if (storedData.projectName) projectStore.defferedName = storedData.projectName
    },

    save() {
      storage.save({
        currentView: appStore.currentView,
        mainArea: editorStore.mainArea,
        mainImage: editorStore.mainImage,
        projectName: projectStore.data.projectName
      })
    }
  }
}
