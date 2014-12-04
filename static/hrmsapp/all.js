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
        var thisMacInput = $(this).prev();
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/addmacdialog/', 'dialog=macs&host=' + thisVm, renderAddMacDialog);
        function renderAddMacDialog(receive)
        {
            var macsDiv = $('div#dialogAddMacDiv');
            var dialogAddMacDiv = $('div#dialogAddMacDiv');
            var dialogAddMac = $('div#dialogAddMac');
            oldValue = macsDiv.children().filter(':checked');
            dialogAddMac.hide();
            dialogAddMacDiv.empty();
            dialogAddMacDiv.append(receive);
            dialogAddMac.dialog({
                title: "add mac",
                resizable: false,
                modal: true,
                width: 210,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        macsChecked = macsDiv.children().filter(':checked');
                        macsChecked.each(function()
                        {
                            newValue += $(this).val() + ',';
                        });
                        $.post('/vm/changecacs/', 'host=' + thisVm + '&oldvalue=' + oldValue + '&newvalue=' + newValue, __isSaved);
                        function __isSaved(receive)
                        {
                            if(receive == "successful")
                            {
                                thisMacInput.css('background-color', '#00dd00');
                            }
                            else
                            {
                                thisMacInput.css('background-color', '#ff0000');
                            }
                        }
                    },
                    Cancel: function() {
                        $(this).dialog("destroy");
                    }
                }
            });
        }
    });


    var addIps = $('button.addIps');
    addIps.click(function()
    {       
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/addipdialog/', 'dialog=ips&host=' + thisVm, renderAddIpDialog);
        function renderAddIpDialog(receive)
        {
            var dialogAddIpDiv = $('div#dialogAddIpDiv');
            var dialogAddIp = $('div#dialogAddIp');
            dialogAddIp.hide();
            dialogAddIpDiv.empty();
            dialogAddIpDiv.append(receive);
            dialogAddIp.dialog({
                title: "add ip",
                resizable: false,
                modal: true,
                width: 210,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        $(this).dialog("widget");
                    },
                    Cancel: function() {
                        $(this).dialog("destroy");
                    }
                }
            });
        }
    });


    var changeNode = $('button.changeNode');
    changeNode.click(function()
    {
        var thisNodeInput = $(this).prev();
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/changenodedialog/', 'dialog=nodes&host=' + thisVm, renderChangeNodeDialog);
        function renderChangeNodeDialog(receive)
        {
            oldValue = thisNodeInput.val();
            var dialogAddDogDiv = $('div#dialogAddDogDiv');
            var dialogAddDog = $('div#dialogAddDog');
            dialogAddDog.hide();
            dialogAddDogDiv.empty();
            dialogAddDogDiv.append(receive);
            dialogAddDog.dialog({
                title: "add node",
                resizable: false,
                modal: true,
                width: 210,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        newValue = $('[name=nodeRadio]:checked').val();
                        $.post('/vm/changeitem/', 'host=' + thisVm + '&change=node' + '&oldvalue=' + oldValue + '&newvalue=' + newValue, __isSaved);
                        function __isSaved(receive)
                        {
                            if(receive == "successful")
                            {
                                thisNodeInput.css('background-color', '#00dd00');
                                thisNodeInput.val(newValue);
                            }
                            else
                            {
                                thisNodeInput.css('background-color', '#ff0000');
                            }
                        }
                    },
                    Cancel: function() {
                        $(this).dialog("destroy");
                    }
                }
            });
        }
    });


    var addDogs = $('button.addDogs');
    addDogs.click(function()
    {       
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/adddogdialog/', 'dialog=dogs&host=' + thisVm, renderAddDogDialog);
        function renderAddDogDialog(receive)
        {
            var dialogAddDogDiv = $('div#dialogAddDogDiv');
            var dialogAddDog = $('div#dialogAddDog');
            dialogAddDog.hide();
            dialogAddDogDiv.empty();
            dialogAddDogDiv.append(receive);
            dialogAddDog.dialog({
                title: "add dog",
                resizable: false,
                modal: true,
                width: 210,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        $(this).dialog("widget");
                    },
                    Cancel: function() {
                        $(this).dialog("destroy");
                    }
                }
            });
        }
    });
});