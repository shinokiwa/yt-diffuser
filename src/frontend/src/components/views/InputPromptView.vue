<script setup>
import { ref, onMounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import Overlay from '@/components/elements/Overlay.vue'
import FormGrid from '@/components/elements/FormGrid.vue'
import InputText from '@/components/elements/InputText.vue'

import { useGenerateImage } from '@/composables/api/generate/image'
const { start_generate } = useGenerateImage()

function submit () {
    start_generate(prompt.value)
}

const prompt = ref(null)

</script>

<template>
<WindowArea id="InputPromptView" window-title="画像生成">
    <textarea placeholder="入力テキストを入力して下さい。" v-model="prompt"></textarea>
    <button @click="submit()">生成</button>
</WindowArea>
</template>