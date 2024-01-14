<script setup>
/**
 * 画像サイズ入力フォーム
 **/
import FormElement from '@/components/elements/FormElement.vue'
    
const props = defineProps({
    id: {
        type: String,
    },
    label: {
        type: String,
    },
})
const width = defineModel('width', {
    type: [String, Number],
    defaultValue: 0,
    set: (value) => {
        return parseInt(value)
    },
})
const height = defineModel('height', {
    type: [String, Number],
    defaultValue: '',
    set: (value) => {
        return parseInt(value)
    },
})
</script>

<template>
<FormElement :label="label" :id="id + 'Width'">
    <div class="grid">
        <div class="grid-item">
            <label :for="id + 'Width'">幅</label>
            <input
                type="text"
                :id="id + 'Width'"
                v-model="width"
            />
        </div>

        <div class="grid-item">
            <label :for="id + 'Height'">高さ</label>
            <input
                type="text"
                :id="id + 'Height'"
                v-model="height"
            />
        </div>
    </div>
</FormElement>
</template>

<style scoped>
.grid {
    width: 100%;
    display: flex;
    flex-direction: row;
}
.grid-item {
    width: 50%;
    display: flex;
}
.grid-item label {
    font-size: 80%;
    white-space: nowrap;
    margin-right: 10px;
}

input {
    flex-grow: 1;
    background-color: transparent;
    box-sizing: border-box;
    font-size: var(--font-size-base);
    border: 0 solid var(--color-border-window);
}

input::placeholder {
    color: var(--font-color-gray);
}
</style>