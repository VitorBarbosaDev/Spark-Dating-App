from django.test import TestCase
from messaging.models import Message
from profiles.models import UserProfile

class MessageModelTestCase(TestCase):
    def setUp(self):
        self.user1 = UserProfile.objects.create_user('user1', 'user1@example.com', 'password123')
        self.user2 = UserProfile.objects.create_user('user2', 'user2@example.com', 'password123')

    def test_message_creation(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        self.assertIsInstance(message, Message)
        self.assertEqual(message.content, "Hello")

    def test_message_str(self):
        message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        self.assertEqual(str(message), "Message from user1 to user2")

    def test_message_ordering(self):
        message1 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello")
        message2 = Message.objects.create(sender=self.user1, receiver=self.user2, content="Hello again")
        messages = Message.objects.all()
        self.assertEqual(messages[0], message1)
        self.assertEqual(messages[1], message2)