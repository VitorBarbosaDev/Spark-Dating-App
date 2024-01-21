function fetchNewMessages() {
    console.log("Fetching new messages"); // Add this line for debugging
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
        messageDiv.className = message.sender === currentUserUsername ? 'text-end' : 'text-start';
        messageDiv.dataset.messageId = message.id;

        const messageSpan = document.createElement('span');
        messageSpan.className = `message-bubble ${message.sender === currentUserUsername ? 'user-message' : 'other-user-message'}`;
        messageSpan.textContent = message.content;

        messageDiv.appendChild(messageSpan);
        chatHistory.appendChild(messageDiv);
    });
}


document.addEventListener('DOMContentLoaded', function() {
    setInterval(fetchNewMessages, 5000); // Check for new messages every 5 seconds
});

