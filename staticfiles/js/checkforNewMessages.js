function fetchNewMessages() {

    const lastMessageId = getLastMessageId();
    const url = `${getNewMessagesUrl}?last_message_id=${lastMessageId}`;


    fetchWithRetry(url, 3) // Retry up to 3 times
        .then(response => response.json())
        .then(data => {

            if (data.chat_messages && data.chat_messages.length > 0) {
                updateChatWindow(data.chat_messages);
            } else {

            }
        })
        .catch(error => {

        });
}


function fetchWithRetry(url, retries, delay = 1000) {
    return new Promise((resolve, reject) => {
        const attemptFetch = (retries) => {
            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return resolve(response);
                })
                .catch(error => {
                    if (retries === 0) {
                        reject(error);
                    } else {

                        setTimeout(() => attemptFetch(--retries), delay);
                    }
                });
        };
        attemptFetch(retries);
    });
}

function getLastMessageId() {
    const lastMessage = document.querySelector('.message-history div:last-child');
    return lastMessage ? parseInt(lastMessage.dataset.messageId, 10) : 0;
}



function updateChatWindow(messages) {
    const chatHistory = document.querySelector('.message-history');
    const lastMessageId = getLastMessageId(); // Get the last message ID from the chat window


    messages.forEach(message => {


        // Convert the message IDs to integers for comparison (if they are strings)
        const messageIdInt = parseInt(message.id);

        const lastMessageIdInt = parseInt(lastMessageId);


        // Check if the message ID is greater than the last message ID in the chat
        if (messageIdInt > lastMessageIdInt) {


            const messageDiv = document.createElement('div');
            messageDiv.className = message.sender === currentUserUsername ? 'text-end' : 'text-start';
            messageDiv.dataset.messageId = message.id;
            messageDiv.classList.add('mb-2');

            const messageSpan = document.createElement('span');
            messageSpan.className = `message-bubble ${message.sender === currentUserUsername ? 'user-message' : 'other-user-message'}`;
            messageSpan.textContent = message.content;

            messageDiv.appendChild(messageSpan);
            chatHistory.appendChild(messageDiv);
        } else {

        }
        // Scroll to the bottom of the chat window
        chatHistory.scrollTop = chatHistory.scrollHeight;
    });
}


document.addEventListener('DOMContentLoaded', function() {
    const chatHistory = document.querySelector('.message-history');
    chatHistory.scrollTop = chatHistory.scrollHeight;

    setInterval(fetchNewMessages, 5000); // Check for new messages every 5 seconds
});


module.exports = {
    fetchNewMessages,
    fetchWithRetry,
    getLastMessageId,
    updateChatWindow
};