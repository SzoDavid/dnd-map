const csrf_token = Cookies.get('csrftoken')

function toggle_value(obj, url) {
    const value = obj.classList.contains('off')

    $.ajax({
        url: url,
        type: 'post',
        data: {
            'value': value
        },
        headers: {
            'X-CSRFToken': csrf_token
        },
        dataType: 'json',
        success: function () {
            location.reload()
        }
    })
}
