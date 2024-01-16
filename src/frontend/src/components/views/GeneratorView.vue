<script setup>
import { ref } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import TempGalleryWindow from '@/components/views/common/TempGalleryWindow.vue'

import { useFormStore } from '@/composables/store/form'

import { useGenerateImage } from '@/composables/api/generate/image'
const { start_generate } = useGenerateImage()

const { width, height, prompt, negativePrompt, scheduler, inferenceSteps, guidanceScale } = useFormStore()

const generateCount = ref(1)

function submit () {
    start_generate(
        generateCount.value,
        width.value,
        height.value,
        prompt.value,
        negativePrompt.value,
        scheduler.value,
        inferenceSteps.value,
        guidanceScale.value,
    )
}


</script>

<template>
<WindowArea id="GeneratorView" window-title="画像生成">
    <div id="GeneratorArea">
        <WindowArea id="InputArea" window-title="入力情報">
            <div class="body">
                <div class="input">
                    <label for="count">生成枚数</label>
                    <input id="count" type="number" v-model="generateCount" />
                </div>
                <div class="button">
                    <button @click="submit()">生成</button>
                </div>
            </div>
        </WindowArea>
        <TempGalleryWindow id="OutputArea" />
    </div>
</WindowArea>
</template>

<style scoped>
#GeneratorArea{
    display: flex;
    flex-direction: row;
    height: 100%;
}

#InputArea {
    width: 500px;
    margin-right: 10px;
}

/** ここは暫定 **/
#InputArea textarea {
    width: 100%;
    height: 15em;
}

#OutputArea {
    flex-grow: 1;
    width: min-content;
}

</style>