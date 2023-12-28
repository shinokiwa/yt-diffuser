<script setup>
/**
 * 生成ビューの出力エリア
 */
import { ref, onMounted, onUnmounted} from 'vue'
import WindowArea from '@/components/elements/WindowArea.vue'

import { useTemp } from '@/composables/api/res/output/temp'
const { imageList, refresh, close, deleteAll, deleteSelected } = useTemp()

onMounted(()=>{
    refresh()
})

onUnmounted(()=>{
    close()
})

const is_enable_delete = ref(false)
const gallery = ref(null)
const focus = ref(null)
const rangeFocus = ref(null)

/**
 * 対象を選択状態にする
 * 
 * @param {Element} target 対象の.gallery-item
 * @param {Boolean} ctrlKey Ctrlキーが押されているか
 * @param {Boolean} shiftKey Shiftキーが押されているか
 */
function selectItem (target, ctrlKey=false, shiftKey=false) {
    // Ctrlキーが押されていない場合は選択状態を解除
    if (ctrlKey === false) {
        clearSelect()
    }

    // Shiftキーが押されている場合は範囲選択
    if (shiftKey && focus.value !== null) {
        const startIndex = parseInt(rangeFocus.value)
        const targetIndex = parseInt(target.dataset.index)

        const range = [startIndex, targetIndex].sort((a, b) => a - b)

        gallery.value.querySelectorAll(`.gallery-item`).forEach((v) => {
            const index = parseInt(v.dataset.index)
            if (index >= range[0] && index <= range[1]) {
                v.dataset.selected = '1'
            }
        })
    } else {
        target.dataset.selected = target.dataset.selected === '1' ? '0' : '1'
        rangeFocus.value = target.dataset.index
    }

    focus.value = target.dataset.index
    if (gallery.value.querySelectorAll('.gallery-item[data-selected="1"]').length > 0) {
        is_enable_delete.value = true
    } else {
        is_enable_delete.value = false
    }
    return false
}

function clearSelect () {
    gallery.value.querySelectorAll('.gallery-item[data-selected="1"]').forEach((v) => {
        v.dataset.selected = 0
    })
    is_enable_delete.value = false
}


function mouseDown (event) {
    if (event.target.classList.contains('gallery-item')) {
        selectItem(event.target, event.ctrlKey, event.shiftKey)
    } else {
        clearSelect()
    }
}

function keyDown (event) {
    let index = focus.value === null ? 0 : parseInt(focus.value)

    if (event.key === 'ArrowRight') {
        if (gallery.value.querySelector('.gallery-item.focus') === null) {
            index = index - 1
        }
        if (index >= imageList.value.length - 1) {
            index = imageList.value.length - 2
        }
        selectItem(gallery.value.querySelector(`.gallery-item[data-index="${index + 1}"]`), false, event.shiftKey)
    } else if (event.key === 'ArrowLeft' && index > 0) {
        if (index < 1) {
            index = 1
        }
        selectItem(gallery.value.querySelector(`.gallery-item[data-index="${index - 1}"]`), false, event.shiftKey)
    } else if (event.key === 'ArrowUp' || event.key === 'ArrowDown') {
        event.preventDefault()
        const current = gallery.value.querySelector('.gallery-item.focus')
        const rect = current.getBoundingClientRect()
        let rows = []
        gallery.value.querySelectorAll('.gallery-item').forEach((v, i) => {
            let targetRect = v.getBoundingClientRect()
            if (targetRect.left == rect.left) {
                rows.push([v, targetRect])
            }
        })
        rows = rows.sort((a, b) => {
            return a[1].top - b[1].top
        })
        const currentRow = rows.findIndex((v) => {
            return v[0] === current
        })
        if (event.key === 'ArrowUp') {
            if (currentRow > 0) {
                selectItem(rows[currentRow - 1][0], false, event.shiftKey)
            }
        } else {
            if (currentRow < rows.length - 1) {
                selectItem(rows[currentRow + 1][0], false, event.shiftKey)
            }
        }
    } else if (event.key === 'Enter') {
        const selected = gallery.value.querySelector('.gallery-item[data-selected="1"]')
        if (selected !== null) {
            window.open(selected.dataset.imageUrl)
        }
    } else if (event.key === 'Delete') {
        doDeleteSelected()
    } else {
        return
    }
}

function doDeleteSelected () {
    const selected = gallery.value.querySelectorAll('.gallery-item[data-selected="1"]')
    const selectImgs = []
    selected.forEach((v) => {
        selectImgs.push(v.dataset.imageUrl)
    })
    if (selectImgs.length > 0) {
        deleteSelected(selectImgs)
    }

    is_enable_delete.value = false
}

function doDeleteAll () {
    window.confirm('すべて削除しますか？') && deleteAll()
}

</script>

<template>
<WindowArea window-title="出力画像" activate="1">
    <div class="menu">
        <button @click="refresh">更新</button>
        <button v-if="is_enable_delete" @click="doDeleteSelected">選択したものを削除</button>
        <button @click="doDeleteAll">すべて削除</button>
    </div>
    <div class="gallery"
        ref="gallery"
        tabindex="0"

        @mousedown.left="mouseDown"
        @keydown="keyDown($event)"
    >
        <div
            class="gallery-item"
            v-for="(image, index) in imageList"
            :key="image.id"

            :class="{ focus: focus === index.toString() }"
            :data-index="index"
            :data-image-url="image.url"
            data-selected="0"

        >
            <img
                :src="'output/temp/' + image.url + '?t=' + image.timestamp"
            />
        </div>
    </div>
</WindowArea>
</template>

<style scoped>

.menu {
    display: flex;
    justify-content: flex-end;
}

.menu button {
    margin: 5px;
}
.gallery {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    word-wrap: break-word;
    user-select: none;
}

.gallery-item {
    position: relative;
    width: 150px;
    height: 150px;
    margin: 5px;
    display: inline-block;
    box-sizing: content-box;
}

.gallery-item img {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.gallery-item::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    box-sizing: border-box;
}

.gallery-item.focus::before {
    box-shadow: 0 0 0 2px #333333;
}

.gallery-item[data-selected="1"]::before {
    border: 1px solid #3246dd;
    background-color: rgba(50, 70, 221, 0.3);
}


</style>