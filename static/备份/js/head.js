

// 判断是否登入
javascript: isLoging();
// 关键字搜索
var keyword = getParam("stp");
var cate = getParam("sCate");
if (keyword != undefined && keyword.length > 0)
    $("#keyword").val(unescape(keyword));
if (cate != undefined && cate.length > 0) {
    $('#search_cates').find('.on').removeClass('on');
    $('#cate_' + cate).addClass('on');
    $(".dropSearch dt").html('<span>' + $('#cate_' + cate).html() + '<b class="icon"></b></span>');
    $(".dropSearch dd").hide();
}

/*点击搜索按钮*/
$(".searchBut").click(function () {
    var Keyword = $.trim($("#keyword").val());
    var sCategory = $("#search_cates .on").attr('id').replace("cate_", "");
    if (Keyword == "") {
        Keyword = $.trim($("#keyword").attr('placeholder'));
    }
    window.open("/book_find2/?stp=" + escape(Keyword) + "&sCate=" + sCategory);
    $("#bigAutocompleteContent").hide();
})

/*按回车键 搜索*/
$("#keyword").keypress(function (event) {
    var e = event ? event : (window.event ? window.event : null);
    var key = e.which;
    if (key == 13) {
        var Keyword = $.trim($("#keyword").val())
        var sCategory = $("#search_cates .on").attr('id').replace("cate_", "");
        if (Keyword != "") {
            window.open("/book_find2/?stp=" + escape(Keyword) + "&sCate=" + sCategory);
            $("#bigAutocompleteContent").hide();
        }
    }
})
// 分类搜索
$(".dropSearch dl dt").hover(function () {
    $(".dropSearch dd").show();
})
$(".dropSearch").mouseleave(function () {
    $(".dropSearch dd").hide();
})
$(".dropSearch dd ul li").click(function () {
    var $this = $(this);
    $this.addClass("on").siblings().removeClass("on");
    $(".dropSearch dt").html('<span>' + $this.html() + '<b class="icon"></b></span>');
    $(".dropSearch dd").hide();
})
/*下拉框*/
$("#keyword").bigAutocomplete({
    width: 428, url: "/book_find2/ajax/", callback: function (data) {
        window.open("/book_find2/?stp=" + escape(data.label) + "");
    }
})


//  图书轮播
if ($(".headBookFocusPanel ul li").length > 1) {
    $(".headBookFocus").slide({ mainCell: ".headBookFocusPanel ul", effect: "leftLoop", interTime: 5000, pageStateCel: ".pageState", autoPlay: true })
}
// 图片
if ($(".headPicFocusPanel ul li").length > 1) {
    $(".headPicFocus").slide({ mainCell: ".headPicFocusPanel ul", titCell: ".buttonWrap span", interTime: 5000, autoPlay: true })
}
// 公告
if ($(".noticePanel ul li").length > 1) {
    $(".notice").slide({ mainCell: ".noticePanel ul", interTime: 3000, effect: "topLoop", autoPlay: true })
}

//图书网搜索补全下拉
$("#keyword").bigAutocomplete({
    url: "/book_find2/ajax/", callback: function (data) {
        window.open("/book_find2/?stp=" + escape(data.label) + "");
    }
});
$(".searchArea .searchFrom .dropSearch").hover(function () {
    var $this = $(this);
    $this.find("dd").show();
}, function () {
    var $this = $(this);
    $this.find("dd").hide();
});

bookNav("#webCategory");
function bookNav(a) {
    $(a).delegate(".js_toggle", "mouseenter", function () {
        var t = $(this),
        e = t.find(".menu-item"),
        o = (t.index(), e.find(".menu-item"), $(a).offset().top),
        i = t.offset().top - o,
        n = (e.outerHeight() - t.outerHeight()) / 2,
        s = $(a).height() - (t.offset().top - o + t.outerHeight());
        e.outerHeight() / 2 > s ? e.css("bottom", -s) : e.css("top", n > i ? -i - 2 : -n - 2),
        e.show(),
        t.addClass("hover")
    }).delegate(".js_toggle", "mouseleave",
function () {
    $(this).removeClass("hover").find(".menu-item").hide();
})
}
if ($(".category-content .category").is(":hidden")) {
    $("#nav .category-content .all-goods").hover(function () {
        $(".category-content .category").show();
    }, function () {
        $(".category-content .category").hide();
    })
}

$(".specil_category li").each(function (index, obj) {
    if (window.location.pathname == '/')
        return;

    $(obj).removeClass('cur');
    if ($(obj).find('a').attr('href').toLocaleLowerCase().indexOf(window.location.pathname.toLocaleLowerCase()) != -1)
        $(obj).addClass('cur');
});