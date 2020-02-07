function DarkenPageWithLoading() {
    var loadTopPos;
    $(".DarkBg").remove();
    $("body").prepend("<div class='DarkBg d-flex align-items-center justify-content-center'><div class='spinner-grow' style='width: 3rem; height: 3rem;' role='status'><span class='sr-only'>Loading...</span></div></div>");

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