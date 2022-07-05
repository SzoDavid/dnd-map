class ImageMapGenerator {
    constructor(selector, div, coords_field, maps) {
        this.coords = null
        this.area = null
        this.finished = false
        let _this = this

        this.location_selector = selector
        this.maps = JSON.parse(maps)

        this.map = document.createElement('map')
        this.map.id = 'map'
        this.map.name = 'map'
        this.img = document.createElement('img')
        this.img.useMap = '#map'

        this.controls = document.createElement('div')
        this.reset = document.createElement('button')
        this.reset.textContent = 'RESET'
        this.reset.onclick = function () {
            _this.coords_field.value = ''
            location.reload()
        }
        this.controls.appendChild(this.reset)

        div.appendChild(this.img)
        div.appendChild(this.map)
        div.appendChild(this.controls)

        this.location_selector.onchange = function () {_this.update()}
        this.img.onclick = function (event) {_this.onclick(event)}

        this.update()

        this.coords_field = coords_field
        this.coords_field.disabled = true
        if (this.coords_field.value !== '') {
            this.create_area(this.coords_field.value)
        }
    }

    onclick(event) {
        if (this.finished) return

        let zoom = this.maps[this.location_selector.value].width / this.img.offsetWidth
        let x = Math.round((event.pageX - this.img.offsetLeft) * zoom)
        let y = Math.round((event.pageY - this.img.offsetTop) * zoom)

        if (this.coords === null) {
            if (this.area !== null ) {

            }
            this.coords = {
                x: x,
                y: y
            }
        } else {
            let topLeft = {
                x: Math.min(this.coords.x, x),
                y: Math.min(this.coords.y, y)
            }
            let bottomRight = {
                x: Math.max(this.coords.x, x),
                y: Math.max(this.coords.y, y)
            }

            this.create_area(`${topLeft.x},${topLeft.y},${bottomRight.x},${bottomRight.y}`)
        }
    }

    update() {
        this.img.src = this.maps[this.location_selector.value].url
        if (this.area) {
            this.map.removeChild(this.area)
            location.reload()
        }
        this.finished = false
        this.coords = null
    }

    create_area(coords) {
        this.area = document.createElement('area')
        this.area.title = 'Preview'
        this.area.coords = coords
        this.coords_field.value = coords
        this.area.href = '#'
        this.map.appendChild(this.area)
        $('img[usemap]').mapster({
            fillColor: '00ff00',
            singleSelect: true,
            scaleMap: true,
        })
        $('area').mapster('select')
        this.finished = true
    }
}
