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
    addIcon('addVm', '/static/desk/icons/test.png', 'add instance');
    addIcon('addNode', '/static/desk/icons/test.png', 'add node');
    addIcon('addIp', '/static/desk/icons/test.png', 'add ip');
    addIcon('addPort', '/static/desk/icons/test.png', 'add dog port');
    addIcon('addMac', '/static/desk/icons/test.png', 'add mac');
    addIcon('test6', '/static/desk/icons/test.png');

    var deskDialog = $('.ui-dialog');
    deskDialog.hide();
    var allIcon = $('img#allVms');
    var hostsDiv = $('div#hostDiv');
    var deskAllVms = $('div#deskAllVms');
    allIcon.click(function()
    {
        $.post('/vm/', 'item=all', renderAll);
        deskAllVms.dialog({
                title: "all instances",
                resizable: false,
                modal: false,
                buttons: {
                    Cancel: function() {
                        $(this).dialog("close");
                    }
                }
        });
    });
    var addIcon = $('img#addVm');
    var deskAddVm = $('div#vmItemDiv');
    deskAddVm.hide();
    var starttime = $('input#startTime');
    var endtime = $('input#endTime');
    (function()
    {
        starttime.datepicker({
            defaultDate: "+1w",
            changeMonth: true,
            numberOfMonths: 1,
            onClose: function(selectedDate) {
                endtime.datepicker("option", "minDate", selectedDate);
            }
        });
        endtime.datepicker({
            defaultDate: "+1w",
            changeMonth: true,
            numberOfMonths: 1,
            onClose: function(selectedDate) {
                starttime.datepicker("option", "maxDate", selectedDate);
            }
        });
    })();
    addIcon.click(function()
    {
        renderNodes();
        renderPorts();
        renderIps();
        renderMacs();
        deskAddVm.dialog({
            title: "add instance",
            resizable: false,
            modal: false,
            buttons: {
                Submit: function() {
                    $('form#addHost').submit();
                }
            }
        });
    });

    function renderAll(receive)
    {
        hostsDiv.empty();
        hostsDiv.append(receive);
    }

    var nodeSelector = $('select#node');
    nodeSelector.click(renderNodes);
    function renderNodes()
    {
        $.post('/vm/nodes/', 'item=nodes', __renderNodes);
        function __renderNodes(receive)
        {
            nodeSelector.empty();
            nodeSelector.append(receive);
        }
    }

    var ipSelector = $('select#ip');
    ipSelector.click(renderIps);
    function renderIps()
    {
        $.post('/vm/ips/', 'item=ips', __renderIps);
        function __renderIps(receive)
        {
            ipSelector.empty();
            ipSelector.append(receive);
        }
    }

    var macSelector = $('select#mac');
    macSelector.click(renderMacs);
    function renderMacs()
    {
        $.post('/vm/macs/', 'item=macs', __renderMacs);
        function __renderMacs(receive)
        {
            macSelector.empty();
            macSelector.append(receive);
        }
    }

    var portsSelector = $('select#dogPort');
    portsSelector.click(renderPorts);
    function renderPorts()
    {
        $.post('/vm/dogports/', 'item=dogports', __renderPorts);
        function __renderPorts(receive)
        {
            portsSelector.empty();
            portsSelector.append(receive);            
        }
    }

    var addNodeIcon = $('img#addNode');
    var deskAddNode = $('div#deskAddNode');
    deskAddNode.hide();
    addNodeIcon.click(function()
    {
        var newNodeInput = $('input[name=newNode]');
        deskAddNode.dialog({
            title: "add node",
            resizable: false,
            modal: false,
            buttons: {
                Submit: function() {
                    $.post('/vm/addnode/', 'newNode=' + newNodeInput.val(), isSaved)
                }
            }
        });

        function isSaved(receive)
        {
            if (receive == 'successful')
            {
                newNodeInput.css('border', '1px solid rgb(0, 255, 0)');
            }
            else
            {
                newNodeInput.css('border', '1px solid rgb(255, 0, 0)')
            }
        }        

    });

    var addIpIcon = $('img#addIp');
    var deskAddIp = $('div#deskAddIp');
    deskAddIp.hide();
    addIpIcon.click(function()
    {
        var newIpInput = $('input[name=newIp]');
        deskAddIp.dialog({
            title: "add node",
            resizable: false,
            modal: false,
            buttons: {
                Submit: function() {
                    $.post('/vm/addip/', 'newIp=' + newIpInput.val(), isSaved)
                }
            }
        });

        function isSaved(receive)
        {
            if (receive == 'successful')
            {
                newIpInput.css('border', '1px solid rgb(0, 255, 0)');
            }
            else
            {
                newIpInput.css('border', '1px solid rgb(255, 0, 0)')
            }
        }    
    });

    var addMacIcon = $('img#addMac');
    var deskAddMac = $('div#deskAddMac');
    deskAddMac.hide();
    addMacIcon.click(function()
    {
        var newMacInput = $('input[name=newMac]');
        deskAddMac.dialog({
            title: "add node",
            resizable: false,
            modal: false,
            buttons: {
                Submit: function() {
                    $.post('/vm/addmac/', 'newMac=' + newMacInput.val(), isSaved)
                }
            }
        });

        function isSaved(receive)
        {
            if (receive == 'successful')
            {
                newMacInput.css('border', '1px solid rgb(0, 255, 0)');
            }
            else
            {
                newMacInput.css('border', '1px solid rgb(255, 0, 0)')
            }
        }    
    });


    var addDogIcon = $('img#addPort');
    var deskAddDog = $('div#deskAddDog');
    deskAddDog.hide();
    addDogIcon.click(function()
    {
        var thisNode = $('select#allNodes');
        var newDogPortInput = $('input[name=newDogPort]');
        _();
        thisNode.click(_);
        function _()
        {   
            $(this).empty();
            $.post('/vm/nodes/', 'item=nodes', __);
            function __(receive)
            {
                var thisNodes = $('select#allNodes');
                thisNodes.append(receive);
            }
        };
        deskAddDog.dialog({
            title: "add dog",
            resizable: false,
            modal: false,
            buttons: {
                Submit: function() {
                    if (thisNode == '')
                    {
                        thisNode.css('border', '1px solid rgb(255, 0, 0)');
                    }
                    else
                    {
                        $.post('/vm/adddog/',
                            'dogPort=' + newDogPortInput.val() +
                            '&node=' + thisNode.val(),
                            isSaved);
                    }
                }
            }
        });

        function isSaved(receive)
        {
            if (receive == 'successful')
            {
                newDogPortInput.css('border', '1px solid rgb(0, 255, 0)');
            }
            else
            {
                newDogPortInput.css('border', '1px solid rgb(255, 0, 0)')
            }
        } 
    });

});