import { ProjectLayer } from './projectLayer'

export class ProjectLayers {
  /**
   * コンストラクタ
   * @param {Object} data
   */
  constructor(data) {
    this.layers = {}

    if (data?.layers && typeof data?.layers === 'object') {
      for (const layerId in data.layers) {
        this.layers[layerId] = new ProjectLayer(data.layers[layerId])
      }
    }

    this.order = []
    if (Array.isArray(data?.order)) {
      this.order = data.order
    }
  }

  /**
   * レイヤーを追加する
   *
   * レイヤーはorderの先頭に追加される
   *
   * @param { ProjectLayer } layer
   */
  addLayer(layer) {
    this.layers[layer.id] = new ProjectLayer(layer)
    this.order = [layer.id, ...this.order]
  }

  /**
   * イテレーター
   * orderの順番にlayerを返す
   */
  *[Symbol.iterator]() {
    for (const layerId of this.order) {
      yield this.layers[layerId]
    }
  }
}
