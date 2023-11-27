<script setup>
/**
 * 通知エリアおよび通知トーストのコンポーネント
 * notificationStateがtrueになったら右端からスライドインで表示する。
 * また、newNotificationsに通知を追加すると、トーストで通知を表示する。
 * トーストは通知エリアと連動してスライドするため同一のコンポーネントで実装している。
 */

import { ref, watch } from 'vue'
import ProgressView from '@/components/views/ProgressView.vue'
import { useNotificationStore } from '@/composables/store/notification';
const {
    notificationState,
    showNotificationArea,
    hideNotificationArea,
    newNotifications,
    clearNewNotifications
} = useNotificationStore()

const notifications = ref([])
const toastQueue = ref([])
const isShownToast = ref(false)
const toastMessage = ref('')

watch(newNotifications, ()=>{
    // 新規通知を追加
    if (newNotifications.value.length === 0) {
        return;
    }
    notifications.value = notifications.value.concat(newNotifications.value)
    toastQueue.value = toastQueue.value.concat(newNotifications.value)

    clearNewNotifications()
    showToast()
})

function showToast() {
    if (toastQueue.value.length === 0) {
        return; // キューが空の場合は何もしない
    }

    isShownToast.value = true;
    toastMessage.value = toastQueue.value[0]; // キューの先頭のメッセージを表示

    setTimeout(() => {
        isShownToast.value = false;
        toastQueue.value.shift(); // 表示したメッセージをキューから削除
        if (toastQueue.value.length > 0) {
            setTimeout(showToast, 500); // 次のメッセージを表示
        }
    }, 3000); // メッセージを3秒間表示
}
</script>

<template>
<div id="NotificationView">
  <div class="notification-panel" :class="{ 'show': notificationState }">
    <ul class="notifications">
        <li class="notify-box" v-for="notification in notifications" :key="notification.id">
            {{ notification.message }}
        </li>
    </ul>
    <ul class="bottom">
        <li class="close">
            <a href="#" @click="hideNotificationArea()">閉じる</a>
        </li>
        <li class="progress notify-box">
            <ProgressView />
        </li>
    </ul>
  </div>
  <div class="toast-area">
    <div class="toast notify-box" :class="{ 'show': isShownToast }">
        {{ toastMessage }}
    </div>
  </div>
</div>
</template>

<style scoped>
.notification-panel {
    position: fixed;
    top: 0px;
    right: -500px; /* 初期状態では画面外に配置 */
    width: 400px;
    height: 100%;
    padding: 20px;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    transition: right 0.2s ease-in-out;
    background-color: var(--color-bg-menu);
    color: var(--font-color-light);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
}

.notification-panel.show {
    right: 0px; /* 表示時に画面内にスライドイン */
}

.notification-panel ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.notify-box {
    height: 100px;
    border: 1px solid var(--color-border-window);
    border-radius: 5px;
    box-sizing: content-box;
    padding: 10px;
    background-color: var(--color-bg-menu);
    color: var(--font-color-light);
}

.notification-panel ul.notifications li {
    margin-bottom: 10px;
}

.notification-panel ul.bottom {
    bottom: 0px;
    left: 0px;
    width: 100%;
}

.notification-panel ul.bottom li.close {
    margin-bottom: 10px;
}

.notification-panel ul.bottom li.close a {
    color: var(--font-color-light);
}

.notification-panel .progress {
    height: 140px;
}

.toast {
    visibility: hidden;
    width: 400px;
    margin-left: -125px;
    position: fixed;
    z-index: 100;
    right: 20px;
    bottom: -150px;
    transition: bottom 0.2s, visibility 0.5s, right 0.2s ease-in-out;
}

.toast.show {
    visibility: visible;
    bottom: 30px;
}

.notification-panel.show + .toast-area .toast {
    right: 420px;
}

</style>
