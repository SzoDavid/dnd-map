class ImageMapGenerator {
    constructor(selector, div, maps) {
        this.location_selector = selector
        this.maps = JSON.parse(maps)
        this.img = document.createElement('img')
        div.appendChild(this.img)

        let _this = this
        this.location_selector.onchange = function () {_this.update()}
        this.img.onclick = function (event) {_this.onclick(event)}

        console.log(this.maps)

        this.update()
    }

    onclick(event) {
        let zoom = this.maps[this.location_selector.value].width / this.img.offsetWidth
        let x = Math.round((event.pageX - this.img.offsetLeft) * zoom)
        let y = Math.round((event.pageY - this.img.offsetTop) * zoom)
        console.log('x: ' + x + ' y: ' + y)
    }

    update() {
        this.img.src = this.maps[this.location_selector.value].url
    }
}
