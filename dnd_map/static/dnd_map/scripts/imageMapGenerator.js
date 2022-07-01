class ImageMapGenerator {
    constructor(selector, div, maps) {
        let _img = document.createElement('img')
        div.appendChild(_img)

        const _selector = selector
        const _maps = JSON.parse(maps)

        const update_method = this.update
        selector.onchange = function () {update_method(_selector, _img, _maps)}

        selector.onchange()
    }

    update(selector, img, maps) {
        console.log(selector.value)
        img.src = maps[selector.value]
    }
}
