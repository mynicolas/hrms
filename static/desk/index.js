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
    var container = $('div#container');

    $(window).resize(function()
    {
        var docWidth = $(document.body).width();
        container.css({
            width: docWidth,
        });        
    });

    var desk = $('div#desk');
    desk.sortable();
    desk.disableSelection();
    // 在桌面添加一个icon
    function addIcon(id, iconPath, name)
    {
        if(name == undefined)
        {
            name = "icon";
        }
        var iconHtml = "<div class = 'icon'>" +
            "<img class = 'iconBody' id = '" + id + "' src = '" + iconPath + "'/>" +
            "<input class = 'iconName' value = '" + name + "'/></div>";        
        desk.append(iconHtml);
    }

    addIcon('allVms', '/static/desk/icons/test.png', 'all instances');
    addIcon('allVms', '/static/desk/icons/test.png');
    addIcon('allVms', '/static/desk/icons/test.png');
    addIcon('allVms', '/static/desk/icons/test.png');
    addIcon('allVms', '/static/desk/icons/test.png');
    addIcon('allVms', '/static/desk/icons/test.png');
    addIcon('allVms', '/static/desk/icons/test.png');
    addIcon('allVms', '/static/desk/icons/test.png');


});