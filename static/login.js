
/*====================django ajax ======*/

jQuery(document).ajaxSend(function(event, xhr, settings) {
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    function sameOrigin(url) {
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }
    function safeMethod(method) {
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }

    if (!safeMethod(settings.type) && sameOrigin(settings.url)) {
        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    }
});

/*===============================django ajax end===*/

$(document).ready(function()
{
    var loginDialog = $('div#loginDiv');
    var loginDialogHeader = $('div#loginHeader');
    var loginRegister = $('div#loginRegister');
    var loginSubmit = $('div#loginSubmit');
    var registerDialog = $('div#registerDiv');
    var registerDialogHeader = $('div#registerHeader');
    var registerSubmit = $('div#registerSubmit');
    var registerClear = $('div#registerClear');
    var loginDialogMini = $('div#loginDialogMini');
    loginDialogMini.hide();

    registerDialog.hide();

    loginRegister.click(function()
    {
        loginDialog.fadeOut('fast');
        registerDialog.fadeIn('fast');
    });

    dialogDrag(registerDialog, registerDialogHeader);
    dialogDrag(loginDialog, loginDialogHeader);
    // 创建可拖动元素
    // element：需要拖动的元素
    // handler：拖动的手柄
    // 拖动范围的参数，默认为'document'
    function dialogDrag(element, handler, limit)
    {
        var con;
        if(limit == undefined)
        {
            con = 'document';
        }
        else
        {
            con = limit;
        }
        element.draggable({
            handle: handler,
            cursor: 'move',
            containment: con,
            start: function()
            {
                $(this).css({'opacity': '0.3'});
            },
            stop: function()
            {
                $(this).css('opacity', '1')
            }
        });
    }

    $('div#registerClose').click(function()
    {
        registerDialog.fadeOut('fast');
        loginDialog.fadeIn('fast');
    });

    $('div#loginClose').click(function()
    {
        loginDialog.fadeOut('fast');
        loginDialogMini.fadeIn();
    });

    loginDialogMini.click(function()
    {
        loginDialog.fadeIn();
        $(this).fadeOut();
    });

    $('input.registerInputElement').mouseover(function()
    {
        var inputTip = $('div#inputTip');
        var thisId = $(this).attr('id');
        var tip;
        if(thisId == 'loginRegisterUsernameInput' || thisId == 'loginRegisterPasswordInput'
            || thisId == 'loginRegisterPasswordConfirmInput')
        {
            tip = '8 < length < 16';
        }
        else if(thisId == 'loginRegisterEmailInput')
        {
            tip = 'input a true email'
        }

        inputTip.text(tip);
        $(this).mouseout(function()
        {
            inputTip.text('');
        });
    });
});