<script setup>
/**
 * ファイルギャラリーのエリア
 */
import { ref } from 'vue'
import Thumbnail from '@/components/elements/Thumbnail.vue'
import { useViewerStore } from '@/composables/store/viewer';

const props = defineProps({
    'baseDir': {
        type: String,
        default: ''
    },
    'fileList': {
        type: Array
    }
})
const emit = defineEmits(['select', 'clear', 'delete'])

/**
 * ファイルギャラリーのElement
 * 
 * @type {Ref<Element>}
 */
const gallery = ref(null)

/**
 * ファイルギャラリーの各項目のElement
 * 
 * @type {Ref<Element>}
 */
const galleryItems = ref(null)

/**
 * 拡大表示の要素
 */
const viewer = ref(null)

/**
 * 現在フォーカスがある要素のインデックス
 * 
 * @type {Ref<String>}
 */ 
const focus = ref(null)

/**
 * 範囲選択時のフォーカスの開始位置
 * 
 * @type {Ref<String>}
 */
const rangeFocus = ref(null)

/**
 * 拡大表示する画像のURL
 */
const viewImage = ref(null)

/**
 * 選択した要素を取得する
 * 
 * @return {NodeList} 選択した要素のNodeList
 */
function getSelectedItems () {
    return gallery.value.querySelectorAll('.gallery-item[data-selected="1"]')
}

/**
 * 指定したインデックスの要素を取得する
 * 
 * @param {Number | String} index インデックス
 * 
 * @return {Element} 要素
 */
function getItem (index) {
    return gallery.value.querySelector(`.gallery-item[data-index="${index}"]`)
}

/**
 * 対象を選択状態にする
 * 
 * Ctrlキーを押している場合は、選択対象を追加する
 * Shiftキーが押されている場合は範囲選択する
 * 
 * @param {Element} target 対象の.gallery-item要素
 * @param {Boolean} ctrlKey Ctrlキーが押されているか
 * @param {Boolean} shiftKey Shiftキーが押されているか
 */
function selectItem (target, ctrlKey=false, shiftKey=false) {
    // Ctrlキーが押されていない場合は選択状態を解除
    if (ctrlKey === false) { galleryItems.value.forEach((v) => { v.dataset.selected = '0' }) }

    // targetが.gallery-item要素でない場合は何もしない
    if (target.classList.contains('gallery-item') === false) { return }

    // Shiftキーが押されている場合は範囲選択
    if (shiftKey && rangeFocus.value !== null) {
        const range = [
            parseInt(rangeFocus.value),
            parseInt(target.dataset.index)
        ].sort((a, b) => a - b)

        galleryItems.value.forEach((v) => {
            const index = parseInt(v.dataset.index)
            if (index >= range[0] && index <= range[1]) {
                v.dataset.selected = '1'
            }
        })
    } else {
        target.dataset.selected = target.dataset.selected === '1' ? '0' : '1'
        rangeFocus.value = target.dataset.index
    }

    if (gallery.value.querySelector('.gallery-item[data-selected="1"]') === null) {
        emit('clear')
    } else {
        emit('select')
    }

    if (focus.value === target.dataset.index) {
        showViewer(target.dataset.imageUrl, target.dataset.timestamp)
    } else {
        focus.value = target.dataset.index
    }
    window.scrollTo(0, target.offsetTop)
    return false
}

function keyDown (event) {

    if (event.key === 'ArrowRight') {
        focusToNext(event)
    } else if (event.key === 'ArrowLeft') {
        focusToPrev(event)
    } else if (event.key === 'ArrowUp') {
        event.preventDefault()
        focusToUp(event)
    } else if (event.key === 'ArrowDown') {
        event.preventDefault()
        focusToDown(event)
    } else if (event.key === 'Delete') {
        event.preventDefault()
    } else if (event.key === 'Enter') {
        const selected = getItem(focus.value)
        if (selected) {
            showViewer(selected.dataset.imageUrl, selected.dataset.timestamp)
        }
    } else if (event.key === 'Escape') {
        viewer.value.hide()
    } else {
        return
    }
}


/**
 * フォーカスを次に移動する
 */
function focusToNext (event) {
    let index = focus.value === null ? 0 : parseInt(focus.value)

    if (gallery.value.querySelector('.gallery-item.focus') !== null) {
        index = index + 1
    }
    if (index >= props.fileList.length - 1) {
        index = props.fileList.length - 1
    }
    selectItem(getItem(index), false, event.shiftKey)
}

/**
 * フォーカスを前に移動する
 */
function focusToPrev (event) {
    let index = focus.value === null ? 0 : parseInt(focus.value)

    if (index < 1) {
        index = 1
    } else {
        index = index - 1
    }
    selectItem(getItem(index), false, event.shiftKey)
}

/**
 * 指定した要素の縦並びのリストを取得する
 */
function getVerticalList (target) {
    const rect = target.getBoundingClientRect()
    let rows = []
    let current = null
    gallery.value.querySelectorAll('.gallery-item').forEach((v, i) => {
        let targetRect = v.getBoundingClientRect()
        if (targetRect.left == rect.left) {
            rows.push([v, targetRect])
            if (targetRect.top == rect.top) {
                current = rows.length - 1
            }
        }
    })
    rows = rows.sort((a, b) => {
        return a[1].top - b[1].top
    })

    return [rows, current]
}

/**
 * フォーカスを上に移動する
 */
function focusToUp (event) {
    const [rows, current] = getVerticalList(getItem(focus.value))
    if (current === null) { return }

    if (current > 0) {
        selectItem(rows[current - 1][0], false, event.shiftKey)
    }
}

/**
 * フォーカスを下に移動する
 */
function focusToDown (event) {
    const [rows, current] = getVerticalList(getItem(focus.value))
    if (current === null) { return }

    if (current < rows.length - 1) {
        selectItem(rows[current + 1][0], false, event.shiftKey)
    }
}

/**
 * 選択した要素を削除するイベントを発火する
 */
 function deleteSelected () {
    const selected = getSelectedItems()
    const selectImgs = []
    selected.forEach((v) => {
        selectImgs.push(v.dataset.imageUrl)
    })
    if (selectImgs.length > 0) {
        emit('delete', selectImgs)
    }
    viewer.value.hide()
}

/**
 * 画像を拡大表示する
 */
function showViewer (url, timestamp) {
    const { showViewer, isShowViewer } = useViewerStore()
    showViewer(props.baseDir + url + '?t=' + timestamp)
}

defineExpose({
    getSelectedItems,
    deleteSelected
})

</script>

<template>
<div class="gallery"
    ref="gallery"
    tabindex="0"

    @mousedown.left="selectItem($event.target, $event.ctrlKey, $event.shiftKey)"
    @keydown="keyDown($event)"
>
    <div
        class="gallery-item"
        v-for="(image, index) in fileList"
        :key="image.id"
        ref="galleryItems"

        :class="{ focus: focus === index.toString() }"
        :data-index="index"
        :data-image-url="image.url"
        :data-timestamp="image.timestamp"
        data-selected="0"

        @dblclick="showViewer(image.url, image.timestamp)"
    >
        <Thumbnail
            :src="baseDir + image.url + '?t=' + image.timestamp"
        />
    </div>
</div>
</template>

<style scoped>
.gallery {
    display: flex;
    flex-wrap: wrap;
    justify-content: flex-start;
    word-wrap: break-word;
    user-select: none;
    height: 0;
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