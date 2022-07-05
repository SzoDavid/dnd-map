const admin = '<tr><td><a class="toggle{0}" href="{1}">⚑</a><a class="toggle{2}" href="{3}">☰</a><a class="button" ' +
    'href="{4}">✎</a><a class="button" href="{5}">Add</a></td></tr>'
const div = '<div class="list_column"><table class="item"><tr><td><a href="{0}">{1}</a></td></tr>{2}</table><ul>{3}</ul></div>'
const li = '<li><table class="item"><tr><td><a href="{0}">{1}</a></td></tr>{2}</table><ul>{3}</ul></li>'

let max_depth = null

function generateList(items, auth) {
    let result = ''

    items.forEach(function (item) {
        result += li.format(
            item['details'],
            `<strong>${item['name']}</strong><br><em>${item['type']}</em>`,
            auth ? admin.format(
                !item['discovered'] ? ' off' : '',
                item['toggle_discovered'],
                !item['description'] ? ' off' : '',
                item['toggle_description'],
                item['edit'],
                item['add_child']
            ) : '',
            item['children'].length === 0 ? '' : `${generateList(item['children'], auth)}`,
        )
    })

    return result
}

function populateListView(json, auth, add_div_url) {
    const items = JSON.parse(json)

    let result = ''

    items.forEach(function (item) {
        if (max_depth == null) {
            max_depth = item['max_depth']
        } else {
            result += div.format(
                item['details'],
                `<strong>${item['name']}</strong><br><em>${item['type']}</em>`,
                auth ? admin.format(
                    !item['discovered'] ? ' off' : '',
                    item['toggle_discovered'],
                    !item['description'] ? ' off' : '',
                    item['toggle_description'],
                    item['edit'],
                    item['add_child'],
                ) : '',
                item['children'].length === 0 ? '' : `${generateList(item['children'], auth)}`,
            )
        }
    })

    if (auth) {
        result += `<div class="list_column"><a class="button" href="${add_div_url}">+</a></div>`
    }

    document.getElementById('list_view').innerHTML = result
}

