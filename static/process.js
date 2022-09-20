let ws = new WebSocket("ws://0.0.0.0:$PORT/ws");

    ws.onmessage = function(event) {
        let messages = document.getElementById('messages')
        let message = document.createElement('li');
        console.log(event.data, typeof (event.data))
        let receiveJson = JSON.parse(event.data);
        console.log(receiveJson, typeof (receiveJson));
        let content = document.createTextNode(`${receiveJson.number} ${receiveJson.message}`);
        message.appendChild(content);
        messages.appendChild(message)
    };

    function sendMessage(event) {
        let input = document.getElementById("messageText");
        let message = {message: input.value};
        let messageJson = JSON.stringify(message);

        ws.send(messageJson);
        input.value = '';
        event.preventDefault()
    }
