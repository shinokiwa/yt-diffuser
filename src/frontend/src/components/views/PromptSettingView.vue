<script setup>
/**
 * プロンプト設定画面
 */
import { ref, onMounted, onUnmounted } from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'
import InputPrompt from '@/components/elements/InputPrompt.vue'
import FormElement from '@/components/elements/FormElement.vue'
import InputSeed from '@/components/elements/InputSeed.vue'

import { useForm } from '@/composables/store/form'
import { useLatestForm } from '@/composables/api/res/form/latest'
import { useGeneratePreview } from '@/composables/api/generate/preview'
import { useOutputPreview } from '@/composables/api/res/output/preview'

const { previewSrc } = useOutputPreview()

onUnmounted(() => {
    // 本来このタイミングでやることではないが暫定。
    const { updateLatestForm } = useLatestForm()
    updateLatestForm()
})

const { seed, prompt, nPrompt, inferenceSteps } = useForm()

const promptList = ref([])
const nPromptList = ref([])

function preview () {
    const { updateLatestForm } = useLatestForm()
    updateLatestForm()

    const { start_generate } = useGeneratePreview()
    start_generate(
        seed.value,
        prompt.value,
        nPrompt.value,
        inferenceSteps.value
    )
}
</script>

<template>
<WindowArea id="PromptSettingView" window-title="プロンプト設定">
    <div id="PromptSettingArea">
        <div class="left-area">
            <div class="image-area">
                <img class="preview-image" :src="previewSrc" />
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
                <InputSeed label="SEED値" v-model="seed" />
                <div>
                    画像サイズ
                    <label>
                        縦
                    </label>
                    <input size="3" type="number" placeholder="1" />px<br />
                    <label>
                        横
                    </label>
                    <input size="3" type="number" placeholder="1" />px
                </div>
                <div>
                    <label>
                        スケジューラー
                    </label>
                    <select>
                        <option value="0">なし</option>
                        <option value="1">毎日</option>
                        <option value="2">毎週</option>
                        <option value="3">毎月</option>
                    </select>
                </div>
                <div>
                    <label for="InferenceSteps">
                        ステップ数
                    </label>
                    <input id="InferenceSteps" type="number" v-model="inferenceSteps" />
                </div>
                <div>
                    <label>
                        ガイダンススケール
                    </label>
                    <input type="number" placeholder="1" />
                </div>
            </div>
        </div>
        <div class="right-area">
            <InputPrompt
                id="prompt"
                label="プロンプト"
                v-model="prompt"
                :prompt-list="promptList"
            />
            <InputPrompt
                id="nPrompt"
                label="ネガティブプロンプト"
                v-model="nPrompt"
                :prompt-list="nPromptList"
            />
            <div class="prompt-area">
                メモ<br />
                <textarea placeholder=""></textarea>
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
