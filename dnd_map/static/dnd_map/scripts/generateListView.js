const admin = '<a class="toggle{0}" href="{1}">{2}</a><a class="toggle{3}" href="{4}">{5}</a><a class="button" href="{6}">✎</a>'
const add = '<a class="button" href="{0}">+</a>'
const div = '<div class="list_column">{0}<a href="{1}">{2}</a>{3}</div>{4}'
const li = '<li>{0}<a href="{1}">{2}</a>{3}</li>{4}'

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
                item['discovered'] ? '✓' : '✗',
                !item['description'] ? ' off' : '',
                item['toggle_description'],
                item['description'] ? '✓' : '✗',
                item['edit']
            ) : '',
            item['details'],
            item['name'],
            item['children'].length === 0 ? '' : `<ul>${generateList(item["children"], auth)}</ul>`,
            auth ? `<li>${add.format(item["add_child"])}</li>` : ''
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
                item['discovered'] ? '✓' : '✗',
                !item['description'] ? ' off' : '',
                item['toggle_description'],
                item['description'] ? '✓' : '✗',
                item['edit']
            ) : '',
            item['details'],
            item['name'],
            item['children'].length === 0 ? '' : `<ul>${generateList(item['children'], auth)}</ul>`,
            auth ? `<div class="list_column">${add.format(add_div_url)}</div>` : ''
        )
    })

    document.getElementById('list_view').innerHTML = result
}

