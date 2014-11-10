$(document).ready(function()
{
    var managerDivHtml = "<div id = 'managerDiv'>" +
                         "<div id = 'managerHeader'><div id = 'managerClose'>x</div></div>" +
                         "<div id = 'managerContentDiv'>" +
                             "<div id = 'allUsers'>" +
                                 "<div id = 'allUsersHead'></div>" +
                             "</div>" +
                             "<div id = 'newUsers'>" +
                                 "<div id = 'newUsers'></div>" +
                             "</div>" +
                         "</div>" +
                     "</div>";
    $('div#toolbarDiv').append(managerDivHtml);
    var managerDiv = $('div#managerDiv');
    var managerHeader = $('div#managerHeader');
    var managerClose = $('div#managerClose');
    managerDiv.hide();

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
        });
    }

    // 当点击管理按钮时，弹出管理窗体
    $('div#manager').click(function()
    {
        managerDiv.fadeIn('fast');
        dialogDrag(managerDiv, managerHeader);
    });
});