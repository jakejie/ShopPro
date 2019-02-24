
// 判断是否登入
        // 图片缓存加载
        $(".lazyImg").scrollLoading();
//   收藏
function frAdd(ids) {
    $.ajax({
        type: 'get',
        url: "/ashx/FavoriteAdd.ashx",
        data: { ids: ids },
        dataType: 'html',
        success: function (data) {
            if (data == "110") {//未登录
                window.location = "/RegUser/login.aspx?url=" + escape(location.href);
            } else if (data == "500") {//参数错误
                alert("参数错误！");
            } else if (data == "101") {//未发现图书
                alert("参数错误！");
            } else {
                var error = 0;
                var array = data.split(",");
                if (array.length > 0) {
                    for (var i = 0; i < array.length; i++) {
                        if (array[i] == "0") {
                            error++;
                        }
                    }
                }
                var msg = "收藏成功";
                if (error > 0) {
                    msg = "部分收藏成功";
                }


                SimplePop.alert("提示", {
                    id: "kindPop",
                    width: "109px",
                    showTitle: false,
                    height: "34px",
                    time: 1,
                    type: "info",
                    opacity: 0,
                    title: "",
                    content: "<div class='dialogContent'><i class='txt_01'><span class='warnIcon'></span>" + msg + "</i></div>"
                })
            }
        },
        error: function () { alert("网路请求错误请联系管理员"); }
    });
}

//点赞
$(document).on("click", ".oparaBut a", function () {
    var $this = $(this);
    var id = $this.parent().attr("data-id");
    var bookid = $this.parent().attr("data-bookid");
    var va = $this.attr("class") == "support" ? "1" : "0";
    $.get("/ashx/imgagecode.aspx", { rid: id, uname: 'bookschina', bid: bookid, va: va }, function (data) {
        if (data == "-9") {
            var url = window.location.href;
            window.location.href = '/RegUser/login.aspx?url=' + url;
        } else if (data != "-1") {
            $this.html('<span class="icon"></span>' + (parseInt($this.text()) + 1))
        } else {
            alert("您已选择了对该评论的观点!");
        }
    })
});

