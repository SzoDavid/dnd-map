let model_select

const fields = {
    'none': ['name', 'pronunciation', 'parents', 'parents_kingdom', 'parents_city', 'parents_terrain', 'type',
        'description', 'map', 'coords', 'coords_index', 'coords_kingdom', 'coords_city', 'coords_location',
        'capital', 'discovered', 'show_description'],
    'kingdom': ['name', 'pronunciation', 'description', 'map', 'coords', 'discovered'],
    'city': ['name', 'pronunciation', 'parents', 'parents_kingdom', 'type', 'description', 'map', 'coords',
        'coords_index', 'coords_kingdom', 'capital', 'discovered'],
    'place': ['name', 'pronunciation', 'parents', 'parents_city', 'type', 'description', 'map', 'coords',
        'coords_index', 'coords_kingdom', 'coords_city', 'discovered'],
    'terrain': ['name', 'pronunciation', 'type', 'description', 'show_description'],
    'coords': ['parents', 'parents_kingdom', 'parents_city', 'parents_terrain', 'coords', 'coords_location'],
}

function refresh_page () {
    fields['none'].forEach(function (id) {
        document.getElementById(id).hidden = true
    })
    fields[model_select.value].forEach(function (id) {
        document.getElementById(id).hidden = false
    })
}

window.onload = function () {
    model_select = document.getElementById('model')
    refresh_page()
}
