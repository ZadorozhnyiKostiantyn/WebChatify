function hideMenu(speed) {
    $(".menuWrap").fadeOut(speed);
    $(".menu").animate({opacity: '0', left: '-320px'}, speed);
}

function closeAllOverlay(speed) {
    $(".overlay, .menuWrap").fadeOut(speed);
    $(".menu").animate({opacity: '0', left: '-320px'}, speed);
    $(".config").animate({opacity: '0', right: '-200vw'}, speed);
    $(".groupCreation").animate({opacity: '0', right: '-200vw'}, speed);
    $('.inviteLink').fadeOut(speed)
}

function cssMoreMenu() {
    $(".moreMenu").css({
        top: 50 + "px",
        left: '',
        right: 20 + "px"
    });
}

function hideMoreMenu() {
    cssMoreMenu()
    $(".moreMenu").hide();
}


function copyToClipboard(text) {
    var textarea = $('<textarea></textarea>');
    textarea.val(text);
    $('body').append(textarea);
    textarea.select();
    document.execCommand('copy');
    textarea.remove();
}

function toggleMoreMenu() {
    if ($(".moreMenu").is(":hidden")) {
        $(".moreMenu").slideToggle("fast");
    } else {
        hideMoreMenu()
    }
}

function closeMoreMenu(e) {
    if (!$(e.target).closest(".chatButton").length &&
        !$(e.target).closest(".otherOptions").length &&
        !$(e.target).closest(".option").length) {
        hideMoreMenu()
    }
}

$(document).ready(function () {
    const SPEED = 180;
    const HOST_URL = "http://127.0.0.1:8000";
    var chatId = 0;
    /* make side menu show up */
    $(".trigger").click(function () {
        $(".overlay, .menuWrap").fadeIn(180);
        $(".menu").animate({opacity: '1', left: '0px'}, SPEED);
    });

    /* make config menu show up */
    $(".settings").click(function () {
        $(".config").animate({opacity: '1', right: '0px'}, SPEED);
        /* hide others */
        hideMenu(SPEED);
    });

    // Show/Hide the other notification options
    $(".deskNotif").click(function () {
        $(".showSName, .showPreview, .playSounds").toggle();
    });

    /* close all overlay elements */
    $(".overlay").click(function () {
        closeAllOverlay(SPEED);
    });

    //This also hide everything, but when people press ESC
    $(document).keydown(function (e) {
        if (e.keyCode == 27) {
            closeAllOverlay(SPEED);
        }
    });

    //Enable/Disable night mode
    $(".DarkThemeTrigger").click(function () {
        $("body").toggleClass("DarkTheme")
    });

    /* small conversation menu */
    $(".otherOptions").click(function () {
        chatId = room_id;
        toggleMoreMenu()
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

    /* make ng (new group) menu show up */
    $(".ng").click(function () {
        $(".groupCreation").animate({opacity: '1', right: '0px'}, SPEED);
        /* hide others */
        hideMenu(SPEED);
    });

    /* */
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

    /* set new  image*/
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


    $('.chatButton').click(function () {
        var selectedChat = $(this);

        selectedChat.addClass('active');
        selectedChat.siblings().removeClass('active');

        var roomName = $(this).data('name');
        var roomId = $(this).data('id');
        window.location.pathname = `/chat/${roomId}/`;
    });


    $(".chatButton").on("contextmenu", function (e) {
        e.preventDefault(); // Відміна стандартного контекстного меню
        var chatButton = $(this);
        var offsetX = e.pageX - chatButton.offset().left;
        var offsetY = e.pageY - 40;
        chatId = $(this).data('id');

        $(".moreMenu").css({
            top: offsetY + "px",
            left: offsetX + "px",
        });
        toggleMoreMenu()
    });

    $(".option").click(function () {
        if ($(this).hasClass("invite")) {
            $.ajax({
                url: '/chat/get_invite_link/',
                method: 'GET',
                data: {
                    chatId: chatId
                },
                success: function (response) {
                    var inviteLink = response.link;
                    $('#inviteLinkInput').val(`${HOST_URL}/chat/invite/${inviteLink}`);
                    $(".overlay, .menuWrap").fadeIn(SPEED);
                    $('.inviteLink').fadeIn(SPEED); // Показуємо вікно з посиланням
                },
                error: function () {
                    alert('Failed to get invite link. Please try again.');
                }
            });
        } else if ($(this).hasClass("leaveGroup")) {
            window.location.pathname = `/chat/leave_chat_room/${chatId}`;
        }
    });


    $('.copyLink').click(function () {
        var inviteLink = $('#inviteLinkInput').val();
        copyToClipboard(inviteLink);
        closeAllOverlay()
    });


    $(document).on({
        "mousedown": function (e) {
            closeMoreMenu(e)
        },
        "click": function (e) {
            closeMoreMenu(e)
        }
    });
});
