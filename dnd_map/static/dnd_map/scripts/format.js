String.prototype.format = function () {
    let args = arguments
    return this.replace(/{(\d+)}/g, function (match, index) {
        return typeof args[index] == 'undefined' ? match : args[index]
    })
}
