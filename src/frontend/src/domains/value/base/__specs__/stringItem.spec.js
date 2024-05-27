/**
 * stringItem.js のテスト
 */
import { describe, it, expect } from 'vitest'

import { StringItem } from '../stringItem'

describe('StringItem', () => {
  it('値を設定するとバリデーションが実行され通過すると値がセットされる。', () => {
    const item = new StringItem('test')
    expect(item.value).toBe('test')
  })

  describe('validate', () => {
    it('optionsをオーバーライドするとバリデーションを変更できる。', () => {
      class TestItem extends StringItem {
        get options() {
          return {
            label: 'テスト',
            minLength: 5,
            maxLength: 10
          }
        }
      }
      const item = new TestItem('test')
      expect(item.hasError).toBe(true)
      expect(item.error).toBe('テストは5文字以上で入力してください。')

      const item2 = new TestItem('testtesttest')
      expect(item2.hasError).toBe(true)
      expect(item2.error).toBe('テストは10文字以内で入力してください。')

      const item3 = new TestItem()
      expect(item3.hasError).toBe(true)
      expect(item3.error).toBe('テストを入力してください。')
    })

    it('文字列以外の値を設定すると文字列に変換される。', () => {
      const item = new StringItem(123)
      expect(item.value).toBe('123')

      const item2 = new StringItem(null)
      expect(item2.value).toBe('')

      const item3 = new StringItem({ test: 'test' })
      expect(item3.value).toBe('[object Object]')
    })
  })
  describe('default', () => {
    it('値が入っていない場合だけデフォルト値を設定する', () => {
      const item = new StringItem().default('test')
      expect(item.value).toBe('test')

      const item2 = new StringItem('test').default('test2')
      expect(item2.value).toBe('test')
    })
  })
})
