import WebSocketInstance from "./websocket.js";

class Chat {
    constructor() {
        this.username = null;
        this.roomId = null;
        this.convHistory = null;
    }

    waitForSocketConnection(callback) {
        setTimeout(function () {
            if (WebSocketInstance.state() === 1) {
                console.log("Connection is made");
                callback();
                return;
            } else {
                console.log("Wait for connection...");
                this.waitForSocketConnection(callback);
            }
        }, 100);
    }

    initialise(username, roomId) {
        this.username = username;
        this.roomId = roomId;

        this.waitForSocketConnection(() => {
            WebSocketInstance.fetchMessages(this.username, this.roomId);
            this.scrollToBottom();
        });

        WebSocketInstance.connect(`${this.roomId}`);
    }

    renderMessage(message) {
        //const wrapperDiv = $('<div>').addClass('wrapper');
        const msgDivTag = $('<div>').addClass('msg');
        const spanTimestampTag = $('<span>').addClass('timestamp').text(message.timestamp);
        const pTag = $('<p>').text(message.message);

        if (message.author === this.username) {
            msgDivTag.addClass('messageSent');
        } else {
            const spanUsernameTag = $('<span>')
                .addClass('username')
                .text(`@${message.author.toLowerCase()}`)
                .css({color: message.color_session});
            msgDivTag.addClass('messageReceived');
            msgDivTag.append(spanUsernameTag);
        }

        msgDivTag.append(pTag);
        msgDivTag.append(spanTimestampTag);
        //wrapperDiv.append(msgDivTag);
        //this.convHistory.append(wrapperDiv);
        this.convHistory.append(msgDivTag);
    }


    renderActionUserMessage(message, actionClass) {
        //const wrapperDiv = $('<div>').addClass('wrapper');
        const msgDivTag = $('<div>')
            .addClass('msg')
            .addClass('userAction')
            .addClass(actionClass)
            .text(message.message);

        //wrapperDiv.append(msgDivTag);
        //this.convHistory.append(wrapperDiv);
        this.convHistory.append(msgDivTag);
    }

    renderJoinMessage(message) {
        this.renderActionUserMessage(message, 'join');
    }

    renderLeaveMessage(message) {
        this.renderActionUserMessage(message, 'leave');
    }

    setMessages(messages) {
        for (const [key, message] of Object.entries(messages)) {
            switch (message.type) {
                case 'message':
                    this.renderMessage(message);
                    break;
                case 'join':
                    this.renderJoinMessage(message);
                    break;
                case 'leave':
                    this.renderLeaveMessage(message);
                    break;
            }
        }
        this.scrollToBottom();
    }

    addMessage(message) {
        this.renderMessage(message);
        this.scrollToBottomAnimate();
    }

    joinMessage(message) {
        this.renderJoinMessage(message);
        this.scrollToBottomAnimate()
    }

    leaveMessage(message) {
        this.renderLeaveMessage(message);
        this.scrollToBottomAnimate()
    }

    scrollToBottomAnimate() {
        const convHistory = $(".convHistory");
        convHistory.animate({scrollTop: convHistory.prop("scrollHeight")}, 500);

    }

    scrollToBottom() {
        const convHistory = $(".convHistory");
        convHistory.scrollTop(convHistory.prop("scrollHeight"));
    }

    init() {
        this.convHistory = $(".convHistory");
        const messageInputDom = $('#chat-message-input');

        WebSocketInstance.addCallbacks(
            this.setMessages.bind(this),
            this.addMessage.bind(this),
            this.joinMessage.bind(this),
            this.leaveMessage.bind(this)
        );

        this.initialise(username, room_id);

        $('#chat-message-input').on('keyup', (e) => {
            if (e.keyCode === 13) {  // enter, return
                $('#chat-message-submit').click();
            }
        });

        $('.pick').click(function () {
            console.log(`You choose: ${$(this).text()}`);
            messageInputDom.val(messageInputDom.val() + $(this).text())
        });

        $('#chat-message-submit').on('click', (e) => {
            if (messageInputDom.val() !== '') {
                const messageObject = {
                    'message': messageInputDom.val(),
                    'from': this.username,
                    'chatId': this.roomId
                };
                WebSocketInstance.newChatMessage(messageObject);
                messageInputDom.val('');
            }
            this.scrollToBottomAnimate()
        });

        this.convHistory.on('scroll', () => {
            if (this.convHistory.scrollTop() < this.convHistory.prop("scrollHeight") - this.convHistory.height()) {
                $('#scroll-down-button').fadeIn();
            } else {
                $('#scroll-down-button').fadeOut();
            }
        });

        $('#scroll-down-button').click(() => {
            this.scrollToBottomAnimate();
        });
    }
}

$(document).ready(() => {
    const chat = new Chat();
    chat.init();
});