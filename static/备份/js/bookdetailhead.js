

$.ajax({
    url: "/Book_Detail/this.html",
    success: function (data) {
        $("#webCategory").html(data);
    }
});