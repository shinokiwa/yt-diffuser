<script setup>
/**
 * プロンプト設定画面
 */
import { ref, onMounted, onUnmounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import ProgressBar from '@/components/elements/ProgressBar.vue'

import InputPrompt from '@/components/elements/InputPrompt.vue'
import InputSeed from '@/components/elements/InputSeed.vue'
import InputSelect from '@/components/elements/InputSelect.vue'
import InputText from '../elements/InputText.vue'

import ImageTabArea from '@/components/views/promptsetting/ImageTabArea.vue'
import DetailArea from '@/components/views/promptsetting/DetailArea.vue'

import { useLatestForm } from '@/composables/api/res/form/latest'
import { useFormPrompt } from '@/composables/api/res/form/prompt'
import { useGeneratePreview } from '@/composables/api/generate/preview'
import { useGenerateProgress } from '@/composables/api/generate/progress'
import { useFormStore } from '@/composables/store/form'

const { percentage } = useGenerateProgress()

const { savePrompt, getPrompt, saveNegativePrompt, getNegativePrompt, deletePrompt } = useFormPrompt()

async function doUpdateLatestForm () {
    const { updateLatestForm } = useLatestForm()
    updateLatestForm({ seed, generateType, width, height, prompt, negativePrompt, scheduler, inferenceSteps, guidanceScale, strength, memo })
}

onUnmounted(() => {
    // 本来このタイミングでやることではないが暫定。
    doUpdateLatestForm()
})

const { seed, generateType, width, height, prompt, negativePrompt, scheduler, inferenceSteps, guidanceScale, strength, memo } = useFormStore()

function preview () {
    doUpdateLatestForm()

    const { start_generate } = useGeneratePreview()
    start_generate(
        generateType.value,
        seed.value,
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
<WindowArea id="PromptSettingView" window-title="プロンプト設定">
    <div id="PromptSettingArea">
        <div class="left-area">
            <ImageTabArea />

            <div clss="option-area">
                <ProgressBar :value="percentage" height="10" />
                <div>
                    <button @click="preview">プレビュー</button>
                </div>
                <div>
                    <input type="checkbox" id="RealTimePreview" />
                    <label for="RealTimePreview">
                        リアルタイムプレビュー
                    </label>
                </div>
                <InputSeed id="Seed" label="SEED値" v-model="seed" />
                <InputSelect id="Process" label="生成方法" v-model="generateType">
                    <option value="t2i">Text to Image</option>
                    <option value="i2i">Image to Image</option>
                    <option value="inpaint">InPaint</option>
                </InputSelect>
                <InputText id="Strength" label="強度" v-model="strength" />

            </div>
        </div>
        <div class="right-area">
            <InputPrompt
                id="prompt"
                label="プロンプト"
                v-model="prompt"

                :load="getPrompt"
                @save="savePrompt"
                :trash="deletePrompt"
            />
            <InputPrompt
                id="nPrompt"
                label="ネガティブプロンプト"
                v-model="negativePrompt"

                :load="getNegativePrompt"
                @save="saveNegativePrompt"
                :trash="deletePrompt"
            />
            <div class="detail-area">
                <DetailArea
                    class="detail-form"

                    v-model:width="width"
                    v-model:height="height"
                    v-model:scheduler="scheduler"
                    v-model:inferenceSteps="inferenceSteps"
                    v-model:guidanceScale="guidanceScale"
                />
                <div class="detail-memo">
                    メモ<br />
                    <textarea v-model="memo"></textarea>
                </div>
            </div>
        </div>
    </div>
</WindowArea>
</template>

<style scoped>
#PromptSettingArea{
    display: flex;
    flex-direction: row;
    height: 100%;
}

.left-area {
    width: 400px;
    margin-right: 10px;
}

.left-area .two-column > * {
    width: 50%;
}


.right-area {
    flex-grow: 1;
    width: min-content;
}

.detail-area {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
}

.detail-area > * {
    width: calc(50% - 10px);
}

.detail-area .detail-form {
    margin-right: 10px;
}

.detail-area textarea {
    width: 100%;
    height: 15em;
}
</style>
