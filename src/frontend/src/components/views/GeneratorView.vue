<script setup>
import { ref } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import TempGalleryWindow from '@/components/views/common/TempGalleryWindow.vue'
import ProgressBar from '@/components/elements/ProgressBar.vue'

import { useGenerateProgress } from '@/composables/api/generate/progress'
import { useFormStore } from '@/composables/store/form'
import { useGenerateImage } from '@/composables/api/generate/image'

const { generateTotal: total, generateCount: count, percentage } = useGenerateProgress()

const generateCount = ref(1)

function submit () {
    start(generateCount.value)

}
function start (count) {
    const { start_generate } = useGenerateImage()
    const { generateType, width, height, prompt, negativePrompt, scheduler, inferenceSteps, guidanceScale, strength } = useFormStore()
    start_generate(
        generateType.value,
        count,
        width.value,
        height.value,
        prompt.value,
        negativePrompt.value,
        scheduler.value,
        inferenceSteps.value,
        guidanceScale.value,
        strength.value,
    )
}

</script>

<template>
<WindowArea id="GeneratorView" window-title="画像生成">
    <div id="GeneratorArea">
        <WindowArea id="InputArea" window-title="入力情報">
            <div class="body">
                <div class="preset">
                    <button @click="start(4)">4</button>
                    <button @click="start(10)">10</button>
                    <button @click="start(20)">20</button>
                </div>
                <div class="input">
                    <label for="Count">生成枚数</label>
                    <input id="Count" type="number" v-model="generateCount" />
                </div>
                <div class="button">
                    <button id="StartFromCount" @click="submit()">生成</button>
                </div>
                <div class="progress">
                    <ProgressBar :value="percentage" height="10" />
                    <div>
                        {{ count }} / {{ total }}
                    </div>
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

button {
    margin: 5px;
    padding: 5px 10px;
    color: var(--font-color-light);
    border: 1px solid var(--color-border-window);
    border-radius: 4px;
    background-color: #33cc44;
    font-weight: bold;
    cursor: pointer;
}
</style>