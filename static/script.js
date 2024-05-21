function sendMessage() {
    var userInput = document.getElementById("user-input").value;
    document.getElementById("chat-box").innerHTML += "<p><strong>You:</strong> " + userInput + "</p>";
    document.getElementById("user-input").value = "";

    // Get previous system responses
    var previousResponses = getPreviousResponses();

    // Send user message and previous responses to server
    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput, systemResponses: previousResponses })
    })
        .then(response => response.json())
        .then(data => {
            var botResponse = data.response;
            document.getElementById("chat-box").innerHTML += "<p><strong>ChatGPT:</strong> " + botResponse + "</p>";
            scrollToBottom();
        });
}

function getPreviousResponses() {
    var previousResponses = [];
    var chatBoxContent = document.getElementById("chat-box").innerHTML;
    var chatMessages = chatBoxContent.split("<p><strong>");
    for (var i = 1; i < chatMessages.length; i++) {
        var role = chatMessages[i].split("</strong>")[0];
        var content = chatMessages[i].split("</strong> ")[1].split("</p>")[0];
        previousResponses.push({ role: role, content: content });
    }
    return previousResponses;
}

function quickChat() {
    fetch('/quick-chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(data => {
            var botResponse = data.response;
            document.getElementById("chat-box").innerHTML += "<p><strong>ChatGPT:</strong> " + botResponse + "</p>";
            scrollToBottom();
        });
}

function scrollToBottom() {
    var chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}

