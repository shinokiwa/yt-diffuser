/**
 * apiDriver.js のモック
 */
import { vi } from 'vitest'

const API = {
  get: vi.fn(),
  post: vi.fn(),
  put: vi.fn(),
  upload: vi.fn(),
  del: vi.fn()
}

export const useAPI = vi.fn().mockReturnValue(API)
