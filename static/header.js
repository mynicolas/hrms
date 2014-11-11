$(document).ready(function()
{
    var managerDivHtml = "<div id = 'managerDiv'>" +
                         "<div id = 'managerHeader'><div id = 'managerClose'>x</div></div>" +
                         "<div id = 'managerContentDiv'>" +
                             "<div class = 'usersTable' id = 'allUsers'>" +
                                 "<div class = 'usersTableHead' id = 'allUsersHead'>all users</div>" +
                             "</div>" +
                             "<div class = 'usersTable' id = 'newUsers'>" +
                                 "<div class = 'usersTableHead' id = 'newUsersHead'>new users</div>" +
                             "</div>" +
                             "<div id = 'usersContentContainer'>" +
                                 "<div class = 'usersContentDiv' id = 'allUsersContentDiv'></div>" +
                                 "<div class = 'usersContentDiv' id = 'newUsersContentDiv'></div>" +
                             "</div>" +
                         "</div>" +
                     "</div>";
    $('div#toolbarDiv').append(managerDivHtml);
    var managerDiv = $('div#managerDiv');
    var managerHeader = $('div#managerHeader');
    var managerClose = $('div#managerClose');
    var allUsersContentDiv = $('div#allUsersContentDiv');
    var newUsersContentDiv = $('div#newUsersContentDiv');
    managerDiv.hide();

    // 当manager窗体的all users标签被点击时，该标签北京变为白色，另一个标签则成为绿色,并且从服务器获取所有用户的信息（不包括没有登陆权限的用户）
    $('div#allUsersHead').click(function()
    {
        $('div.usersTableHeadClick').removeClass().addClass('usersTableHead');
        $(this).removeClass().addClass('usersTableHeadClick');

    });

    // 当manager窗体的new users标签被点击时，该标签变为白色，另一个变成绿色，并且从服务器获取没有登陆权限但是已经注册的用户（is_active = false）
    $('div#newUsersHead').click(function()
    {
        $('div.usersTableHeadClick').removeClass().addClass('usersTableHead');
        $(this).removeClass().addClass('usersTableHeadClick');

    });
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
        managerClose.click(function()
        {
            managerDiv.fadeOut('fast');
        });
    });
});