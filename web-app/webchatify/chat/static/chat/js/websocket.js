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
        //const path = `ws://${window.location.host}/ws/chat/${chatUrl}/`;
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

    addCallbacks(messagesCallback, newMessageCallback) {
        this.callbacks["messages"] = messagesCallback;
        this.callbacks["new_message"] = newMessageCallback;
    }

    state() {
        return this.chatSocket.readyState;
    }
}

const WebSocketInstance = WebSocketService.getInstance();
export default WebSocketInstance;