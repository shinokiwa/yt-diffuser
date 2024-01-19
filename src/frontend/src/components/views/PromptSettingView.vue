<script setup>
/**
 * プロンプト設定画面
 */
import { ref, onMounted, onUnmounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import ProgressBar from '@/components/elements/ProgressBar.vue'

import InputPrompt from '@/components/elements/InputPrompt.vue'
import InputSeed from '@/components/elements/InputSeed.vue'
import InputText from '@/components/elements/InputText.vue'
import InputSize from '@/components/elements/InputSize.vue'

import { useLatestForm } from '@/composables/api/res/form/latest'
import { useFormPrompt } from '@/composables/api/res/form/prompt'
import { useGeneratePreview } from '@/composables/api/generate/preview'
import { useGenerateProgress } from '@/composables/api/generate/progress'
import { useOutputPreview } from '@/composables/api/res/output/preview'
import { useFormStore } from '@/composables/store/form'

const { percentage } = useGenerateProgress()
const { previewSrc } = useOutputPreview()

const { savePrompt, saveNegativePrompt } = useFormPrompt()

async function doUpdateLatestForm () {
    const { updateLatestForm } = useLatestForm()
    updateLatestForm({ seed, width, height, prompt, negativePrompt, scheduler, inferenceSteps, guidanceScale, memo })
}

onUnmounted(() => {
    // 本来このタイミングでやることではないが暫定。
    doUpdateLatestForm()
})

const { seed, width, height, prompt, negativePrompt, scheduler, inferenceSteps, guidanceScale, memo } = useFormStore()

const promptList = ref([])
const nPromptList = ref([])

function preview () {
    doUpdateLatestForm()

    const { start_generate } = useGeneratePreview()
    start_generate(
        seed.value,
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
<WindowArea id="PromptSettingView" window-title="プロンプト設定">
    <div id="PromptSettingArea">
        <div class="left-area">
            <div class="image-area">
                <img class="preview-image" :src="previewSrc" />

                <ProgressBar :value="percentage" height="10" />
            </div>
            <div clss="option-area">
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
                <InputSize id="ImageSize" label="画像サイズ" v-model:width="width" v-model:height="height" />
                <div>
                    <label>
                        スケジューラー
                    </label>
                    <select v-model="scheduler">
                        <option value="ddim">DDIM</option>
                        <option value="pndm">PNDM</option>
                        <option value="deis">DEIS Multi</option>
                        <option value="dpms-singlestep">DPMS Singlestep</option>
                        <option value="dpms-multistep">DPMS Multistep</option>
                        <option value="euler">Euler Dscrete</option>
                        <option value="euler-ancestral">Euler Ancestral</option>
                        <option value="lcm">LCM</option>
                    </select>
                </div>
                <InputText id="InferenceSteps" label="ステップ数" type="number" v-model="inferenceSteps" />
                <InputText id="GuidanceScale" label="ガイダンススケール" v-model="guidanceScale" />
            </div>
        </div>
        <div class="right-area">
            <InputPrompt
                id="prompt"
                label="プロンプト"
                v-model="prompt"
                :prompt-list="promptList"
                @save="savePrompt"
            />
            <InputPrompt
                id="nPrompt"
                label="ネガティブプロンプト"
                v-model="negativePrompt"
                :prompt-list="nPromptList"
                @save="saveNegativePrompt"
            />
            <div class="prompt-area">
                メモ<br />
                <textarea v-model="memo"></textarea>
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

.preview-image {
    width: 300px;
    height: 300px;
    object-fit: cover;
}


.right-area {
    flex-grow: 1;
    width: min-content;
}

textarea {
    width: 50%;
    height: 15em;
}
</style>
