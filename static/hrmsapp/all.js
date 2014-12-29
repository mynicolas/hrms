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
    function getAll()
    {// 所有实例的icon
        $.post('/vm/', 'item=all', renderAll);
        deskAllVms.dialog({
                title: "all instances",
                resizable: true,
                modal: false,
                width: 1300,
                height: 500,
                buttons: {
                    Cancel: function() {
                        $(this).dialog("close");
                    }
                }
        });
    }

    var hostsDiv = $('div#hostsDiv');
    function renderAll(receive)
    { // 渲染所有实例项目
        hostsDiv.empty();
        hostsDiv.append(receive);
        var hostsDivWidth = 0;
        $('div.aHostItem').first().children().each(function()
        {
            hostsDivWidth += $(this).width();
        });
        hostsDiv.css('width', hostsDivWidth + 'px');
        var starttime = $('.start');
        var endtime = $('.end');
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

        var nodeSelector = $('.node');
        nodeSelector.click(__allNodes);
        function __allNodes()
        {
            thisSelector = $(this);
            $.post('/vm/nodes/', 'item=nodes', __renderNodes);
            function __renderNodes(receive)
            {
                thisSelector.empty();
                thisSelector.append(receive);
            }
        }

        $('div#hosts').children().filter(':even').each(function()
        {
            $(this).css('background-color', '#1681B8');
        });
        
    }

    var thisHost = '';
    var thisItem = '';
    var oldValue = '';
    var newValue = '';
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
        var oldMacs = ',';
        var newMacs = ',';
        var thisMacInput = $(this).prev();
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/addmacdialog/', 'dialog=macs&host=' + thisVm, renderAddMacDialog);
        function renderAddMacDialog(receive)
        {
            var macsDiv = $('div#dialogAddMacDiv');
            var dialogAddMacDiv = $('div#dialogAddMacDiv');
            var dialogAddMac = $('div#dialogAddMac');

            dialogAddMac.hide();
            dialogAddMacDiv.empty();
            dialogAddMacDiv.append(receive);
            dialogAddMac.dialog({
                title: "add mac",
                resizable: false,
                modal: true,
                width: 240,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        macsChecked = macsDiv.children().filter(':checked');
                        macsChecked.each(function()
                        {
                            newMacs += $(this).val() + ',';
                        });
                        if(oldMacs != newMacs)
                        {
                            $.post('/vm/changemacs/', 'host=' + thisVm + '&oldvalue=' + oldMacs + '&newvalue=' + newMacs, __isSaved);
                            $(this).dialog("destroy");
                        }
                        else
                        {
                            newMacs = ',';
                        }
                        function __isSaved(receive)
                        {
                            if(receive == "successful")
                            {
                                getAll();
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
            oldMacsChecked = macsDiv.children().filter(':checked');
            oldMacsChecked.each(function()
            {
                oldMacs += $(this).val() + ',';
            });
        }
    });


    var addIps = $('button.addIps');
    addIps.click(function()
    {
        var oldIps = ',';
        var newIps = ',';
        var thisIpInput = $(this).prev();
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/addipdialog/', 'dialog=ips&host=' + thisVm, renderAddIpDialog);
        function renderAddIpDialog(receive)
        {
            var ipsDiv = $('div#dialogAddIpDiv');
            var dialogAddIpDiv = $('div#dialogAddIpDiv');
            var dialogAddIp = $('div#dialogAddIp');

            dialogAddIp.hide();
            dialogAddIpDiv.empty();
            dialogAddIpDiv.append(receive);
            dialogAddIp.dialog({
                title: "add ip",
                resizable: false,
                modal: true,
                width: 240,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        macsChecked = ipsDiv.children().filter(':checked');
                        macsChecked.each(function()
                        {
                            newIps += $(this).val() + ',';
                        });
                        if(oldIps != newIps)
                        {
                            $.post('/vm/changeips/', 'host=' + thisVm + '&oldvalue=' + oldIps + '&newvalue=' + newIps, __isSaved);
                            $(this).dialog("destroy");
                        }
                        else
                        {
                            newIps = ',';
                        }
                        function __isSaved(receive)
                        {
                            if(receive == "successful")
                            {
                                getAll();
                                thisIpInput.css('background-color', '#00dd00');
                            }
                            else
                            {
                                thisIpInput.css('background-color', '#ff0000');
                            }
                        }
                    },
                    Cancel: function() {
                        $(this).dialog("destroy");
                    }
                }
            });
            oldMacsChecked = ipsDiv.children().filter(':checked');
            oldMacsChecked.each(function()
            {
                oldIps += $(this).val() + ',';
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
            var dialogChangeNodeDiv = $('div#dialogChangeNodeDiv');
            var dialogChangeNode = $('div#dialogChangeNode');
            dialogChangeNode.hide();
            dialogChangeNodeDiv.empty();
            dialogChangeNodeDiv.append(receive);
            dialogChangeNode.dialog({
                title: "add node",
                resizable: false,
                modal: true,
                width: 210,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        newValue = $('[name=nodeRadio]:checked').val();
                        $.post('/vm/changenode/', 'host=' + thisVm + '&change=node' + '&oldvalue=' + oldValue + '&newvalue=' + newValue, __isSaved);
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



    var changeBusinessMan = $('button.changeBusinessMan');
    changeBusinessMan.click(function()
    {
        var thisBusinessManInput = $(this).prev();
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/changeownerdialog/', 'dialog=businessMan&host=' + thisVm, renderChangeBusinessManDialog);
        function renderChangeBusinessManDialog(receive)
        {
            oldValue = thisBusinessManInput.val();
            var dialogChangeBusinessManDiv = $('div#dialogChangeBusinessManDiv');
            var dialogChangeBusinessMan = $('div#dialogChangeBusinessMan');
            dialogChangeBusinessMan.hide();
            dialogChangeBusinessManDiv.empty();
            dialogChangeBusinessManDiv.append(receive);
            dialogChangeBusinessMan.dialog({
                title: "add node",
                resizable: false,
                modal: true,
                width: 210,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        newValue = $('[name=businessManRadio]:checked').val();
                        $.post('/vm/changeowner/', 'host=' + thisVm + '&change=businessMan' + '&oldvalue=' + oldValue + '&newvalue=' + newValue, __isSaved);
                        function __isSaved(receive)
                        {
                            if(receive == "successful")
                            {
                                thisBusinessManInput.css('background-color', '#00dd00');
                                thisBusinessManInput.val(newValue);
                            }
                            else
                            {
                                thisBusinessManInput.css('background-color', '#ff0000');
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


    var changeOwner = $('button.changeOwner');
    changeOwner.click(function()
    {
        var thisOwnerInput = $(this).prev();
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/changeownerdialog/', 'dialog=nodes&host=' + thisVm, renderChangeOwner);
        function renderChangeOwner(receive)
        {
            oldValue = thisOwnerInput.val();
            var dialogChangeOwnerDiv = $('div#dialogChangeOwnerDiv');
            var dialogChangeOwner = $('div#dialogChangeOwner');
            dialogChangeOwner.hide();
            dialogChangeOwnerDiv.empty();
            dialogChangeOwnerDiv.append(receive);
            dialogChangeOwner.dialog({
                title: "change owner",
                resizable: false,
                modal: true,
                width: 210,
                height: 300,
                close: function(){$(this).dialog("destroy")},
                buttons: {
                    Submit: function() {
                        newValue = $('[name=ownerRadio]:checked').val();
                        $.post('/vm/changeowner/', 'host=' + thisVm + '&change=owner' + '&oldvalue=' + oldValue + '&newvalue=' + newValue, __isSaved);
                        function __isSaved(receive)
                        {
                            if(receive == "successful")
                            {
                                thisOwnerInput.css('background-color', '#00dd00');
                                thisOwnerInput.val(newValue);
                            }
                            else
                            {
                                thisOwnerInput.css('background-color', '#ff0000');
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
        var thisDogSN = $(this).prev();     
        var thisVm = $(this).parent().parent().attr('id');
        $.post('/vm/adddogdialog/', 'dialog=dogs&host=' + thisVm, renderAddDogDialog);
        function renderAddDogDialog(receive)
        {
            var oldDogs = ',';
            var newDogs = ',';
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
                        if(newDogs != oldDogs)
                        {
                            var newDogsChecked = dialogAddDogDiv.children().filter(':checked')
                            if(newDogsChecked.length >= 1)
                            {
                                newDogsChecked.each(function()
                                {
                                    newDogs += $(this).next().text() + $(this).next().next().text() + ',';
                                });
                            }
                            else
                            {
                                newDogs = ',-:-,';
                            }
                            if(newDogs != oldDogs)
                            {
                                $.post('/vm/changedogs/', 'host=' + thisVm + '&oldvalue=' + oldDogs + '&newvalue=' + newDogs, __isSaved);
                                function __isSaved(receive)
                                {
                                    if(receive == "successful")
                                    {
                                        getAll();
                                        thisDogSN.css('background-color', '#00dd00');
                                    }
                                    else
                                    {
                                        thisDogSN.css('background-color', '#ff0000');
                                    }
                                }
                                $(this).dialog('destroy');
                            }
                        }
                    },
                    Cancel: function() {
                        $(this).dialog("destroy");
                    }
                }
            });
            var emptyDog = $('input#emptyDog');
            if(thisDogSN.children().length == 0)
            {
                emptyDog.attr('checked', true);
            }
            var dogNotEmpty = dialogAddDogDiv.children().filter('input').not('input#emptyDog');
            dialogAddDogDiv.children().filter('input').change(function()
            {
                if(emptyDog.is(':checked'))
                {
                    dialogAddDogDiv.children().filter('input').not('input#emptyDog').removeAttr('checked')
                }
                if(dogNotEmpty.is(':checked').length == 0)
                {
                    emptyDog.attr('checked', true);
                }
                dogNotEmpty.click(function()
                {
                    emptyDog.attr('checked', false);
                });
            });
            var oldDogsChecked = dialogAddDogDiv.children().filter(':checked');
            if(oldDogsChecked.length >= 1)
            {
                oldDogsChecked.each(function()
                {
                    oldDogs += $(this).next().text() + $(this).next().next().text() + ',';
                });
            }
            else
            {
                oldDogs = ',-:-,';
            }

            var addSn = $('button.addSn');
            var dialogAddSn = $('div#dialogAddSn')
            addSn.click(function()
            {
                var thisDog = $(this).prev();
                dialogAddSn.dialog({
                    title: "add sn",
                    resizable: false,
                    modal: true,
                    width: 210,
                    height: 150,
                    close: function(){$(this).dialog("destroy");},
                    buttons: {
                        Submit: function() {
                            var thisSn = $('input#dialogAddSnInput').val();
                            if(thisSn)
                            {
                                thisDog.text(thisSn);
                                $(this).dialog("destroy");
                            }
                        },
                        Cancel: function() {
                            $(this).dialog("destroy");
                        }
                    }
                });
            });

        }
    });

    $('div#hosts').sortable({
        opacity: 0.5,
        stop: function() {
            var vmSorts = ',';
            var hosts = $('div#hosts').children();
            hosts.each(function()
            {
                vmSorts += $(this).attr('id') + ',';
            });
            $.post('/user/changesort/', 'vmsort=' + vmSorts);
        }
    });

});