import { SOCKET_URL  } from "./settings.js";

class WebSocketService {
    static instance = null;
    callbacks = {};

    static getInstance() {
        if(!WebSocketService.instance) {
            WebSocketService.instance = new WebSocketService();
        }
        return WebSocketService.instance;
    }

    constructor() {
        this.chatSocket = null;
    }

    connect(chatUrl){
        const path = `${SOCKET_URL}/ws/chat/${chatUrl}/`;

        this.chatSocket = new WebSocket(path);
        this.chatSocket.onopen = () => {
            console.log("WebSocket open")
        }
        this.chatSocket.onmessage = e => {
            this.socketNewMessage(e.data);
        }
        this.chatSocket.onerror = e => {
            console.log(e.message);
        }
        this.chatSocket.onclose = () => {
            console.log("WebSocket closed let's reopnen");
            this.connect();
        }
    }

    disconnect() {
        this.chatSocket.close();
    }

    socketNewMessage(data) {
        const parseData = JSON.parse(data);
        const command = parseData.command;

        if (Object.keys(this.callbacks).length === 0) {
            return;
        }
        if (command === "messages") {
            this.callbacks[command](parseData.messages.reverse());
        }
        if (command === "new_message") {
            this.callbacks[command](parseData.message);
        }
        if (command === "join_message") {
            this.callbacks[command](parseData.message);
        }
    }

    fetchMessages(username, chatId) {
        this.sendMessage({
            command: 'fetch_messages',
            username: username,
            chatId: chatId
        });
    }

    newChatMessage(message) {
        this.sendMessage({
            command: 'new_message',
            from: message.from,
            message: message.message,
            chatId: message.chatId
        });
    }

    sendMessage(data){
        try {
            this.chatSocket.send(JSON.stringify({...data}));
        } catch (error) {
            console.log(error.message);
        }
    }

    addCallbacks(
        messagesCallback,
        newMessageCallback,
        newJoinMessageCallback
    ) {
        this.callbacks["messages"] = messagesCallback;
        this.callbacks["new_message"] = newMessageCallback;
        this.callbacks["join_message"] = newJoinMessageCallback;
    }

    state() {
        return this.chatSocket.readyState;
    }
}

const WebSocketInstance = WebSocketService.getInstance();
export default WebSocketInstance;