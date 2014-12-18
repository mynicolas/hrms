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
    var startButton = $('button#start');
    var startMenu = $('ul#startMenu');
    startMenu.hide();

    startMenu.menu();

    startButton.click(function()
    {
        startMenu.toggle();
    });

    var username = $('div#username');
    username.click(function()
    {
        var oldPassword = $('input#changeOldPassword');
        var newPassword = $('input#changeNewPassword');
        var pswdConfirm = $('input#changePswdConfirm');  
        var changePasswordDiv = $('div#changePasswordDiv');      
        oldPassword.removeClass().addClass('changePasswordInput').val('');
        newPassword.removeClass().addClass('changePasswordInput').val('');
        pswdConfirm.removeClass().addClass('changePasswordInput').val('');
        changePasswordDiv.removeClass();
        $("input.changePasswordInput").focus(function()
        {
            $(this).removeClass();
            changePasswordDiv.removeClass();
        });
        newPassword.blur(function()
        {
            var reg = /^$/;
        });
        var changePasswordDialog = $('div#changePasswordDialog');
        changePasswordDialog.dialog({
            title: 'change password',
            width: 240,
            resizable: false,
            focus: function() {$(this).css('background-color', '#ffffff')},
            buttons: {
                Submit: function() {
                    if (oldPassword.val() != '' && newPassword.val() != '' && pswdConfirm.val() != '')
                    {
                        if (newPassword.val() == pswdConfirm.val())
                        {
                            if (matchType('password', newPassword.val()))
                            {
                                $.post('/login/changepassword/', '&oldpassword=' + $.md5(oldPassword.val()) + '&newpassword=' + $.md5(newPassword.val()), __isChanged);
                                function __isChanged(receive)
                                {
                                    if (receive == 'successful')
                                    {
                                        changePasswordDiv.addClass('isChanged');
                                    }
                                    else if(receive == 'failed')
                                    {
                                        changePasswordDiv.addClass('notChanged');
                                    }
                                    else if(receive == 'notmatch')
                                    {
                                        oldPassword.addClass('pswdNotMatch');
                                    }
                                }
                            }
                            else
                            {
                                alert('password must contain @#$%^&*...')
                            }
                        }
                        else 
                        {
                            pswdConfirm.removeClass().addClass('pswdNotMatch');
                        }
                    }
                }
            }
        });
    });

    function matchType(type, value)
    {// 判断用户输入的数据类型
        var reg;
        if(type == 'password')
        {
            reg = /[~!@#$%^&*()_+`\-=]+/;
            if(value.search(reg) < 0)
            {
                return false;
            }
            else
            {
                reg = /[a-z0-9]+/
                if(value.search(reg) < 0)
                {
                    return false;
                }
                else
                {
                    reg = /.{8,14}/
                    if(reg.test(value))
                    {
                        return true;
                    }
                    else
                    {
                        return false;
                    }
                }
            }
        }
        else
        {
            return true;
        }
    }

});