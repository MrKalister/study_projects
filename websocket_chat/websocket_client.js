document.addEventListener('DOMContentLoaded', function(){

    const messagesContainer = document.querySelector("#messages_container");
    const messageInput = document.querySelector("[name=message_input]");
    const sendMessageButton = document.querySelector("[name=send_message_button]");

    let websocketClient = new WebSocket("ws://localhost:12345")

    websocketClient.onopen = () => {
        console.log('client connected');

        sendMessageButton.onclick = () => {
            websocketClient.send(messageInput.value);
            messageInput.value = "";
        };
    };

    websocketClient.onmessage = (message) => {
        const newMessage = document.createElement('div');
        newMessage.innerHTML = message.data;
        messagesContainer.appendChild(newMessage);
    };

}, false);