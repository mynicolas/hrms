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
    {// 桌面根据浏览器大小自动调整
        var docWidth = $(document.body).width();
        container.css({
            width: docWidth,
        });        
    });

    var desk = $('div#desk');
    desk.sortable();
    desk.disableSelection();

    // 在桌面添加一个icon
    // id: 需要指定该icon的id
    // iconPath: 需要指定该icon图片的路径
    // name: 该icon的名字，可忽略
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
    addIcon('user', '/static/desk/icons/test.png', 'user');
    addIcon('log', '/static/desk/icons/test.png', 'log');


    var deskDialog = $('.ui-dialog');
    deskDialog.hide();
    var allIcon = $('img#allVms');
    var deskAllVms = $('div#deskAllVms');
    allIcon.click(getAll);
    function getAll()
    {
        $.post("/static/hrmsapp/all.js", '', function(receive){$(body).append()});
    }
    function getAll()
    {// 所有实例的icon
        $.post('/vm/', 'item=all', renderAll);
        deskAllVms.dialog({
                title: "all instances",
                resizable: true,
                modal: false,
                width: 1200,
                height: 300,
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

        $('div#hosts').children().filter(':odd').each(function()
        {
            $(this).css('background-color', '#1681B8');
        });
        
    }

    var addIcon = $('img#addVm');
    var deskAddVm = $('div#vmItemDiv');
    deskAddVm.hide();
    var starttime = $('input#startTime');
    var endtime = $('input#endTime');
    addIcon.click(addIconClick);
    function addIconClick()
    {// 添加实例的icon
        renderNodes();
        renderIps();
        renderMacs();
        var thisNode = $('select#node');
        thisNode.change(function()
        {
            renderPorts($(this).val());
        });

        deskAddVm.dialog({
            title: "add instance",
            resizable: false,
            modal: false,
            buttons: {
                Submit: __addHost
            }
        });
        function __addHost()
        {
            var vmName = $('input#vmName').val();
            var vcpus = $('input#vcpus').val();
            var mem = $('input#mem').val();
            var disk = $('input#disk').val();
            var startTime = $('input#startTime').val();
            var endTime = $('input#endTime').val();
            var bandwidth = $('input#bandwidth').val();
            var company = $('input#company').val();
            var dogSn = $('input#dogSn').val();
            var dogPort = $('select#dogPort').val();
            var node = $('select#node').val();
            var ip = $('select#ip').val();
            var mac = $('select#mac').val();
            $.post('/vm/add/',
                'vmname=' + vmName +
                '&vcpus=' + vcpus +
                '&mem=' + mem +
                '&datadisk=' + disk +
                '&nodehost=' + node +
                '&starttime=' + startTime +
                '&endtime=' + endTime +
                '&bandwidth=' + bandwidth +
                '&company=' + company +
                '&dogsn=' + dogSn +
                '&dogport=' + dogPort +
                '&ip=' + ip +
                '&mac=' + mac,
                isSaved
            );
            function isSaved(receive)
            {
                var vmItemDiv = $('div#vmItemDiv');
                if (receive == 'successful')
                {
                    vmItemDiv.css('border', '1px solid rgb(0, 255, 0)');
                    addIconClick();
                }
                else
                {
                    vmItemDiv.css('border', '1px solid rgb(255, 0, 0)');
                }
            }
        }
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
    }

    var nodeSelector = $('select#node');
    function renderNodes()
    { // 渲染所有node
        $.post('/vm/nodes/', 'item=nodes', __renderNodes);
        function __renderNodes(receive)
        {
            nodeSelector.empty();
            nodeSelector.append(receive);
            renderPorts($('select#node').val());
        }
    }

    var ipSelector = $('select#ip');
    function renderIps()
    { // 渲染所有ip
        $.post('/vm/ips/', 'item=ips', __renderIps);
        function __renderIps(receive)
        {
            ipSelector.empty();
            ipSelector.append(receive);
        }
    }

    var macSelector = $('select#mac');
    function renderMacs()
    { // 渲染所有mac
        $.post('/vm/macs/', 'item=macs', __renderMacs);
        function __renderMacs(receive)
        {
            macSelector.empty();
            macSelector.append(receive);
        }
    }

    var portsSelector = $('select#dogPort');
    function renderPorts(node)
    { // 渲染所有dog port
        $.post('/vm/dogports/', 'node=' + node, __renderPorts);
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
    { // 添加node的icon
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
    { // 添加ip的icon
        var newIpInput = $('input[name=newIp]');
        deskAddIp.dialog({
            title: "add ip",
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
    { // 添加mac的icon
        var newMacInput = $('input[name=newMac]');
        deskAddMac.dialog({
            title: "add mac",
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


    var addPortIcon = $('img#addPort');
    var deskAddPort = $('div#deskAddPort');
    deskAddPort.hide();
    addPortIcon.click(function()
    { 
        var thisNode = $('select#allNodes');
        thisNode.empty();
        var newDogPortInput = $('input[name=newPort]');
        _();
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
        deskAddPort.dialog({
            title: "add dog port",
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


    var userIcon = $('img#user');
    var deskUser = $('div#deskUser');
    deskUser.hide();
    userIcon.click(function()
    { // user的icon
        $('div#usersDiv').empty();
        deskUser.dialog({
            title: "user",
            resizable: false,
            modal: false,
            width: 1140,
            height: 300,
            close: function(){$(this).dialog("destroy")},
            buttons: {
                Submit: function() {
                    $(this).dialog("destroy");
                },
                Register: function() {
                    $('form[name=register]').css('background-color', '#ffffff');
                    $('input#usernameInput').removeClass().addClass('notRegistered').val('');
                    $('input#passwordInput').css({
                        'border': '1px solid #A9A8A8',
                        'width': '100%'
                    }).val('');
                    $('input#pswdConfirmInput').css({
                        'border': '1px solid #A9A8A8',
                        'width': '100%'
                    }).val('');

                    var registerDialog = $('div#registerDialogDiv');
                    registerDialog.dialog({
                        title: "register",
                        modal: true,
                        resizable: false,
                        focus: function() {
                            $(this).css('background-color', '#ffffff');
                        },
                        close: function(){$(this).dialog("destroy")},
                        buttons: {
                            Submit: function() {
                                var usernameInput = $('input#usernameInput');
                                var passwordInput = $('input#passwordInput');
                                var pswdConfirmInput = $('input#pswdConfirmInput');
                                if(usernameInput.val() != '')
                                {
                                    if (passwordInput.val() == pswdConfirmInput.val())
                                    {
                                        if(passwordInput.val() == '' || pswdConfirmInput == '')
                                        {
                                            passwordInput.css('border', '1px solid rgb(255, 0, 0)');
                                            pswdConfirmInput.css('border', '1px solid rgb(255, 0, 0)');
                                        }
                                        else
                                        {
                                            $.post('/login/register/', 'username=' + usernameInput.val() + '&password=' + passwordInput.val(), __isSaved);
                                            function __isSaved(receive)
                                            {
                                                if(receive == 'successful')
                                                {
                                                    $('form[name=register]').css('background-color', '#00ff00');
                                                }
                                                else
                                                {
                                                    $('form[name=register').css('background-color', '#ff00ff');
                                                }
                                            }
                                            
                                        }
                                    }
                                    else
                                    {
                                        pswdConfirmInput.css('border', '1px solid rgb(255, 0, 0)');
                                    }
                                }
                            },
                            Close: function() {
                                $(this).dialog('destroy');
                            }
                        }
                    });

                    // 注册对话框中的用户名输入框失焦时，向服务器判断该用户名是否已被注册
                    var usernameInput = $('input#usernameInput');
                    var passwordInput = $('input#passwordInput');
                    var pswdConfirmInput = $('input#pswdConfirmInput');
                    usernameInput.focus(function()
                        {
                            $(this).css('width', '100%');
                    });
                    passwordInput.focus(function()
                    {
                        $(this).css({
                            'width': '100%',
                            'border': '1px solid #A9A8A8'
                        });
                    });
                    pswdConfirmInput.focus(function()
                    {
                        $(this).css({
                            'width': '100%',
                            'border': '1px solid #A9A8A8'
                        });
                    });
                    usernameInput.blur(checkUser);
                    function checkUser() 
                    {
                        if (usernameInput.val() != '')
                        {
                            $.post('/login/checkuser/', 'username=' + usernameInput.val(), __isRegister);
                        }
                        else
                        {
                            usernameInput.removeClass('isRegistered notRegistered');
                        }
                        // 如果该用户名已被注册，将注册对话框的边框设置为红色, 如果未被注册，设置为绿色
                        function __isRegister(receive)
                        {
                            if (receive == 'failed')
                            {
                                usernameInput.removeClass().addClass('isRegistered');
                            }
                            else if (receive == 'successful')
                            {
                                usernameInput.removeClass().addClass('notRegistered')
                            }
                        }
                    }
                }
            }
        });

        $.post('/user/', 'user=all', renderUsers);
        function renderUsers(receive)
        {
            var thisUser;
            var oldQuery = ',';
            var oldModify = ',';
            var newQuery = ',';
            var newModify = ',';
            var usersDiv = $('div#usersDiv')
            usersDiv.append(receive);

            var permItem = $('input.aUserPermissionItem');
            $('div.aUserPermissionDiv').mouseenter(function()
            {
                thisUser = $(this);
                var oldQueryChecked = thisUser.children().children().children().filter('.queryItem').filter(':checked');
                var oldModifyChecked = thisUser.children().children().children().filter('.modifyItem').filter(':checked');
                oldQueryChecked.each(function()
                {
                    oldQuery += $(this).attr('name') + ',';
                });
                oldModifyChecked.each(function()
                {
                    oldModify += $(this).attr('name') + ',';
                });
            });
            permItem.change(function()
            {
                thisChecked = $(this);
                newQuery = ',';
                newModify = ',';
                var newQueryChecked = thisUser.children().children().children().filter('.queryItem').filter(':checked');
                var newModifyChecked = thisUser.children().children().children().filter('.modifyItem').filter(':checked');
                newQueryChecked.each(function()
                {
                    newQuery += $(this).attr('name') + ',';
                });
                newModifyChecked.each(function()
                {
                    newModify += $(this).attr('name') + ',';
                });

                $.post('/user/changeperm/',
                    'username=' + thisUser.attr('id') +
                    '&oldquery=' + oldQuery +
                    '&newquery=' + newQuery +
                    '&oldmodify=' + oldModify +
                    '&newmodify=' + newModify,
                    isSaved);

                function isSaved(receive)
                {
                    if(receive == 'successful')
                    {
                        thisChecked.parent().css('background-color', '#00ff00');
                    }
                    else
                    {
                        thisChecked.parent().css('background-color', "ff0000");
                    }
                }
            });

            $('div.aUserPermissionDiv').mouseleave(function()
            {
                oldQuery = ',';
                oldModify = ',';
                newQuery = ',';
                newModify = ',';
            });
        }
    });

    
    var logIcon = $('img#log');
    var deskLogDiv = $('div#deskLogDiv');
    deskLogDiv.hide();
    logIcon.click(function()
    { // log 的icon
        deskLogDiv.dialog({
            title: "log",
            resizable: true,
            modal: false,
            width: 1000,
            height: 500,
            close: function(){$(this).dialog("close")},
            buttons: {
                Query: function() {
                    var conditionLogDiv = $('div#conditionLogDiv');
                    conditionLogDiv.dialog({
                        title: "log query",
                        resizable: true,
                        modal: true,
                        width: 230,
                        height: 230,
                        close: function(){$(this).dialog("destroy")},
                        buttons: {
                            Submit: function() {
                                var hostName = $('select#logQueryHostName').val();
                                var startTime = $('input#logQueryStartTime').val();
                                var endTime = $('input#logQueryEndTime').val();
                                $.post(
                                    'log/conditionlog/',
                                    'hostname=' + hostName +
                                    '&starttime=' + startTime +
                                    '&endtime=' + endTime,
                                    __query
                                    )
                                function __query(receive)
                                {
                                    deskLogDiv.empty();
                                    deskLogDiv.append(receive); 
                                }
                            }
                        }   
                    });
                    
                    var vmNameSelector = $('select#logQueryHostName');
                    $.post('/log/vmnames/', '', renderVmNames);
                    function renderVmNames(receive)
                    {
                        vmNameSelector.empty();
                        vmNameSelector.append(receive);
                    }
                    
                    function getDate()
                    {
                        var date = new Date();
                        var year = date.getFullYear()
                        var month = date.getMonth() + 1
                        var day = date.getDate()
                        return month + "/" + day + "/" + year;
                    }

                    var logQueryStartTime = $('input#logQueryStartTime');
                    var logQueryEndTime = $('input#logQueryEndTime');
                    logQueryStartTime.val(getDate);
                    logQueryEndTime.val(getDate);
                    logQueryStartTime.datepicker({
                        altFormat: "mm/dd/yy",
                        defaultDate: +0,
                        defaultDate: "+1w",
                        changeMonth: true,
                        numberOfMonths: 1,
                        onClose: function(selectedDate)
                            {
                                logQueryEndTime.datepicker("option", "minDate", selectedDate)
                            }
                    });
                    logQueryEndTime.datepicker({
                        altFormat: "mm/dd/yy",
                        defaultDate: +0,
                        defaultDate: "+1w",
                        changeMonth: true,
                        numberOfMonths: 1,
                        onClose: function(selectedDate)
                            {
                                logQueryStartTime.datepicker("option", "maxDate", selectedDate)
                            }
                    });
                }
            }
        });

        $.post('/log/', '', renderLogs);
        function renderLogs(receive)
        {
            deskLogDiv.empty();
            deskLogDiv.append(receive);
        }
    });
});