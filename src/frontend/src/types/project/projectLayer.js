export class ProjectLayer {
  constructor(data) {
    this.layerId = data?.layerId
    this.layerName = data?.layerName
    this.width = data?.width
    this.height = data?.height
    this.image = data?.image
    this.i2i = data?.i2i
    this.mask = data?.mask
  }
}
