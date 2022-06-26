let ImageMap = function (map, img, previousWidth) {
    let areas = map.getElementsByTagName('area'),
        len = areas.length,
        coords = []

    for (let n = 0; n < len; n++) {
        coords[n] = areas[n].coords.split(',')
    }

    this.resize = function () {
        let clen, x = img.offsetWidth / previousWidth

        for (let n = 0; n < len; n++) {
            clen = coords[n].length

            for (let m = 0; m < clen; m++) {
                coords[n][m] *= x
            }

            areas[n].coords = coords[n].join(',')
        }

        previousWidth = document.body.clientWidth
        return true
    }

    window.onresize = this.resize
}
