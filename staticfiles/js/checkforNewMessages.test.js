// Import the functions you want to test
const { fetchNewMessages, getLastMessageId, fetchWithRetry, updateChatWindow } = require('./checkforNewMessages');

// Mock the fetch API
global.fetch = jest.fn(() =>
    Promise.resolve({
        json: () => Promise.resolve({ chat_messages: ['message1', 'message2'] }),
    })
);

// Mock the other functions
jest.mock('./checkforNewMessages', () => ({
    getLastMessageId: jest.fn(),
    fetchWithRetry: jest.fn(),
    updateChatWindow: jest.fn(),
}));

describe('fetchNewMessages', () => {
    it('fetches new messages correctly', async () => {
        // Arrange
        getLastMessageId.mockReturnValueOnce(1);
        fetchWithRetry.mockReturnValueOnce(Promise.resolve({
            json: () => Promise.resolve({ chat_messages: ['message1', 'message2'] }),
        }));

        // Act
        await fetchNewMessages();

        // Assert
        expect(getLastMessageId).toHaveBeenCalled();
        expect(fetchWithRetry).toHaveBeenCalled();
        expect(updateChatWindow).toHaveBeenCalledWith(['message1', 'message2']);
    });
});