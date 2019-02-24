isLoging();
function logincommon() {
    $.ajax({
        type: "post",
        url: "/ashx/userlogin.ashx?indexuserlogin=1",
        success: function (data) {
            if (data != "" && data != "0") {
                $(".loginArea").html("<b>欢迎光临中国图书网</b><a  href=\"/vieworder/default.aspx\" target=\"_self\" class=\"userCenter\">" + data + "</a><a href=\"javascript:void(0)\" class=\"userExit\" onclick=\"loginoutcommon();\">[安全退出]</a>");
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            return
        }
    })
}



function loginoutcommon() {
    $.ajax({
        type: "post",
        url: "/ashx/userlogin.ashx?outs=1",
        success: function (data) {
            if (data == "1") {
                if ($("#__VIEWSTATE")) {
                    parent.location.reload();
                }
                if ($(".loginArea")) {
                    $(".loginArea").html("<b>欢迎光临中国图书网，请</b><a href=\"/RegUser/login.aspx\" target=\"_self\" class=\"login\">登录 </a><a href=\"/RegUser/Register.aspx\" class=\"regist\" target=\"_self\">注册</a>");
                }
                window.location = '/RegUser/login.aspx';
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            return
        }
    })
}

function isLoging() {//新版检测是否登录
    $.ajax({
        type: "post",
        url: "/ashx/userlogin.ashx?indexuserlogin=1",
        success: function (data) {
            if (data != "" && data != "0") {
                $(".loginArea").html("<b>欢迎光临中国图书网</b><a  href=\"/vieworder/default.aspx\" target=\"_self\" class=\"userCenter\">" + data + "</a><a href=\"javascript:void(0)\" class=\"userExit\" onclick=\"loginoutcommon();\">[安全退出]</a>");
            }
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            return
        }
    })
}

function GoToPage(obj) {
    var urlTemp = $(obj).attr("data-temp");
    var page = $('#txtPageInputValue').val();
    page = isPositiveInteger(page) ? page : 1;
    window.open(urlTemp.replace("{0}", page), '_self');
}

function isPositiveInteger(s) {//是否为正整数
    var re = /^[0-9]+$/;
    return re.test(s)
}