let max_depth = null

function generateItem(item, auth) {
    let table = document.createElement('table')
    table.classList.add('item')

    let tr_title = document.createElement('tr')
    tr_title.innerHTML = `<td><a href="${item['details']}"><strong>${item['name']}</strong><br><em>${item['type']}</em></a></td>`

    table.append(tr_title)

    if (item['children'].length !== 0) {
        tr_title.innerHTML += `<td rowspan="2"><button class="toggle" onclick="collapse(this)">⮟</button></td>`
    }

    if (auth) {
        let admin = `<tr><td><a class="toggle${item['discovered'] ? '' : ' off'}" ` +
            `href="${item['toggle_discovered']}">⚑</a><a class="toggle${item['description'] ? '' : ' off'}" ` +
            `href="${item['toggle_description']}">☰</a><a class="button" href="${item['edit']}">✎</a>`

        if (item['depth'] < max_depth - 1) {
            admin += `<a class="button" href="${item['add_child']}">Add</a>`
        }

        admin += '</td></tr>'

        table.innerHTML += admin
    }

    if (item['children'].length !== 0) {
        let ul_children = document.createElement('ul')
        table.append(ul_children)

        item['children'].forEach(function (child) {
            let child_item = generateItem(child, auth)
            let li_child = document.createElement('li')
            li_child.append(child_item)
            ul_children.append(li_child)
        })
    }

    return table
}

function collapse(obj) {
    let button = obj
    let table = obj.parentNode.parentNode.parentNode.parentNode
    button.classList.toggle('off')
    if (button.textContent === '⮟') {
        table.getElementsByTagName('ul')[0].hidden = true
        button.textContent = '⮜'
    } else {
        table.getElementsByTagName('ul')[0].hidden = false
        button.textContent = '⮟'
    }
}

function populateListView(json, auth, add_div_url) {
    const div = document.getElementById('list_view')
    const data = JSON.parse(json)
    max_depth = data['max_depth']
    const items = data['items']

    console.log(data)

    items.forEach(function (item) {
        let div_item = document.createElement('div')
        div_item.classList.add('list_column')
        div_item.append(generateItem(item, auth))
        div.append(div_item)
    })

    if (auth) {
        let div_append = document.createElement('div')
        div_append.classList.add('list_column')
        div_append.innerHTML = `<a class="button" href="${add_div_url}">+</a>`
        div.append(div_append)
    }
}
