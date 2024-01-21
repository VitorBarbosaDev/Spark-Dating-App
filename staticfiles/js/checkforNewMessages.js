function fetchNewMessages() {
    const lastMessageId = getLastMessageId();
    const url = `${getNewMessagesUrl}?last_message_id=${lastMessageId}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {
            if (data.messages && data.messages.length > 0) {
                updateChatWindow(data.messages);
            }
        })
        .catch(error => console.error('Error:', error));
}

function getLastMessageId() {
    const lastMessage = document.querySelector('.message-history div:last-child');
    return lastMessage ? lastMessage.dataset.messageId : '';
}

function updateChatWindow(messages) {
    const chatHistory = document.querySelector('.message-history');
    messages.forEach(message => {
        const messageDiv = document.createElement('div');
        messageDiv.className = message.sender === "{{ request.user.username }}" ? 'text-end' : 'text-start';
        messageDiv.dataset.messageId = message.id;

        const messageSpan = document.createElement('span');
        messageSpan.className = `message-bubble ${message.sender === "{{ request.user.username }}" ? 'user-message' : 'other-user-message'}`;
        messageSpan.textContent = message.content;

        messageDiv.appendChild(messageSpan);
        chatHistory.appendChild(messageDiv);
    });
}

setInterval(fetchNewMessages, 5000); // Check for new messages every 5 seconds
