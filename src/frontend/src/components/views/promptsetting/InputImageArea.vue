<script setup>
/**
 * 画像入力エリア
 */
import { ref } from 'vue'
import ImageArea from '@/components/views/promptsetting/ImageArea.vue'
import { useInputImage } from '@/composables/api/res/input/image'

const props = defineProps({
    src: {
        type: String,
        default: ''
    },
    imageType: {
        type: String,
        default: 'source'
    }
})

const image = ref(null)

const pasteFile = async ()=>{
    const { uploadImage } = useInputImage()
    try {
        const permission = await navigator.permissions.query({ name: 'clipboard-read' });
        if (permission.state === 'denied') {
            toast.emit('貼付に失敗しました。')
        }
        const clipboardContents = await navigator.clipboard.read();
        for (const item of clipboardContents) {
            if (!item.types.includes('image/png')) {
                toast.emit('クリップボードに画像がありません。')
            }
            const blob = await item.getType('image/png');
            const upfile = new File([blob], "check.png", { type: "image/png" })
            await uploadImage(props.imageType, upfile)
            image.value.update()
        }

    } catch (error) {
        console.error(error.message);
    }
}

const deleteFile = () => {
    const { deleteImage } = useInputImage()
    deleteImage(props.imageType)
    image.value.empty()
}
</script>

<template>
<ImageArea
    :src="src"
    ref="image"
    empty-message="画像をドラッグするか、ボタン操作で画像を選択してください。"
>
    <button
        title="ファイルを選択"
    >
        <i class="bi-files"></i>
    </button>
    <button
        title="クリップボードから貼付け"
        @click="pasteFile"
    >
        <i class="bi-clipboard"></i>
    </button>
    <button
        title="画像を削除"
        @click="deleteFile"
    >
        <i class="bi-trash"></i>
    </button>
</ImageArea>
</template>

<style scoped>
</style>