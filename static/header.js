$(document).ready(function()
{
    var managerDiv = "<div id = 'managerDiv'>" +
                         "<div id = 'managerHeader'><div id = 'managerClose'>x</div></div>" +
                         "<div id = 'managerContent'>" +
                             "<div id = 'allUsers'>" +
                                 "<div id = 'allUsersHead'></div>" +
                             "</div>" +
                             "<div id = 'newUsers'>" +
                                 "<div id = 'newUsers'></div>" +
                             "</div>" +
                         "</div>" +
                     "</div>";
    $('div#toolbarDiv').append(managerDiv);
    $('div#managerDiv').hide();

    // 当点击管理按钮时，弹出管理窗体
    $('div#manager').click(function()
    {
        $('div#managerDiv').fadeIn('fast');
    });
});