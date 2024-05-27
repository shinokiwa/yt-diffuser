/**
 * index.js のテスト
 */
import { describe, it, expect, vi } from 'vitest'
import { useAPIDriver, APIDriver } from '../index'

describe('API呼び出しドライバー', () => {
  describe('useAPIDriver ファクトリーメソッド', () => {
    it('API呼び出しドライバーを返す。', () => {
      const driver = useAPIDriver()
      expect(driver).toHaveProperty('get')
      expect(driver).toHaveProperty('post')
      expect(driver).toHaveProperty('upload')
      expect(driver).toHaveProperty('del')
    })
  })

  describe('APIDriver', () => {
    const fetchMock = vi.fn().mockResolvedValue({
      json: vi.fn().mockResolvedValue({
        mock_data: 'response'
      })
    })

    const apiDriver = new APIDriver(fetchMock)

    describe('get', async () => {
      it('GETリクエストを送信する。', async () => {
        const response = await apiDriver.get('/api/res/model')
        expect(fetchMock).toHaveBeenCalledWith('/api/res/model')
        expect(response).toEqual({ mockData: 'response' })
      })

      it('パラメータでクエリストリングを付与する。', async () => {
        await apiDriver.get('/api/res/model', { key: 'value' })
        expect(fetchMock).toHaveBeenCalledWith('/api/res/model?key=value')
      })
    })

    describe('post', async () => {
      it('POSTリクエストを送信する。', async () => {
        const response = await apiDriver.post('/api/res/model', { sendData: 'value' })

        expect(fetchMock).toHaveBeenCalledWith('/api/res/model', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({ send_data: 'value' })
        })
        expect(response).toEqual({ mockData: 'response' })
      })
    })

    describe.skip('upload', async () => {
      it('POSTリクエストを送信する。', async () => {
        const data = new FormData()
        data.append('key', 'value')
        await apiDriver.upload('/api/res/model', data)
        expect(fetchMock).toHaveBeenCalledWith('/api/res/model', {
          method: 'POST',
          body: data
        })
      })
    })

    describe.skip('del', async () => {
      it('DELETEリクエストを送信する。', async () => {
        const response = await apiDriver.del('/api/res/model')
        expect(fetchMock).toHaveBeenCalledWith('/api/res/model', {
          method: 'DELETE'
        })
        expect(response).toEqual({ mock: 'response' })
      })
    })
  })
})
