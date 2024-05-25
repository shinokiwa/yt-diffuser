<template>
    <div class="form-area"
        @click="selectImage"
        @dragenter="dragEnter"
    >
        <div class="title">
            {{ props.title }}
        </div>
        <div class="btn-menu mb-2">
            <button type="button" class="btn btn-outline-secondary" title="ファイルを選択" @click.stop="selectImage">
                <i class="bi-files"></i>
            </button>
            <button type="button" class="btn btn-outline-secondary" title="クリップボードから貼付け" @click.stop="pasteImage" v-if="!props.nonpaste">
                <i class="bi-clipboard"></i>
            </button>
            <button type="button" v-if="isUploaded" class="btn btn-outline-secondary" title="画像を削除" @click.stop="deleteImage">
                <i class="bi-trash"></i>
            </button>
        </div>
    
        <input ref="input" class="hidden" type="file" @change="changeImage" />
    
        <div class="image-zone"
            tabindex="0"
        >
            <div v-if="isUploaded">
                <img
                    ref="image"
                    :src="targetURL"
                    alt="アップロード済みの画像"
                    @load="getImageInfo"
                >
                <p v-if="imageInfo" class="text-center">{{ imageInfo.width }} x {{ imageInfo.height }}</p>
            </div>
            <div v-if="isUploaded == false" class="no-image">
                画像をドラッグするか、ボタン操作で画像を選択してください。
            </div>
        </div>
        <div
            class="drag-zone"
            v-if="isEnter"
            @dragover.prevent
            @drop.prevent="dropImage"
            @dragenter="dragEnter"
            @dragleave="dragLeave"
        ></div>
    </div>
    </template>
    
    <script setup>
    import { defineProps, defineEmits, ref, onMounted} from 'vue'
    import axios from 'axios';
    import toast from '@/events/toast.js'
    
    const props = defineProps({
        modelValue:Boolean,
        title:String,
        target:String,
        nonpaste: Boolean
    })
    const emits = defineEmits(['update:modelValue'])
    
    const image = ref(null)
    const targetURL = ref(props.target)
    const imageInfo = ref(null)
    
    const isUploaded = ref(false)
    onMounted(()=>{
        if (props.target != '') {
            updateImage()
            const checkImg = new Image()
            checkImg.src = targetURL.value
            checkImg.onload = ()=>{
                isUploaded.value = true
                emits('update:modelValue', true)
                updateImage()
            }
        }
    })
    
    const getImageInfo = () => {
        const i = image.value
        imageInfo.value = {
            width: i.naturalWidth,
            height: i.naturalHeight
        }
    }
    
    const updateImage = () => {
        const date = new Date();
        const timestamp = date.getTime();
        targetURL.value = `${props.target}?cacheBuster=${timestamp}`
    }
    
    const isEnter = ref(false)
    const dragEnter = () => isEnter.value = true
    const dragLeave = () => isEnter.value = false
    const dropImage = (event)=> {
        const images = event.dataTransfer.files;
        uploadImage(images[0]);
        isEnter.value = false;
    }
    
    const input = ref(null)
    const selectImage = ()=>input.value.click()
    const changeImage = () => {
        if (input.value.files.length == 0) {
            return false
        }
        uploadImage(input.value.files[0])
    }
    
    const pasteImage = async ()=>{
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
                const image = new File([blob], "check.png", { type: "image/png" })
                uploadImage(image)
            }
        } catch (error) {
            console.error(error.message);
        }
    }
    
    const uploadImage = (targetImage) => {
        const formData = new FormData();
        formData.append('image', targetImage);
        const api = axios.create()
        api.post('/api/userdata' + props.target, formData).then((response)=>{
            const r = response.data
            if (r.result == 'ok') {
                isUploaded.value = true
                emits('update:modelValue', true)
                updateImage()
                toast.emit('画像を更新しました。')
            } else if (r.result == 'err' && r.type == 'validation') {
                if (r.data.errors.indexOf("Filetype is not supported.") != -1) {
                    toast.emit('この形式には対応していません。')
                } else {
                    toast.emit(r.data.errors[0])
                }
            } else {
                console.error(r);
            }
        }).catch((error)=>{
            console.error(error);
        })
    }
    
    const deleteImage = () => {
        const api = axios.create()
        api.delete(`/api/userdata${props.target}`).then((response)=>{
            if (response && response.data) {
                const r = response.data
                if (r.result == 'ok') {
                    isUploaded.value = false
                    emits('update:modelValue', false)
                    toast.emit('画像を削除しました。')
                } else {
                    toast.emit('画像の削除に失敗しました。')
                }
            }
        })
    }
    
    </script>
    
    <style scoped>
    .form-area {
        height: 180px;
        border: 1px solid var(--color-mid2);
        box-sizing: border-box;
        padding: 10px;
    }
    
    .title {
        margin-left: 0;
    }
    
    .form-area .btn-menu {
        margin-top: -11px;
        padding-right: 10px;
    }
    .image-zone {
        text-align: center;
    }
    
    .image-zone .no-image {
        margin-top: 43px;
    }
    
    .image-zone img {
        width: auto;
        height: auto;
        max-width: 90px;
        max-height: 90px;
    }
    
    .drag-zone {
        position: absolute;
        top:0; right: 0; bottom:0; left: 0;
    
        border:1px solid #86b7fe;
        outline: 0;
        box-shadow: 0 0 2px 5px var(--color-shadow);
        border-radius: inherit;
    }
    </style>