/**
 * IntersectionObserverの制御
 * いまのところimgタグのみ対象
 */

let observer = null

export function useImageObserver() {
    if (observer === null) {
        observer = new IntersectionObserver ((entries) => {
            entries.forEach((entry) => {
                if (entry.isIntersecting) {
                    const image = entry.target
                    image.src = image.dataset.src
                    observer.unobserve(image)
                }
            })
        })
    }

    return {
        observer
    }
}