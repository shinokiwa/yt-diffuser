/**
 * 画像ファイルを扱うための型定義
 *
 */
export class ImageFile {
  /**
   * コンストラクタ
   *
   * @param {Object} data 画像データ
   */
  constructor(data) {
    this.uuid = data?.uuid || crypto.randomUUID()
    this.name = data?.name || ''
    this.path = data?.path || ''
    this.selected = data?.selected || false
  }
}
