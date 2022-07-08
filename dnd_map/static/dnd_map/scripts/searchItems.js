const template = '<li><table class="item">{0}{1}</table></li>'
const title = '<tr><td><a href="{0}"><strong>{1}</strong><br><em>{2}</em></a></td></tr>'
const admin = '<tr><td><a class="toggle{0}" href="{1}">⚑</a><a class="toggle{2}" href="{3}">☰</a><a class="button" ' +
    'href="{4}">✎</a><a class="button" href="{5}">Add</a></td></tr>'

const csrf_token = Cookies.get('csrftoken')

function searchItems(value, div) {
    console.log('button pressed')
    if (value === '')
        return


    $.ajax({
        url: '#',
        type: 'post',
        data: {
            search: value
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: 'json',
        success: function (result) {
            while (div.firstChild) {
                div.removeChild(div.firstChild);
            }

            let result_list = document.createElement('ul')

            result.query.forEach(function (item) {
                result_list.innerHTML += template.format(
                    title.format(
                        item['details'], item['name'], item['type']
                    ),
                    result['auth'] ? admin.format(
                        !item['discovered'] ? ' off' : '',
                        item['toggle_discovered'],
                        !item['description'] ? ' off' : '',
                        item['toggle_description'],
                        item['edit'],
                        item['add_child'],
                    ) : ''
                )
            })

            div.appendChild(result_list)
        }
    })
}
