/**
 * IntersectionObserverの制御
 * いまのところimgタグのみ対象
 */
import { onMounted, onUnmounted } from 'vue'

let observer = null

/**
 * IntersectionObserverのインスタンスを返す
 *
 * @param {Ref<HTMLElement>} image
 * @returns {Object} observer
 */
export function useImageObserver(image) {
  if (observer === null) {
    observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          const image = entry.target
          image.src = image.dataset.src
          observer.unobserve(image)
        }
      })
    })
  }

  onMounted(() => {
    const { observer } = useImageObserver()
    observer.observe(image.value)
  })
  onUnmounted(() => {
    const { observer } = useImageObserver()

    if (image.value) {
      observer.unobserve(image.value)
    }
  })
  return {
    observer
  }
}
