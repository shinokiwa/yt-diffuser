/**
 * API呼び出し
 * 
 */
import axios from 'axios'

const api = axios.create()

export function useApi () {
    return{
        api
    }
}