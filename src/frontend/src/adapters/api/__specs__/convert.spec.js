/**
 * convert.js のテスト
 */
import { describe, it, expect } from 'vitest'
import { toCamelCase, toSnakeCase } from '../convert'

describe('toSnakeCase', () => {
  it('データを再帰的にスネークケースに変換して返す', () => {
    const data = {
      simple: 'value1',
      nullValue: null,
      camelCase: {
        snakeCase: 'value2'
      }
    }
    const result = toSnakeCase(data)
    expect(result).toEqual({
      simple: 'value1',
      null_value: null,
      camel_case: { snake_case: 'value2' }
    })
  })

  it('配列の要素も再帰的にスネークケースに変換して返す', () => {
    const data = {
      array: [
        {
          camelCase: 'value1'
        }
      ]
    }
    const result = toSnakeCase(data)
    expect(result).toEqual({
      array: [
        {
          camel_case: 'value1'
        }
      ]
    })
  }),
    it('nullの場合はnullを返す', () => {
      const data = null
      const result = toSnakeCase(data)
      expect(result).toBeNull()
    })
})

describe('toCamelCase', () => {
  it('データを再帰的にキャメルケースに変換して返す', () => {
    const data = {
      simple: 'value1',
      null_value: null,
      camel_case: {
        snake_case: 'value2'
      }
    }
    const result = toCamelCase(data)
    expect(result).toEqual({
      simple: 'value1',
      nullValue: null,
      camelCase: { snakeCase: 'value2' }
    })
  })

  it('配列の要素も再帰的にキャメルケースに変換して返す', () => {
    const data = {
      array: [
        {
          camel_case: 'value1'
        }
      ]
    }
    const result = toCamelCase(data)
    expect(result).toEqual({
      array: [
        {
          camelCase: 'value1'
        }
      ]
    })
  })

  it('nullの場合はnullを返す', () => {
    const data = null
    const result = toCamelCase(data)
    expect(result).toBeNull()
  })
})
