// import WebSocketInstance from "./websocket.js";
//
// function waitForSocketConnection(callback) {
//     setTimeout(function () {
//         if (WebSocketInstance.state() === 1) {
//             console.log("Connection is made");
//             callback();
//             return;
//         } else {
//             console.log("wait for connection...");
//             waitForSocketConnection(callback);
//         }
//     }, 100);
// }
//
// function initialiseChat(username, roomName, chatRoomId) {
//     waitForSocketConnection(() => {
//         WebSocketInstance.fetchMessages(
//             username,
//             chatRoomId
//         );
//         scrollToBottom();
//     });
//     WebSocketInstance.connect(`${roomName}`);
// }
//
// function renderMessage(message) {
//     var msgDivTag = document.createElement('div');
//     msgDivTag.className = 'msg';
//     var spanTimestampTag = document.createElement('span');
//
//     var pTag = document.createElement('p');
//
//     // Timestamp
//     spanTimestampTag.className = 'timestamp';
//     spanTimestampTag.textContent = message.timestamp;
//
//
//     // Text message
//     pTag.textContent = message.message;
//
//     // Сhecking who is the author of the message
//     if (message.author === username) {
//         $(msgDivTag).addClass('messageSent');
//     } else {
//         // Username
//         var spanUsernameTag = document.createElement('span');
//         spanUsernameTag.className = 'username';
//         spanUsernameTag.textContent = `@${message.author.toLowerCase()}`;
//         $(msgDivTag).addClass('messageReceived');
//         msgDivTag.appendChild(spanUsernameTag);
//     }
//
//
//     msgDivTag.appendChild(pTag);
//     msgDivTag.appendChild(spanTimestampTag);
//     document.querySelector('#chat-log').appendChild(msgDivTag);
// }
//
// function setMessages(messages) {
//     for (const [key, message] of Object.entries(messages)) {
//         renderMessage(message);
//     }
//     scrollToBottom();
// };
//
// function addMessage(message) {
//     renderMessage(message);
//     scrollToBottomAnimate();
// }
//
// function scrollToBottomAnimate() {
//     var convHistory = $(".convHistory");
//     convHistory.animate({
//         scrollTop: convHistory.prop("scrollHeight")
//     }, 500);
// }
//
// function scrollToBottom() {
//     var convHistory = $(".convHistory");
//     convHistory.scrollTop(convHistory.prop("scrollHeight"));
// }
//
// $(document).ready(function () {
//
//
//     WebSocketInstance.addCallbacks(
//         setMessages.bind(this),
//         addMessage.bind(this)
//     );
//
//     initialiseChat(username, roomName, room_id);
//
//
//     $('#chat-message-input').on('keyup', function (e) {
//         if (e.keyCode === 13) {  // enter, return
//             $('#chat-message-submit').click();
//         }
//     });
//
//     $('#chat-message-submit').on('click', function (e) {
//         const messageInputDom = $('#chat-message-input');
//         if (messageInputDom.val() != '') {
//             const messageObject = {
//                 'message': messageInputDom.val(),
//                 'from': username,
//                 'chatId': room_id
//             }
//             WebSocketInstance.newChatMessage(messageObject);
//             messageInputDom.val('');
//         }
//
//     });
// });
//

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

function initialiseChat(username, roomName, chatRoomId) {
    waitForSocketConnection(() => {
        WebSocketInstance.fetchMessages(username, chatRoomId);
        scrollToBottom();
    });
    WebSocketInstance.connect(`${roomName}`);
}

function renderMessage(message) {
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
    $('#chat-log').append(msgDivTag);
}

function setMessages(messages) {
    for (const [key, message] of Object.entries(messages)) {
        renderMessage(message);
    }
    scrollToBottom();
}

function addMessage(message) {
    renderMessage(message);
    scrollToBottomAnimate();
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

    WebSocketInstance.addCallbacks(setMessages.bind(this), addMessage.bind(this));
    initialiseChat(username, roomName, room_id);

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

