<script setup>
/**
 * トースト表示のコンポーネント
 */
import { ref, watch } from 'vue'
import { useLogUseCase } from '@/composables/app'
const { getRefs, getToast } = useLogUseCase()

const { hasToast } = getRefs()

const isShownToast = ref(false)
const toastMessage = ref('')

function showToast() {
  const message = getToast()
  if (message) {
    toastMessage.value = message
    isShownToast.value = true
    setTimeout(() => {
      isShownToast.value = false
      setTimeout(() => {
        showToast()
      }, 500)
    }, 3000)
  }
}

watch(hasToast, (value) => {
  if (value) {
    showToast()
  }
})
</script>

<template>
  <div id="ToastArea">
    <div class="toast" :class="{ show: isShownToast }">
      <div class="toast-message">{{ toastMessage }}</div>
    </div>
  </div>
</template>

<style scoped>
#ToastArea {
  position: absolute;
  display: flex;
  justify-content: center;
  top: 0;
  left: 0;
  width: 100%;
}

.toast {
  position: fixed;
  visibility: hidden;
  z-index: 10000;

  margin-top: -200px;
  min-width: 300px;
  min-height: 50px;

  border: 1px solid var(--color-border-window);
  border-radius: 5px;
  box-sizing: content-box;
  padding: 10px;
  background-color: var(--color-bg-menu);
  color: var(--font-color-light);

  transition:
    margin-top 0.2s,
    visibility 0.5s ease-in-out;
}

.toast.show {
  visibility: visible;
  margin-top: 20px;
}
</style>
