/**
 * API呼び出し
 * 
 * axiosは今後使わないのであとで消す。
 */
import axios from 'axios'

const apix = axios.create()

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

export function useApi () {
    return{
        apix,
        get
    }
}