var iCount = $(".ajaxPage").attr("data-count");
if (iCount > 1) {
    $(".ajaxPage").show();
}
//加载书评
function pageClick(page) {
    var totalCount = $('#hidTotalCount').val();
    var bookId = $('#hidBookId').val();
    $.post("/ashx/GetMsg.ashx", { _page: page, _bookid: bookId, _totalPage: totalCount }, function (data) {
        data = eval("(" + data + ")");
        console.log(data);
        if (data.IsSucceed) {
            $('.tabookRecoCon').html(data.Html);
            $('#divPager').html(data.Pager);
            $("html,body").animate({ scrollTop: $('#tabookReco').offset().top - 60 }, 500);
        } else {
            $('.tabookRecoCon').html(data.Error);
            //$(".recoList ul").append(data);
            //$this.attr("data-page", (parseInt(iPage) + 1))
            //if ((parseInt(iPage) + 1) > iCount) {
            //    $this.hide();
            //}
        }
    });
}
$(".ajaxPage").click(function () {
    var $this = $(this);
    var iBookID = $this.attr("data-bookid");
    var iPage = $this.attr("data-page");
    $.post("/ashx/GetMsg.ashx", { _page: iPage, _bookid: iBookID }, function (data) {
        if (data == "") {
            $this.text("没有了")
            $this.unbind();
        } else {
            $(".recoList ul").append(data);
            $this.attr("data-page", (parseInt(iPage) + 1))
            if ((parseInt(iPage) + 1) > iCount) {
                $this.hide();
            }
        }
    });
})
$("#popbigpic").click(function () {
    var bigImgSrc = $("#bigImgSrc").val();
    var winheight = parseInt($(window).height());
    var popHeight;
    function getImageWidth(url, callback) {
        var img = new Image();
        img.src = url;
        if (img.complete) {
            callback(img.width, img.height);
        } else {
            img.onload = function () {
                callback(img.width, img.height);
            }
        }
    }
    getImageWidth(bigImgSrc, function (w, h) {
        if (h >= 500 && Math.round(winheight * 0.7) - 120 > 500) {

            popHeight = 500;

        } else if (h >= 500 && Math.round(winheight * 0.7) - 120 < 500) {


            popHeight = (Math.round(winheight * 0.7) - 120)

        } else {

            popHeight = h;
        }
        SimplePop.alert("", {
            showTitle: false,
            id: "popbig",
            content: '<div class="popBigWrap"><div class="popBigInner" id="magnifier"><img src="' + bigImgSrc + '" class="smallPic"  style="max-width:100%" height="' + popHeight + '"></div><span class="close" id="popbigclose">×</span></div>'
        })

    })
})
$("body").delegate("#magnifier", "mouseenter ", function () {
    if (!$("#magnifier").hasClass("has")) {
        $("#magnifier").zoombie({ on: 'click' });
        $("#magnifier").addClass("has");
    }
})
$("body").delegate("#popbigclose", "click", function () {
    SimplePop.closeSimplePop();
})
// 五星图书
//$(".fiveStartWrap").slide({ mainCell: ".fiveStartCon", effect: "leftLoop", endFun: function () { $("body").trigger('scroll'); } })
$(".fiveStart ul li").hover(function () {
    var $this = $(this);
    $this.addClass("cur").siblings().removeClass("cur");
    $("body").trigger('scroll');
})
// 买过本商品的人还买了
$(".otherBuyWrap").slide({ mainCell: ".conanimate ul", autoPage: true, effect: "left", scroll: 5, vis: 5, endFun: function () { $("body").trigger('scroll'); } })
// 书友推荐
$(".bookLeft .userRec ul li").hover(function () {
    var $this = $(this);
    $this.addClass("cur").siblings().removeClass("cur");
    $("body").trigger('scroll');
})
// 商品详情左侧浮动导航
$(".tabconNav ul").onePageNav({
    scrollThreshold: 0.1,
    space: 60
})
// 中间浮动导航
$(".tabTitPanel ul").onePageNav({
    scrollThreshold: 0.1,
    space: 60
})
//  屏幕滚动的时 商品详情分类切换
$(window).scroll(function () {
    var h = $(window).scrollTop();
    var bookTab = $("#bookTab");
    var backTop1 = $("#bocktop");
    var tabconNav = $("#tabconNav");
    var bookTabVa = $("#bookTab").offset().top;
    var backTop = $(".side_tool .inner .backTop");
    // 浮动导航
    if (h > bookTabVa) {
        bookTab.addClass("fixed");
    } else {
        bookTab.removeClass("fixed");
    }
    // 返回顶部
    if (h > 500) {
        backTop1.slideDown();
    } else {
        backTop1.slideUp();
    }
    // 侧导航活动区域
    if (h > bookTabVa + 55) {
        if ((h - (bookTabVa + 30)) > ($("#tabBookDetail").height() - tabconNav.height())) {
            tabconNav.css("top", ($("#tabBookDetail").height() - tabconNav.height()) + "px");
        } else {
            tabconNav.css("top", h - (bookTabVa + 30) + "px");
        }
    } else {
        tabconNav.css("top", "0px")
    }
})
// 商品详情目录展开 合并
$("#openCatalog").click(function () {
    var $this = $(this);
    if ($this.hasClass("open")) {
        $this.removeClass("open");
        $this.parents("#catalog").find(".con").removeClass("open");
        $this.html('展开全部<i class="icon"></i>');
    } else {
        $this.addClass("open");
        $this.parents("#catalog").find(".con").addClass("open");
        $this.html('点击收起<i class="icon"></i>');
    }
})
// 判断商品详情是否张开
if (parseInt($("#catalogSwitch").height()) <= 240) {
    $(".catalog .switch").remove();
}
$(function () {

    var pageSide = $(".bookLeft");
    var vh = pageSide.height();
    var pageSideOT = pageSide.offset().top;
    var wH = $(window).height();
    var pageMain = $(".bookRight");
    var pageSidebarIn = $(".bookLeftInner");
    var wH = $(window).height();
    $(window).scroll(function () {
        var top = $(document).scrollTop();
        var pageMainOT = pageMain.offset().top;
        var pageMainH = pageMain.height()-90;
        //  侧边栏滚动
        if (top - (pageSideOT + vh - wH) > 0 && vh < pageMainH) {
            pageSidebarIn.addClass("absoluted");
            if (top > (pageMainH + pageMainOT - $(window).height())) {
                pageSidebarIn.css("top", pageMainH - vh + "px")
            } else {
                pageSidebarIn.css("top", (top - (pageSideOT + vh - wH)) + "px")
            }
        } else {
            pageSidebarIn.removeClass("absoluted");
            pageSidebarIn.css("top", 0)
        }
    })
})
