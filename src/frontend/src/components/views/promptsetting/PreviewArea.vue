<script setup>
/**
 * プレビュー画像エリア
 */
 import { ref } from 'vue'
import ImageArea from '@/components/views/promptsetting/ImageArea.vue'

const props = defineProps({
    src: {
        type: String,
        default: ''
    }
})
</script>

<template>
<ImageArea
    :src="src"
    ref="image"
    empty-message="プレビュー画像がありません。"
>
    <button
        title="ファイルを選択"
    >
        <i class="bi-files"></i>
    </button>
    <button
        title="クリップボードから貼付け"
    >
        <i class="bi-clipboard"></i>
    </button>
    <button
        title="画像を削除"
    >
        <i class="bi-trash"></i>
    </button>
</ImageArea>
</template>

<style scoped>
</style>