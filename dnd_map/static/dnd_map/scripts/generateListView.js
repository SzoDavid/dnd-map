const admin = '<a class="toggle{0}" href="{1}">⚑</a><a class="toggle{2}" href="{3}">☰</a><a class="button" ' +
    'href="{4}">✎</a>'
const add = '<a class="button" href="{0}">+</a>'
const div = '<div class="list_column"><h2>{0}<a href="{1}">{2}</a></h2><ul>{3}{4}</ul></div>'
const li = '<li>{0}<a href="{1}">{2}</a><ul>{3}{4}</ul></li>'

String.prototype.format = function () {
    let args = arguments
    return this.replace(/{(\d+)}/g, function (match, index) {
        return typeof args[index] == 'undefined' ? match : args[index]
    })
}

function generateList(items, auth) {
    let result = ''

    items.forEach(function (item) {
        result += li.format(
            auth ? admin.format(
                !item['discovered'] ? ' off' : '',
                item['toggle_discovered'],
                !item['description'] ? ' off' : '',
                item['toggle_description'],
                item['edit']
            ) : '',
            item['details'],
            item['name'],
            item['children'].length === 0 ? '' : `${generateList(item['children'], auth)}`,
            auth ? `<li>${add.format(item['add_child'])}</li>` : ''
        )
    })

    return result
}

function populateListView(json, auth, add_div_url) {
    const items = JSON.parse(json)

    console.log(items)

    let result = ''

    items.forEach(function (item) {
        result += div.format(
            auth ? admin.format(
                !item['discovered'] ? ' off' : '',
                item['toggle_discovered'],
                !item['description'] ? ' off' : '',
                item['toggle_description'],
                item['edit']
            ) : '',
            item['details'],
            item['name'],
            item['children'].length === 0 ? '' : `${generateList(item['children'], auth)}`,
            auth ? `${add.format(item['add_child'])}` : ''
        )
    })

    result += `<div class="list_column"><h2>${add.format(add_div_url)}</h2</div>`

    document.getElementById('list_view').innerHTML = result
}

