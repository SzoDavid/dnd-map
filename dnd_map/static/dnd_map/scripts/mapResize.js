class ImageMap {
    constructor(map, img, previousWidth) {
        this.img = img
        this.previousWidth = previousWidth
        this.areas =map.getElementsByTagName('area')
        this.len = this.areas.length
        this.coords = []

        for (let n = 0; n < this.len; n++) {
            this.coords[n] = this.areas[n].coords.split(',')
        }
        
        window.onresize = this.resize
    }

    resize() {
        let clen, x = this.img.offsetWidth / this.previousWidth

        for (let n = 0; n < this.len; n++) {
            clen = this.coords[n].length

            for (let m = 0; m < clen; m++) {
                this.coords[n][m] *= x
            }

            this.areas[n].coords = this.coords[n].join(',')
        }

        this.previousWidth = document.body.clientWidth
        return true
    }
}
