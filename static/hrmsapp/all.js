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
    var thisHost;
    var thisItem;
    var oldValue;
    var newValue;
    var hostItemDiv = $('.hostItem').not('.mac').not('.ips').not('.dogNP');
    hostItemDiv.focus(function()
    {
        $(this).css('background-color', '#ffffff');
        thisItem = $(this).attr('class').split(' ')[1];
        thisHost = $(this).parent().parent().attr('id');
        oldValue = $(this).val();
    });
    hostItemDiv.change(function()
    {
        var savedItem = $(this);
        newValue = $(this).val();
        $.post('/vm/modify/', 'host=' + thisHost + '&item=' + thisItem + '&oldvalue=' + oldValue + '&newvalue=' + newValue, __isSaved);
        function __isSaved(receive)
        {
            if(receive == 'successful')
            {
                savedItem.css('background-color', '#00dd00');
            }
            else if(receive == 'failed')
            {
                savedItem.css('background-color', '#ff0000');
            }
        }
    });

    var deskAllVms = $('div#deskAllVms');
    var addMacs = $('button.addMacs');
    addMacs.click(function()
    {
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/addmacdialog/', 'dialog=macs&host=' + thisVm, renderAddMacDialog);
        function renderAddMacDialog(receive)
        {
            // deskAllVms.append(receive);
            var dialogAddMac = $('div#dialogAddMac');
            // dialogAddMam.dialog({
            //     title: "add mac",
            //     resizable: false,
            //     modal: false,
            //     width: 1200,
            //     height: 300,
            //     buttons: {
            //         Submit: function() {
            //             console.log('test');
            //         }
            //         Cancel: function() {
            //             $(this).dialog("close");
            //         }
            // });
        }
    });
});