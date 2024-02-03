/**
 * API呼び出しの共通処理
 */

function get (url, params) {
    let _url = url
    if (params) {
        _url += '?'
        for (const key in params) {
            _url += `${key}=${params[key]}&`
        }
    }
    return fetch(_url)
}

function post (url, data) {
    return fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    })
}

function upload (url, data) {
    return fetch(url, {
        method: 'POST',
        body: data
    })
}

/**
 * DELETEリクエスト
 * deleteが予約語なのでdelにしている
 * 
 * @param {*} url 
 * @returns 
 */
function del (url) {
    return fetch(url, {
        method: 'DELETE'
    })
}

export function useApi () {
    return{
        get,
        post,
        upload,
        del
    }
}