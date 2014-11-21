
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
    // 屏蔽F12键
    $('*').keydown(function(e)
    {
        e = window.event || e || e.which;
        if(e.keyCode == 123)
        {
            e.keyCode = 0;
            return false;
        }
    });

    var query = $("div#queryButton");
    var rightWindow = $("div#rightWindowBody");

    query.click(queryAll);
    queryAll();

    function queryAll()
    {
        post('/query/all', 'query=all', renderAll);
    }

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
                func(receive);
            }
        };
        xmlhttp.open("POST", url, true);
        xmlhttp.setRequestHeader("Content-type", "application/x-www-form-urlencoded");
        xmlhttp.send(content);
    }
//
//    // 处理node的post数据
//    // receive： 获取的服务器数据(xml)
//    function renderNode(receive)
//    {
//        var modify = $('#modifyInput');
//        $(receive).find('node').each(function()
//        {
//            modify.append('<option value = "' + $(this).text() + '">' + $(this).text() + '</option>');
//        });
//    }

    // 处理node的ip数据
    // receive： 获取的服务器数据(xml)
    function renderIp(receive)
    {
        var modify = $('#modifyInput');
        $(receive).find('ip').each(function()
        {
            modify.append('<option value = "' + $(this).text() + '">' + $(this).text() + '</option>');
        });
    }

    var tableHeader = "<div id = 'tableHeader'>" +
                            "<div class = 'tableHeaderItem' id = 'hostNameH'>Name</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostCoreH'>Core</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostMemH'>Memory<br/>(M)</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostDiskH'>Disk<br/>(G)</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostMacH'>Mac</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostStartH'>Start Time<br/>(M/D/Y)</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostEndH'>End Time<br/>(M/D/Y)</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostCompanyH'>Company</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostRemotePortH'>Remote Port</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostDogNH'>Dog Sn</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostDogPH'>Dog Port</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostBandwidthH'>BandWidth<br/>(Mbps)</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostNodeH'>Node</div>" +
                            "<div class = 'tableHeaderItem' id = 'hostIpH'>IP</div>" +
                        "</div>";
    rightWindow.prepend(tableHeader);

    // 处理all的post数据
    // recevie： 获取的服务器数据(xml)
    function renderAll(receive)
    {
        var hostsDiv = $('div#hostsDiv');
        hostsDiv.empty();

        var thisColor = false;
        $(receive).find("aHost").each(function()
        {
            var name = $(this).find("name").text();
            var core = $(this).find("core").text();
            var mem = $(this).find("mem").text();
            var disk = $(this).find("disk").text();
            var mac = $(this).find("mac").text();
            var start = $(this).find("start").text();
            var end = $(this).find("end").text();
            var company = $(this).find("company").text();
            var remotePort = $(this).find("remotePort").text();
            var dogN = $(this).find("dogN").text();
            var dogP = $(this).find("dogP").text();
            var bandwidth = $(this).find("bandwidth").text();
            var node = $(this).find("node").text();
            var ip = $(this).find("ip").text();

            var thisHostColor;
            if(thisColor)
            {
                thisHostColor = "#5CDFFF";
            }
            else
            {
                thisHostColor = "rgba(0, 0, 0, 0)";
            }

            hostsDiv.append("<div class = 'aHostDiv' id = '" + name + "'>" + "</div>");
            var aHostDiv = $("div#" + name);
            var aHost = "<div class = 'hostName' name = 'hostItem'>" + name + "</div>" +
                        "<div class = 'hostCore' name = 'hostItem'>" + core + "</div>" +
                        "<div class = 'hostMem' name = 'hostItem'>" + mem + "</div>" +
                        "<div class = 'hostDisk' name = 'hostItem'>" + disk + "</div>" +
                        "<div class = 'hostMac' name = 'hostItem'>" + mac + "</div>" +
                        "<div class = 'hostStart' name = 'hostItem'>" + start + "</div>" +
                        "<div class = 'hostEnd' name = 'hostItem'>" + end + "</div>" +
                        "<div class = 'hostCompany' name = 'hostItem'>" + company + "</div>" +
                        "<div class = 'hostRemotePort' name = 'hostItem'>" + remotePort + "</div>" +
                        "<div class = 'hostDogN' name = 'hostItem'>" + dogN + "</div>" +
                        "<div class = 'hostDogP' name = 'hostItem'>" + dogP + "</div>" +
                        "<div class = 'hostBandwidth' name = 'hostItem'>" + bandwidth + "</div>" +
                        "<div class = 'hostNode' name = 'hostItem'>" + node + "</div>" +
                        "<div class = 'hostIp' name = 'hostItem'>" + ip + "</div>";
            aHostDiv.append(aHost);
            aHostDiv.css('background-color', thisHostColor);
            thisColor = !thisColor;
        });

        // 每一个host都可以拖动,当拖动结束，保存当前排序
        (function () 
        {
            hostsDiv.sortable({
                distance: 15,
                placeholder: "ui-state-highlight",
                stop: saveHostSort
            });         
        })();

        // 生成所有虚拟机的最终排序结果 “vm1,vm2,vm3,...”
        function saveHostSort() 
        {
            var hostNames = new Array();
            var hosts = hostsDiv.children();
            hosts.each(function()
            {
                var thisHostName = $(this).first().attr('id');
                hostNames.push(thisHostName);
            });
            var thisHostSort = hostNames.toString();
            post('/user/instances/', 'sort=' + thisHostSort, isSorted);
        }

        function isSorted (receive)
        {
            if(receive == "successful")
            {
                queryAll();
            }
        }



        // 获取鼠标点击的元素一些关键属性
        function getAttr(element)
        {
            var elementClass = element.attr('class');
            var elementText = element.text();
            var posX = element.offset().left;
            var posY = element.offset().top;
            var thisWidth = element.width();
            var thisHeight = element.height();
            return {
                thisClass: elementClass,
                thisText: elementText,
                thisPos: {x: posX, y: posY},
                thisSize: {w: thisWidth, h: thisHeight}
            }
        }

        // 点击表格内容时，在原位置产生input框
        $("[name='hostItem']:not(.hostName.hostDogP.hostNode)").dblclick(function() {
            var thisElem = $(this);
            var thisAttr = getAttr($(this));
            var thisX = thisAttr.thisPos.x;     // this距左边界的距离
            var thisY = thisAttr.thisPos.y;     // this距上边界的距离
            var thisW = thisAttr.thisSize.w;    // this的宽度
            var thisH = thisAttr.thisSize.h;    // this的高度
            var beforeChange, afterChange;

            $("div#modifyDiv").remove();        // 先将文档中已经存在的修改框清除

            if ($(this).attr('class') != 'hostStart' && $(this).attr('class') != 'hostEnd'
                && $(this).attr('class') != 'hostName' && $(this).attr('class') != 'hostIp'
                && $(this).attr('class') != 'hostNode' && $(this).attr('class') != 'hostDogP')
            {// 如果双击的不是需要输入时间的地方，则在该处生成文本框
                var maxlength;
                if($(this).attr('class') == 'hostCore')
                {
                    maxlength = 2;
                }
                else if($(this).attr('class') == 'hostMem' || $(this).attr('class') == 'hostDisk')
                {
                    maxlength = 5;
                }
                else if($(this).attr('class') == 'hostMac')
                {
                    maxlength = 17;
                }
                else if($(this).attr('class') == 'hostCompany')
                {
                    maxlength = 24;
                }
                else if($(this).attr('class') == 'hostDogN')
                {
                    maxlength = 40;
                }
                else if($(this).attr('class') == 'hostBandwidth')
                {
                    maxlength = 3;
                }
                $(this).after("<div id = 'modifyDiv'><input id = 'modifyInput' maxlength=" + maxlength + "></input>");
                thisElem.hide();
                var modifyDiv = $("div#modifyDiv");
                var modifyInput = $("#modifyInput");
                document.getElementById('modifyInput').value = $(this).text();
                modifyInput.focus();
                beforeChange = $(this).text();
            }
            else if($(this).attr('class') == 'hostName' || $(this).attr('class') == 'hostDogP'
                || $(this).attr('class') == 'hostNode')
            {// 主机名，狗端口，计算节点 不可修改
                $(this).after("<div id = 'modifyDiv'><input id = 'modifyInput'></input>");
                var modifyDiv = $("div#modifyDiv");
                var modifyInput = $("#modifyInput");
                document.getElementById('modifyInput').value = $(this).text();
                modifyDiv.hide();
                beforeChange = $(this).text();
            }
            else if($(this).attr('class') == 'hostIp')
            {// ip地址需要下拉列表
                $(this).after("<div id = 'modifyDiv'><select id = 'modifyInput'></select>");
                thisElem.hide();
                var modifyDiv = $("div#modifyDiv");
                var modifyInput = $("#modifyInput");
                modifyInput.append('<option value = "' + $(this).text() + '">' + $(this).text() + '</option>');
                modifyInput.focus();
                beforeChange = $(this).text();
            }
            else if($(this).attr('class') == 'hostStart' || $(this).attr('class') == 'hostEnd')
            {// 如果双击的是需要输入时间的地方，则在该处生成时间选择框
                $(this).after("<div id = 'modifyDiv'><input id = 'modifyInput'></input>");
                thisElem.hide();
                var modifyDiv = $("div#modifyDiv");
                var modifyInput = $("#modifyInput");

                $(function()
                {// 当文本框生成的时候就生成时间选择器
                    $("#modifyInput").datepicker();
                });
                $.datepicker.setDefaults(
                {// 设置时间选择器产生的方式，当文本框获得焦点的时候产生
                    showOn: "focus"
                });
                document.getElementById('modifyInput').value = $(this).text();
                modifyInput.focus();
                beforeChange = $(this).text();
            }

            // 当鼠标在整个文档中单击的时候将文本框或者时间选择框中的内容替换给原来位置的div
            $(document).click(function(e)
            {
                if($(e.target).attr('id') != 'modifyInput'
                    && $(e.target).attr('id') != 'ui-datepicker-div'
                    && $(e.target).attr('class') != 'ui-datepicker-header ui-widget-header ui-helper-clearfix ui-corner-all'
                    && $(e.target).attr('class') != 'ui-datepicker-prev ui-corner-all'
                    && $(e.target).attr('class') != 'ui-icon ui-icon-circle-triangle-w'
                    && $(e.target).attr('class') != 'ui-datepicker-next ui-corner-all'
                    && $(e.target).attr('class') != 'ui-icon ui-icon-circle-triangle-e'
                    && $(e.target).attr('class') != 'ui-datepicker-week-end ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled'
                    && $(e.target).attr('class') != 'ui-datepicker-other-month ui-datepicker-unselectable ui-state-disabled'
                    && $(e.target).attr('class') != 'ui-datepicker-title'
                    && $(e.target).attr('class') != 'ui-datepicker-month'
                    && $(e.target).attr('class') != 'ui-datepicker-year'
                    && $(e.target).attr('class') != 'ui-datepicker-calendar'
                    && $(e.target).attr('class') != 'ui-datepicker-week-end'
                    && $(e.target).nodeName != 'TD'
                    && $(e.target).attr('title') != 'Monday'
                    && $(e.target).attr('title') != 'Tuesday'
                    && $(e.target).attr('title') != 'Wednesday'
                    && $(e.target).attr('title') != 'Thursday'
                    && $(e.target).attr('title') != 'Friday'
                    && $(e.target).attr('title') != 'Saturday'
                    && $(e.target).attr('title') != 'Sunday')
                {// 如果单击的位置不是文本框时，将文本框中的内容替换给原来位置的div，并解绑单击事件
                    var modifyDiv = $('#modifyDiv');
                    var modifyValue = document.getElementById('modifyInput').value;
                    var modifyPrevious = modifyDiv.prev().attr('class');
                    /* test input type start */
                    var modifyType;
                    if(modifyPrevious == 'hostCore' || modifyPrevious == 'hostMem'
                        || modifyPrevious == 'hostDisk' || modifyPrevious == 'hostRemotePort'
                        || modifyPrevious == 'hostRemotePort' || modifyPrevious == 'hostBandwidth')
                    {
                        modifyType = "digital";
                    }
                    else if(modifyPrevious == 'hostMac')
                    {
                        modifyType = 'mac';
                    }
                    else if(modifyPrevious == 'hostDogN')
                    {
                        modifyType = 'dogsn';
                    }
                    else if(modifyPrevious == 'hostStart' || modifyPrevious == 'hostEnd')
                    {
                        modifyType = 'date';
                    }
                    else if(modifyPrevious == 'hostIp')
                    {
                        modifyType = 'ip';
                    }
                    else if(modifyPrevious == 'hostCompany')
                    {
                        modifyType = 'zhtext';
                    }
                    else if(modifyPrevious == 'hostName' || modifyPrevious == 'hostNode')
                    {
                        modifyType = 'notChange';
                    }
                    else if(modifyPrevious == 'hostDogP')
                    {
                        modifyType = 'dogport';
                    }
                    var isMatchType = checkInputType(modifyType, modifyValue);
                    /* test input type end */

                    afterChange = document.getElementById('modifyInput').value;
                    var isChange = isChanged(beforeChange, afterChange);
                    if(isMatchType)
                    {
                        if(isChange)
                        {
                            if(modifyDiv.prev().attr('class') == 'hostIp')
                            {
                                post('/query/ip', 'hostName=' + modifyDiv.parent().attr('id') +
                                    '&originalIp=' + beforeChange + '&newIp=' + afterChange, function () {
                                    return true;
                                });
                                thisElem.text(afterChange);
                                modifyDiv.remove();
                                thisElem.show();
                                $(document).unbind('click');
                            }
                            else if(modifyDiv.prev().attr('class') == 'hostCompany')
                            {
                                modifyData(modifyDiv.prev(), afterChange);

                                thisElem.text(afterChange);
                                modifyDiv.remove();
                                thisElem.show();

                                $(document).unbind('click');
//                                queryAll();
                            }
                            else
                            {
                                modifyData(modifyDiv.prev(), afterChange);

                                thisElem.text(afterChange);
                                modifyDiv.remove();
                                thisElem.show();
                                $(document).unbind('click');
                            }

                        }
                        else
                        {
                            thisElem.text(afterChange);
                            modifyDiv.remove();
                            thisElem.show();
                            $(document).unbind('click');
                        }
                    }
                    else
                    {
                        alert('Value type is not matched');
                    }
                }
            });

            $(this).text(document.getElementById('modifyInput').value);

            var modifyDivCss = {
                'float': 'left',
                'width': thisW,
                'height': thisH
            };
            var modifyInputCss = {
                'width': thisW
            };
            modifyDiv.css(modifyDivCss);
            modifyInput.css(modifyInputCss);

            if($(this).attr('class') == 'hostIp')
            {// 如果双击的是 .hostIp 则向服务器请求该主机的可用ip
                post('/query/ip', 'hostName=' + $(this).parent().attr('id'), renderIp);
            }
            /* get ip & node end */
        });
    }


    // 检测输入的内容是否符合所需内容
    // type： 原始类型
    // value： 需要检测的值
    // return: boolean
    function checkInputType(type, value)
    {
        var reg;
        if(type == 'mac')
        {
            reg = /^[A-Fa-f\d]{2}:[A-Fa-f\d]{2}:[A-Fa-f\d]{2}:[A-Fa-f\d]{2}:[A-Fa-f\d]{2}:[A-Fa-f\d]{2}$/;
        }
        else if(type == 'digital')
        {
            reg = /^\d+$/;
        }
        else if(type == 'dogport')
        {
            reg = /^\d{0,3}[^&]?\d{0,3}$/;
        }
        else if(type == 'dogsn')
        {
            reg = /^[0-9a-zA-Z]{0,20}[^&]?[0-9a-zA-Z]{0,20}$/;
        }
        else if(type == 'ip')
        {
            reg = /^((25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])$/;
        }
        else if(type == 'headIp')
        {
            reg = /^((25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])\.){2}(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])$/;
        }
        else if(type == 'tailIp')
        {
            reg = /^(25[0-5]|2[0-4][0-9]|1?[0-9]?[0-9])$/;
        }
        else if(type == 'date')
        {
            reg = /^[0-1]?[0-9]\/[0-3]?[0-9]\/2[0-1][0-9][0-9]$/;
        }
        else if(type == 'text')
        {
            reg = /^[0-9a-zA-Z]+$/;
        }
        else if(type == 'zhtext')
        {
            reg =  /^([0-9a-zA-Z]|[\u4e00-\u9fa5]|[\(\)（）~!@#\u0024%\u005E&*\u0028\u0029\u007C_\u002B'"=\u007B\u005B\u005C\u003F])+[0-9a-zA-Z]*[\(\)（）~!@#\u0024%\u005E&*\u0028\u0029\u007C_\u002B'"=\u007B\u005B\u005C\u003F]*[\u4e00-\u9fa5]*[0-9a-zA-Z]*[\(\)（）~!@#\u0024%\u005E&*\u0028\u0029\u007C_\u002B'"=\u007B\u005B\u005C\u003F]*[\u4e00-\u9fa5]*[\(\)（）~!@#\u0024%\u005E&*\u0028\u0029\u007C_\u002B'"=\u007B\u005B\u005C\u003F]*$/;
        }
        else if(type == 'notChange')
        {
            return true;
        }
        return reg.test(value);
    }

    // 检测输入的数据和原来的div中的数据是否相同
    // original: 原来的div中的数据
    // value: modifyInput中的数据
    // return: boolean
    function isChanged(original, value)
    {
        return !(original == value);
    }

    // 将修改post到服务器
    // element: 原来的div
    // data: 改变后的值
    function modifyData(element, data)
    {
        var hostName = element.parent().attr('id');
        var hostElement = element.attr('class');

        post('/query/host', 'hostName=' + hostName + '&hostElement=' + hostElement + '&data=' + data, isModify);

        function isModify(receive)
        {
            if(receive == 'false')
            {
                alert('Failed');
            }
        }
    }

    var addDivHtml = "<div id = 'addDiv'>" +
                        "<div id = 'addHeaderDiv'>" +
                            "<div id = 'addHeaderClose'>x</div>" +
                        "</div>" +
                        "<div id = 'addContent'>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Name</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostName' maxlength = '5'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Core</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostCore' maxlength = '4'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Memory(M)</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostMem' maxlength = '5'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Disk(G)</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostDisk' maxlength = '8'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Mac Address</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostMac' maxlength = '17'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Start Time</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostStart'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>End Time</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostEnd'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Company</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostCompany' maxlength = '16'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Remote Port</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostRemotePort' maxlength = '8'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Dog Sn</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostDogN' maxlength = '40'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Dog Port</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostDogP' maxlength = '7'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Bandwidth</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostBandwidth' maxlength = '4'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>Node</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostNode' maxlength = '15'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div class = 'addItemLabel'>IP</div>" +
                                "<div class = 'addItemInputDiv'><input id = 'hostIp' maxlength = '15'></input></div>" +
                            "</div>" +
                            "<div class = 'addItemDiv'>" +
                                "<div id = 'addCommit'>Commit</div>" +
                                "<div id = 'addClear'>Clear</div>" +
                            "</div>" +
                        "</div>" +
                    "</div>";
    var theContainer = $('div#container');
    theContainer.append(addDivHtml);
    var addDiv = $('div#addDiv');
    addDiv.hide();

    // 当点击add按钮时，打开或关闭添加主机对话框
    $('div#add').click(function()
    {
        addDiv.fadeIn('fast');
        $('input#hostName').focus();

        $(function()
            {// 当文本框生成的时候就生成时间选择器
                $("#hostStart").datepicker();
                $("#hostEnd").datepicker();

                $.datepicker.setDefaults(
                {// 设置时间选择器产生的方式，当文本框获得焦点的时候产生
                     showOn: "focus"
                });
            });

        // 当点击add对话框中的commit按钮时，将主机添加到服务器数据库
        $('div#addCommit').click(function()
        {
            var name = $('input#hostName').val();
            var core = $('input#hostCore').val();
            var mem = $('input#hostMem').val();
            var disk = $('input#hostDisk').val();
            var mac = $('input#hostMac').val();
            var start = $('input#hostStart').val();
            var end = $('input#hostEnd').val();
            var company = $('input#hostCompany').val();
            var remotePort = $('input#hostRemotePort').val();
            var dogN = $('input#hostDogN').val();
            var dogP = $('input#hostDogP').val();
            var bandwidth = $('input#hostBandwidth').val();
            var node = $('input#hostNode').val();
            var ip = $('input#hostIp').val();

            if(checkInputType('text', name) && checkInputType('zhtext', company) && checkInputType('dogsn', dogN)
                && checkInputType('digital', core) && checkInputType('digital', mem) && checkInputType('digital', disk)
                && checkInputType('digital', remotePort) && checkInputType('dogport', dogP)
                && checkInputType('digital', bandwidth) && checkInputType('mac', mac)
                && checkInputType('date', start) && checkInputType('date', end)
                && checkInputType('ip', node) && checkInputType('ip', ip))
            {
                post('/query/add', 'hostName=' + name +
                               '&hostCore=' + core +
                               '&hostMem=' + mem +
                               '&hostDisk=' + disk +
                               '&hostMac=' + mac +
                               '&hostStart=' + start +
                               '&hostEnd=' + end +
                               '&hostCompany=' + company +
                               '&hostRemotePort=' + remotePort +
                               '&hostDogN=' + dogN +
                               '&hostDogP=' + dogP +
                               '&hostBandwidth=' + bandwidth +
                               '&hostNode=' + node +
                               '&hostIp=' + ip, hostIsExist);
                
            }
            else
            {
                alert('Type of any elements is not matched');
            }

        });

        // 当点击add对话框中的clear按钮
        $('div#addClear').click(function()
        {
            $('div.addItemInputDiv').children().each(function()
            {
                $(this).val('');
            });
        });
    });

    // 从后台获取的数据中判断虚拟主机是否存在
    function hostIsExist(receive)
    {
        if(receive == 'hostExisted')
        {
            alert('Host has already existed');
        }
        else if(receive == 'ipError')
        {
            alert('Ip has already been used or ip is not existed')
        }
        else if(receive = 'successful')
        {
            queryAll();
        }
    }

    var addIpHtml = "<div class = 'dialog' id = 'addIpDiv'>" +
                        "<div id = 'addIpHeaderDiv'>" +
                            "<div id = 'addIpHeaderClose'>x</div>" +
                        "</div>" +
                        "<div id = 'addIpLabelsDiv'>" +
                            "<div class = 'addIpLabel' id = 'normalAddIpLabel'>Normal</div>" +
                            "<div class = 'addIpLabel' id = 'advancedAddIpLabel'>Advanced</div>" +
                        "</div>" +
                        "<div id = 'normalAddIp'>" +
                            "<div class = 'addIpContent'>" +
                                "<div id = 'addIpLabel'>one row one IP</div>" +
                                "<div id = 'addIpTextDiv'>" +
                                    "<textarea id = 'addIpText'></textarea>" +
                                "</div>" +
                            "</div>" +
                            "<div class = 'ipCommitDiv'>" +
                                "<div class = 'ipCommit'>Commit</div>" +
                                "<div class = 'ipCommitStatus'>Input...</div>" +
                            "</div>" +
                        "</div>" +
                        "<div id = 'advancedAddIp'>" +
                            "<div class = 'addIpContent'>" +
                                "<div id = 'ipHeadLabel'>IP Head</div>" +
                                "<div id = 'ipHeadInputDiv'>" +
                                    "<input id = 'ipHeadInput' maxlength = '11'></input>" +
                                "</div>" +
                                "<div id = 'ipFromLabel'>From</div>" +
                                "<div id = 'ipFromInputDiv'>" +
                                    "<input id = 'ipFromInput' maxlength = '3'></input>" +
                                "</div>" +
                                "<div id = 'ipToLabel'>To</div>" +
                                "<div id = 'ipToInputDiv'>" +
                                    "<input id = 'ipToInput' maxlength = '3'></input>" +
                                "</div>" +
                            "</div>" +
                            "<div class = 'ipCommitDiv'>" +
                                "<div class = 'ipCommit'>Commit</div>" +
                                "<div class = 'ipCommitStatus'>Input...</div>" +
                            "</div>" +
                        "</div>" +
                    "</div>";
    theContainer.append(addIpHtml);
    var addIpDiv = $('div#addIpDiv');
    var addAdvanced = $('div#advancedAddIp');
    var normalAddIpLabel = $('div#normalAddIpLabel');
    var advancedAddIpLabel = $('div#advancedAddIpLabel');
    normalAddIpLabel.css({'background-color': '#ffffff', 'border': '1px solid #ffffff'});
    addIpDiv.hide();
    addAdvanced.hide();

    // 当点击addIP按钮时，显示添加IP对话框
    $("div#addIp").click(function()
    {
        addIpDiv.fadeIn('fast');
        $('textarea#addIpText').focus();
    });

    // 当点击添加IP对话框中的某一个标签时，该标签背景色和边框变为白色
    $("div.addIpLabel").click(function()
    {
        $('div.addIpLabel').css('background-color', '#5cdfff');
        $(this).css({'background-color': '#ffffff', 'border': '1px solid #ffffff'});
    });

    // 当点击普通添加IP标签时，显示该标签的div，并隐藏其他标签的div
    normalAddIpLabel.click(function()
    {
        $("div#advancedAddIp").hide();
        $("div#normalAddIp").slideDown('fast');
        $("textarea#addIpText").focus();
    });

    // 当点击高级添加IP标签时，显示该标签的div，并隐藏其他标签的div
    advancedAddIpLabel.click(function()
    {
        $("div#normalAddIp").hide();
        $("div#advancedAddIp").slideDown('fast');
        $("input#ipHeadInput").focus();
    });

    // 当点击添加IP对话框中的commit按钮时，将当前标签中的IP地址列表post到服务器
    $('div.ipCommit').click(function()
    {
        var ipType = $(this).parent().parent().attr('id');
        var ipStatus = $(this).next();
        if(ipType == 'normalAddIp')
        {// 如果使用的是常规添加IP
            var ips = $('textarea#addIpText').val().split('\n');
            var allIsIp = function()
            {
                for(var i = 0; i <= ips.length - 1; i ++)
                {
                    if(!checkInputType('ip', ips[i]))
                    {
                        return false;
                    }
                }
                return true
            };

            if(allIsIp())
            {
                post('/query/addip', 'ips=' + ips, addIpReceive);
            }
            else
            {
                ipStatus.text('Wrong!');
            }

        }
        else if(ipType == 'advancedAddIp')
        {// 如果使用的是高级添加IP
            var ipHead = $('input#ipHeadInput').val();
            var ipFrom = $('input#ipFromInput').val();
            var ipTo = $('input#ipToInput').val();

            if(checkInputType('headIp', ipHead) && checkInputType('tailIp', ipFrom) && checkInputType('tailIp', ipTo))
            {
                var ipString = "";
                var i = ipFrom;
                while(i <= ipTo - 1)
                {
                    ipString += ipHead + '.' + i + ',';
                    i ++;
                }
                ipString += ipHead + '.' + ipTo;
                post('/query/addip', 'ips=' + ipString, addIpReceive);
            }
            else
            {
                ipStatus.text('wrong');
            }
        }

        function addIpReceive(receive)
        {
            if(receive == 'error')
            {
                ipStatus.text('error');
            }
            else if(receive == 'successful')
            {
                $('textarea#addIpText').val('');
                ipStatus.text('successful');
            }
        }
    });

    var logDiv = $('div#logDiv');
    logDiv.hide();

    // 当鼠标点击log按钮时，打开log显示框
    $('div#logButton').click(function()
    {
        logDiv.fadeIn('fast');
        $('div#logContent').empty();
        post('/query/log', 'query=log', renderLog);
        $('#logQueryConditionFrom').datepicker();
        $('#logQueryConditionTo').datepicker();
    });

    function renderLog(receive)
    {
        var logContent = $('div#logContent');
        logContent.empty();
        $(receive).find('log').each(function()
        {
            logContent.prepend("<div>" + $(this).text() + "</div>");
        });
    }

    var helpDialog = $('div#helpDialog');
    helpDialog.hide();
    $('div#help').click(function()
    {
        $('div#helpDialog').fadeIn('fast');
    });
    // 各个窗体的关闭按钮
    $('div#logHeaderClose').click(function()
    {
        $('div#logDiv').fadeOut('fast');
        $('div.logQueryDialog').hide();
        $('select#logQueryConditionThisHost').empty();
    });
    $('div#addIpHeaderClose').click(function()
    {
        $('div#addIpDiv').fadeOut('fast');
        $('div.ipCommitStatus').text('Input...');
    });
    $('div#addHeaderClose').click(function()
    {
        $('div#addDiv').fadeOut('fast');
    });
    $('div#loginDialogClose').click(function()
    {
        $('div#loginDialog').fadeOut('fast');
    });
    $('div#helpDialogClose').click(function()
    {
        $('div#helpDialog').fadeOut('fast');
    });

    // 点击某个窗体的标题栏，该窗体到最前端
    var logHeader = $('div#logHeaderDiv');
    logHeader.mousedown(function()
    {
        $('div#addIpDiv').css('z-index', '1');
        $('div#addDiv').css('z-index', '1');
        $('div#logDiv').css('z-index', '100');
    });
    var addHeader = $('div#addHeaderDiv');
    addHeader.mousedown(function()
    {
        $('div#addIpDiv').css('z-index', '1');
        $('div#logDiv').css('z-index', '1');
        $('div#addDiv').css('z-index', '100');
    });
    var addIpHeaderDiv = $('div#addIpHeaderDiv');
    addIpHeaderDiv.mousedown(function()
    {
        $('div#addDiv').css('z-index', '1');
        $('div#logDiv').css('z-index', '1');
        $('div#addIpDiv').css('z-index', '100');
    });

    // 将所有主机渲染到logQueryDialog中的host下拉列表里
    function renderLogQueryHost(receive)
    {
        var logHost = $('select#logQueryConditionThisHost');
        logHost.append('<option>all</option>');
        $(receive).find('log').each(function()
        {
            logHost.append('<option>' + $(this).text() + '</option>');

        });
    }

    var logQueryDialog = $('div.logQueryDialog');
    logQueryDialog.hide();
    $('div.logQueryItem').click(function()
    {
        $('div.logQueryDialog').hide();
        var thisDialog = $('div#' + $(this).attr('id') + 'Dialog');

        // 从服务器获取所有的实例名
        post('/query/logcondition', 'condition=hostname', renderLogQueryHost);
        var date = new Date();
        var year = date.getFullYear();
        var month = date.getMonth() + 1;
        var day = date.getDate();
        $('input#logQueryConditionFrom').val(month + '/' + day + '/' + year);
        $('input#logQueryConditionTo').val(month + '/' + day + '/' + year);
        thisDialog.fadeIn('fast');
    });
    $('div.logQueryDialogClose').click(function()
    {
        $('select#logQueryConditionThisHost').empty();
        $(this).parent().parent().fadeOut('fast');
    });

    dialogDrag(logDiv, logHeader);
    dialogDrag(addDiv, addHeader);
    dialogDrag(addIpDiv, addIpHeaderDiv);
    dialogDrag(helpDialog, $('div#helpDialogHeader'));

    dialogDrag(logQueryDialog, $('div.logQueryDialogHeader'), 'parent');

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
                $('.ui-draggable').css({'z-index': '1'});
                $(this).css({'z-index': '100'});
            },
            stop: function()
            {
                $(this).css({'opacity': '1'});
            }
        })
    }

    $('div.logQueryConditionCommit').click(function()
    {// 当点击日志查询条件对话框的commit按钮时
        var conditionFrom = $('#logQueryConditionFrom');
        var conditionTo = $('#logQueryConditionTo');

        if(checkInputType('date', conditionFrom.val()) && checkInputType('date', conditionTo.val()))
        {
            var queryHost = $('select#logQueryConditionThisHost').val();
            var from = $('input#logQueryConditionFrom').val();
            var to = $('input#logQueryConditionTo').val();
            if(queryHost == 'all')
            {
                queryHost = 'empty';
            }
            post('/query/logcondition', 'condition=time&hostname=' + queryHost + '&interval=' + from + '-' + to, renderLog);
        }
        else
        {
            alert('please check the date type.');
        }

    });

    // 如果点击logout按钮时，注销登陆
    $('div#logout').click(function()
    {
        location.href = '/logout/';
    });

});
