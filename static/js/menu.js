window.onload = function () {
    var subnav = document.getElementsByClassName('subnav')[0];
    var li = subnav.getElementsByTagName('li');
    var menu = subnav.getElementsByClassName('menu')[0];
    var detail = menu.getElementsByClassName('cate_detail');
    var l;
    for (var i = 0; i < li.length; i++) {
        li[i].setAttribute('num', i);
        li[i].onmouseover = function () {
            for (var j = 0; j < li.length; j++) {
                detail[j].style.display = 'none'
            }
            ;l = this.getAttribute('num');
            detail[l].style.display = 'block'
        }
    }
    ;subnav.onmouseover = function () {
        menu.style.display = 'block'
    };
    subnav.onmouseout = function () {
        menu.style.display = 'none'
    }
};