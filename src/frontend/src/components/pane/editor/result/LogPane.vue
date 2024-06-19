<script setup>
import { useLogUseCase } from '@/composables/app/'
const useCase = useLogUseCase()

const { logs } = useCase.getRefs()

function clear() {
  useCase.clearLog()
}
</script>

<template>
  <div id="EditorResultLogPane">
    <div class="button-area">
      <button @click="clear">
        <i class="bi-trash"></i>
      </button>
    </div>
    <div class="log-area">
      <ul>
        <li v-for="(log, index) in logs" :key="index">
          {{ log }}
        </li>
      </ul>
    </div>
  </div>
</template>

<style scoped>
#EditorResultLogPane {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  height: 100%;
}

.button-area {
  height: 30px;
  display: flex;
  justify-content: flex-end;
  padding: 5px;
}

.button-area button {
  background-color: #aaaaaa;
  margin-left: 5px;
}

.button-area button:hover {
  background-color: #3344aa;
}

.log-area {
  flex: 1;
  width: 100%;
  overflow-x: auto;
  overflow-y: scroll;
}
</style>
