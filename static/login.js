
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

    // 当点击loginDialog中的register按钮时，loginDialog消失，registerDialog出现
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

    // 当点击registerDialog的关闭按钮时，registerDialog关闭，loginDialog出现
    $('div#registerClose').click(function()
    {
        registerDialog.fadeOut('fast');
        loginDialog.fadeIn('fast');
    });

    // 当点击loginDialog的关闭按钮时，loginDialog最小化
    $('div#loginClose').click(function()
    {
        loginDialog.fadeOut('fast');
        loginDialogMini.fadeIn();
    });

    // 当点击loginDialog的最小化按钮时，loginDialog对话框最大化
    loginDialogMini.click(function()
    {
        loginDialog.fadeIn();
        $(this).fadeOut();
    });

    // 当鼠标移到input上时，出现提示，移出时提示消失
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

    // 当点击registerDialog中的clear按钮时，registerDialog中的所有input清空
    registerClear.click(function()
    {
        $('input.registerInputElement').val('');
    });

    // url: post的地址
    // content: post的内容
    // return: xml文档
    function post(url, content, func)
    {
        var xmlhttp;
        if (window.XMLHttpRequest)
        {// code for IE7+, Firefox, Chrome, Opera, Safari
            xmlhttp = new XMLHttpRequest();
        }
        else
        {// code for IE6, IE5
            xmlhttp = new ActiveXObject("Microsoft.XMLHTTP");
        }
        xmlhttp.onreadystatechange = function()
        {
            if(xmlhttp.readyState == 1 || xmlhttp.readyState == 2
                || xmlhttp.readyState == 3)
            {
                return false;
            }
            else if(xmlhttp.readyState == 4 && xmlhttp.status == 200)
            {
                var receive = xmlhttp.responseText;
                if(func != undefined)
                {
                    func(receive);
                }
            }
        };
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send(content);
    }

    // 登陆
    loginSubmit.click(function()
    {
        var username = $('input#usernameInput').val();
        var password = $('input#passwordInput').val();
        if(username != '' && password != '')
        {
            post('/login/', 'username=' + username + '&password=' + password, checkLogin);
        }
    });

    // 检查登陆状态，如果登陆失败，弹出提示
    function checkLogin(receive)
    {
        if(receive == 'error')
        {
            createTipDialog($('div#loginDiv'), 'Login failed, try again?');
        }
        else
        {
            location.href = '/index/';
        }
    }

    // 定义两个全局变量存储新注册的用户名和密码
    var newUsername;
    var newPassword;
    // 当点击registerDialog中的submit按钮时，提交注册新用户信息
    registerSubmit.click(function()
    {
        var username = $('input#loginRegisterUsernameInput').val();
        var password = $('input#loginRegisterPasswordInput').val();
        var pswdConfirm = $('input#loginRegisterPasswordConfirmInput').val();
        var email = $('input#loginRegisterEmailInput').val();
        if(!matchType('username', username))
        {
            alert('username\'s type is wrong');
        }
        else if(!matchType('password', password))
        {
            alert('password\'s type is wrong');
        }
        else if(!matchType('password', pswdConfirm))
        {
            alert('confirm password\'s type is wrong');
        }
        else if(!matchType('email', email))
        {
            alert('email\'s type is wrong');
        }
        if(matchType('username', username) && matchType('password', password)
            && matchType('password', pswdConfirm) && matchType('email', email))
        {
            if(password == pswdConfirm)
            {
                post('/register/', 'username=' + username + '&password=' + password + '&email=' + email, registered);
                newUsername = username;
                newPassword = password;
            }
            else
            {
                registerFailed();
            }
            function registerFailed()
            {
                alert('two password aren\'t same');
            }
        }
        else
        {
            alert('Check the type you inputed')
        }
    });

    /* tipDialog start */
    (function()
    {
        var thisDialogDiv = "<div id='tipDialogDiv'>" +
                        "<div id='tipDialogHeader'><div id='tipDialogClose'>x</div></div>" +
                        "<div id='tipDialogContent'></div>" +
                        "<div id='tipDialogButton'>OK</div>" +
                    "</div>";
        $('div#container').append(thisDialogDiv);
        $('div#tipDialogDiv').hide();
    })();
    // 设置tipDialog的内容
    function setTipContent(content)
    {
        $('div#tipDialogContent').html(content);
    }
    // 创建tipDialog
    // content：dialog内容
    function createTipDialog(parent, content)
    {
        parent.fadeOut('fast');
        setTipContent(content);
        $('div#tipDialogDiv').fadeIn('fast');
    }
    // 关闭Dialog
    function tipDialogClose()
    {
        $('div#tipDialogDiv').fadeOut('fast');
        $('div#loginDiv').fadeIn('fast');
    }
    $('div#tipDialogButton').click(function()
    {
        tipDialogClose();
        $('input#usernameInput').val(newUsername);
        $('input#passwordInput').val(newPassword);
    });
    $('div#tipDialogClose').click(function()
    {
        tipDialogClose();
        $('input#usernameInput').val(newUsername);
        $('input#passwordInput').val(newPassword);
    });

    /* tipDialog end */

    // 如果注册成功
    function registered(receive)
    {
        createTipDialog($('div#registerDiv'), 'Register successful, hope to login?');
    }

    // 检测输入的值的类型是否符合所给类型
    // type：给出的类型
    // valua：需要检测的值
    // return：boolean
    function matchType(type, value)
    {
        var reg;
        if(type == 'username' || type == 'password')
        {
            reg = /^[a-zA-Z]+[0-9]+$/;
            return reg.test(value);
        }
        else if(type == 'email')
        {
            reg = /^[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?$/;
            return reg.test(value);
        }
    }

});