import WebSocketInstance from "./websocket.js";

function waitForSocketConnection(callback) {
    setTimeout(function () {
        if (WebSocketInstance.state() === 1) {
            console.log("Connection is made");
            callback();
            return;
        } else {
            console.log("Wait for connection...");
            waitForSocketConnection(callback);
        }
    }, 100);
}

function initialiseChat(username, chatRoomId) {
    waitForSocketConnection(() => {
        WebSocketInstance.fetchMessages(
            username,
            chatRoomId
        );
        scrollToBottom();
    });
    WebSocketInstance.connect(`${chatRoomId}`);
}

function renderMessage(message) {
    var wrapperDiv = $('<div>').addClass('wrapper');
    var msgDivTag = $('<div>').addClass('msg');
    var spanTimestampTag = $('<span>').addClass('timestamp').text(message.timestamp);
    var pTag = $('<p>').text(message.message);

    if (message.author === username) {
        $(msgDivTag).addClass('messageSent');
    } else {
        var spanUsernameTag = $('<span>').addClass('username').text(`@${message.author.toLowerCase()}`);
        $(msgDivTag).addClass('messageReceived');
        msgDivTag.append(spanUsernameTag);
    }

    msgDivTag.append(pTag);
    msgDivTag.append(spanTimestampTag);
    wrapperDiv.append(msgDivTag)
    $('#chat-log').append(wrapperDiv);
}


function renderActionUserMessage(message, actionClass) {
    var wrapperDiv = $('<div>')
        .addClass('wrapper');

    var msgDivTag = $('<div>')
        .addClass('msg')
        .addClass('userAction')
        .addClass(actionClass)
        .text(message.message);

    wrapperDiv.append(msgDivTag);

    $('#chat-log').append(wrapperDiv);
}

function renderJoinMessage(message) {
    renderActionUserMessage(message, 'join');
}

function renderLeaveMessage(message) {
    renderActionUserMessage(message, 'leave');
}


function setMessages(messages) {
    for (const [key, message] of Object.entries(messages)) {
        switch (message.type) {
            case 'message':
                renderMessage(message);
                break;
            case 'join':
                renderJoinMessage(message);
                break;
            case 'leave':
                renderLeaveMessage(message);
                break;
        }
    }
    scrollToBottom();
}

function addMessage(message) {
    renderMessage(message);
    scrollToBottomAnimate();
}

function joinMessage(message) {
    renderJoinMessage(message);
}

function leaveMessage(message){
    renderLeaveMessage(message)
}

function scrollToBottomAnimate() {
    var convHistory = $(".convHistory");
    convHistory.animate({scrollTop: convHistory.prop("scrollHeight")}, 500);
}

function scrollToBottom() {
    var convHistory = $(".convHistory");
    convHistory.scrollTop(convHistory.prop("scrollHeight"));
}

$(document).ready(function () {
    var convHistory = $(".convHistory");

    WebSocketInstance.addCallbacks(
        setMessages.bind(this),
        addMessage.bind(this),
        joinMessage.bind(this),
        leaveMessage.bind(this)
    );

    initialiseChat(username, room_id);

    $('#chat-message-input').on('keyup', function (e) {
        if (e.keyCode === 13) {  // enter, return
            $('#chat-message-submit').click();
        }
    });

    $('#chat-message-submit').on('click', function (e) {
        const messageInputDom = $('#chat-message-input');
        if (messageInputDom.val() != '') {
            const messageObject = {
                'message': messageInputDom.val(),
                'from': username,
                'chatId': room_id
            };
            WebSocketInstance.newChatMessage(messageObject);
            messageInputDom.val('');
        }
    });

    convHistory.scroll(function () {
        if (convHistory.scrollTop() < convHistory.prop("scrollHeight") - convHistory.height()) {
            $('#scroll-down-button').fadeIn();
        } else {
            $('#scroll-down-button').fadeOut();
        }
    });

    $('#scroll-down-button').click(function () {
        convHistory.animate({scrollTop: convHistory.prop("scrollHeight")}, 500);
    });
});

