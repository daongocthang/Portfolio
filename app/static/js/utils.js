function removeClassStartingWith(el, s) {
    if (typeof el === 'undefined') return;
    el.removeClass(function (index, className) {
        return (className.match(new RegExp("\\S*" + s + "\\S*", 'g') || [])).join(' ');
    })
}

function renderFormErrors(data) {
    let obj = JSON.parse(data);
    $('.help-block').remove();
    $('.form-group').removeClass('has-error');
    for (let key in obj) {
        if (obj.hasOwnProperty(key)) {
            $('<p class="help-block">' + obj[key] + '</p>')
                .insertAfter('#' + key);
            $('#' + key).parent().addClass('has-error');
        }
    }
}

function checkboxAjax(el, url, resp) {
    if (typeof el === 'undefined') return;

    let csrf_token = $('meta[name=csrf-token]').attr('content');

    el.bind('click', function () {
        $.ajax({
            url: url,
            type: 'POST',
            headers: {
                "X-CSRFToken": csrf_token,
            },
            data: {
                'name': $(this).attr('name'),
                'value': $(this).attr('value'),
                'checked': $(this).is(':checked') ? 1 : 0
            },
            success: resp
        });

        $.ajaxSetup({
            beforeSend: function (xhr, settings) {
                if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                    xhr.setRequestHeader("X-CSRFToken", csrf_token)
                }
            }
        });
    });
}