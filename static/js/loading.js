function DarkenPageWithLoading() {
    var loadTopPos;
    $(".DarkBg").remove();
    $("body").prepend("<div class='DarkBg'><img src='/static/images/loading.gif' id='loadImg'/></div>");

        $(".DarkBg").css({
            "height": $(document).height() + "px",
        });

        $(window).on("load resize", function () {
            $(".DarkBg").css({
                "width": document.body.scrollWidth + "px"
            });
        });


}

function LightenPage() {
    $(document).ready(function () {
        $(".DarkBg").remove();
    });
}