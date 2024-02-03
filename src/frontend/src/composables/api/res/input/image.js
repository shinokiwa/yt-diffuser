/**
 * 画像アップロードの処理をするコンポーザブル
 */
import { useApi } from '@/composables/api'

const { upload, del } = useApi()

/**
 * 画像タイプからURLを取得する
 */
function getImageUrl(imageType) {
    if (imageType in ['source', 'mask', 'controlnet']) {
        throw new Error('Invalid image type')
    }
    
    return 'api/res/input/image/' + imageType
}

/**
 * 画像をアップロードする
 * @param {string} imageType
 * @param {File} file
 * @returns {Promise}
 */
async function uploadImage (imageType, file) {
    const formData = new FormData()
    formData.append('image', file)
    const url = getImageUrl(imageType)
    return await upload(url, formData)
}

/**
 * 画像を削除する
 * 
 * @returns 
 */
async function deleteImage(imageType) {
    const url = getImageUrl(imageType)
    return await del(url)
}

export function useInputImage() {


    return {
        uploadImage,
        deleteImage
    }
}