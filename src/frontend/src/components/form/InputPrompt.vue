<script setup>
/**
 * プロンプト入力フォーム
 */
import { ref } from 'vue'
const props = defineProps({
  id: String
})

const prompt = defineModel()
const events = defineEmits(['expand', 'save'])

async function copy() {
  try {
    await navigator.clipboard.writeText(prompt.value);
  } catch (err) {
    console.error(err)
  }
}
</script>

<template>
  <div :id="id + 'Form'" class="input-prompt">
    <div class="button-area">
      <button type="button" title="拡大表示" @click="events('expand')">
        <i class="bi-arrows-angle-expand"></i>
      </button>

      <button type="button" title="クリップボードにコピー" @click='copy'>
            <i class="bi-clipboard"></i>
        </button>

      <button type="button" title="プロンプトを保存" @click="events('save', prompt)">
        <i class="bi-save2"></i>
      </button>

    </div>
    <textarea :id="id" placeholder="ここに入力" v-model="prompt"></textarea>
  </div>

</template>

<style scoped>
.input-prompt {
  display: flex;
  flex-direction: column;
  height: 100%;
  width: 100%;
}

.button-area {
  display: flex;
  justify-content: flex-end;
  padding: 5px;
}

.button-area button {
  margin-left: 5px;
}

textarea {
  flex: 1;
  height: 12em;
  padding: 5px;
  font-size: var(--font-size-base);
  resize: vertical;
  width: 100%;
  background-color: transparent;
  box-sizing: border-box;
  border-radius: 5px;
  border: 1px solid var(--color-border-window);
}
</style>