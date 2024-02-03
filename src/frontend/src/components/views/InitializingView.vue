<script setup>
/**
 * 初期化中画面のコンポーネント
 * 
 * 初期化処理もここで行う。
 */
import { onMounted } from 'vue'

import ProgressBar from '@/components/elements/ProgressBar.vue'

import { useModel } from '@/composables/api/res/model'
import { useLatestForm } from '@/composables/api/res/form/latest'
import { useFormStore } from '@/composables/store/form'
import { useViewStore } from '@/composables/store/view'
import { useGenerateStatus } from '@/composables/api/generate/status'


onMounted(healthCheck)

/**
 * サーバーが起動するのを待つ
 */
async function healthCheck () {
    try {
        const response = await fetch('/api/health')
        if (response.ok) {
            await init()
        } else {
            setTimeout(healthCheck, 3000)
        }
    } catch (e) {
        console.log(e)
        setTimeout(healthCheck, 3000)
    }
}

/**
 * 初期化処理
 * 
 * 前回使用モデルを取得
 * 取得できた場合は生成ビュー表示
 * モデル一覧を取得
 * モデルがある場合はモデルセットアップ表示
 * モデルがない場合はモデル管理表示
 */
async function init () {
    useGenerateStatus()

    const { getModels, baseModels } = useModel()
    await getModels()

    const { getLatestForm } = useLatestForm()
    await getLatestForm()

    const { changeView, views } = useViewStore()

    if (baseModels.value.length == 0) {
        changeView(views.MODEL_MANAGE)
    } else {
        changeView(views.MODEL_MANAGE)
    }
}
</script>

<template>
<div id="InitializingView">
    <p>初期化中...</p>
    <div class="progress-bar-wrapper">
        <ProgressBar :value=100 />
    </div>
</div>
</template>

<style scoped>
#InitializingView {
    width: 100%;
    height: 100%;
}

#InitializingView p {
    margin: 100px auto 10px;
    text-align: center;
}

#InitializingView .progress-bar-wrapper {
    width: 50%;
    margin: auto;
}
</style>