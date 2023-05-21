function hide(speed) {
    $(".menuWrap").fadeOut(speed);
    $(".menu").animate({opacity: '0', left: '-320px'}, speed);
}

$(document).ready(function () {
    const SPEED = 180;
    /* make side menu show up */
    $(".trigger").click(function () {
        $(".overlay, .menuWrap").fadeIn(SPEED);
        $(".menu").animate({opacity: '1', left: '0px'}, SPEED);
    });

    /* make config menu show up */
    $(".settings").click(function () {
        $(".config").animate({opacity: '1', right: '0px'}, SPEED);
        /* hide others */
        hide(SPEED);
    });

    // Show/Hide the other notification options
    $(".deskNotif").click(function () {
        $(".showSName, .showPreview, .playSounds").toggle();
    });

    /* close all overlay elements */
    $(".overlay").click(function () {
        $(".overlay, .menuWrap").fadeOut(SPEED);
        $(".menu").animate({opacity: '0', left: '-320px'}, SPEED);
        $(".config").animate({opacity: '0', right: '-200vw'}, SPEED);
    });

    //This also hide everything, but when people press ESC
    $(document).keydown(function (e) {
        if (e.keyCode == 27) {
            $(".overlay, .menuWrap").fadeOut(SPEED);
            $(".menu").animate({opacity: '0', left: '-320px'}, SPEED);
            $(".config").animate({opacity: '0', right: '-200vw'}, SPEED);
            $(".groupCreation").animate({opacity: '0', right: '-200vw'}, SPEED);
        }
    });

    /* make ng (new group) menu show up */
    $(".ng").click(function () {
        $(".groupCreation").animate({opacity: '1', right: '0px'}, SPEED);
        /* hide others */
        hide()
    });

    $("#group_photo").change(function () {
        const file = this.files[0];
        const reader = new FileReader();

        reader.onload = function (e) {
            document.getElementById("preview_image").src = e.target.result;
            document.getElementById("preview_image").style.display = "block";
            document.getElementById("group_photo_lable").style.display = "none";
        };

        reader.readAsDataURL(file);
    });

    $("#preview_image").click(function () {
        document.getElementById("group_photo").click();
    });


    $(".btn-cancel").click(function () {
        $(".groupCreation").animate({opacity: '0', right: '-200vw'}, SPEED);
        $(".overlay, .menuWrap").fadeOut(SPEED);
        $(".menu").animate({opacity: '0', left: '-320px'}, SPEED);
        document.getElementById("preview_image").style.display = "none";
        document.getElementById("group_photo_lable").style.display = "flex";
    });

    /* small conversation menu */
    $(".otherOptions").click(function () {
        $(".moreMenu").slideToggle("fast");
    });

    /* clicking the search button from the conversation focus the search bar outside it, as on desktop */
    $(".search").click(function () {
        $(".searchChats").focus();
    });

    /* Show or Hide Emoji Panel */
    $(".emoji").click(function () {
        $(".emojiBar").fadeToggle(120);
    });

    /* if the user click the conversation or the type panel will also hide the emoji panel */
    $(".convHistory, .replyMessage").click(function () {
        $(".emojiBar").fadeOut(120);
    });
});