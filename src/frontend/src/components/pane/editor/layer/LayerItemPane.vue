<script setup>
/**
 * レイヤー表示エリア レイヤーリスト
 */
import { ref } from 'vue'
import ImageThumb from '@/components/element/ImageThumb.vue'
import { ProjectLayer } from '@/types/project'

import { useEditorStateUseCase } from '@/composables/editorStateUseCase'
const { changeMainToLayer } = useEditorStateUseCase()

import { useProjectEditUseCase } from '@/composables/'
const { getRefs, getImageUrl, selectLayer } = useProjectEditUseCase()

const { selectedLayer } = getRefs()

const props = defineProps({
  projectName: {
    type: String,
    default: ''
  },
  layerId: {
    type: String,
    default: ''
  },
  layer: {
    type: ProjectLayer,
    default: new ProjectLayer()
  },
  mode: {
    type: String,
    default: 'view'
  }
})

const name = ref(props.layer.layerName)
const mode = ref(props.mode)
const input = ref(null)

function select() {
  selectLayer(props.layerId)
  changeMainToLayer()
}
function toEdit() {
  mode.value = 'edit'
  input.value.disabled = false
  input.value.focus()
}
</script>

<template>
  <div
    class="layer-item"
    :class="{ selected: selectedLayer === layerId }"
    @click="select"
    @dblclick="toEdit"
  >
    <div class="layer-thumb">
      <ImageThumb :src="getImageUrl(projectName, layerId, layer.image)" :cacheBuster="true" />
    </div>
    <div class="layer-info">
      <input
        ref="input"
        type="text"
        :disabled="mode === 'view'"
        v-model="name"
        @focusout="mode = 'view'"
      />
    </div>
  </div>
</template>

<style scoped>
.layer-item {
  padding: 5px;
  border-bottom: 1px solid var(--color-border-window);
  display: flex;
  align-items: center;
  flex-direction: row;
}
.layer-item.selected {
  background-color: var(--color-bg-selected);
}
.layer-item:hover,
.layer-item.selected:hover {
  background-color: var(--color-bg-focus);
}

.layer-thumb {
  width: 50px;
  height: 50px;
}
.layer-info {
  margin-left: 5px;
  display: flex;
  align-items: center;
  flex-direction: column;
}
</style>
