import { ProjectLayers } from './projectLayers'

export class Project {
  constructor(data) {
    this.projectName = data?.projectName || ''
    this.width = data?.width || 1024
    this.height = data?.height || 1024
    this.layers = new ProjectLayers(data?.layers)
  }

  /**
   * レイヤーをセットする
   */
  setLayers(layers) {
    this.layers = new ProjectLayers(layers)
  }
}
