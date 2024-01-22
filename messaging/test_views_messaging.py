from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from profiles.models import UserProfile, Match
from messaging.models import Message

class MessagingViewTestCase(TestCase):
    def setUp(self):
        # Create test users
        self.user1 = UserProfile.objects.create_user('user1', 'user1@example.com', 'password123')
        self.user2 = UserProfile.objects.create_user('user2', 'user2@example.com', 'password123')

        # Create a match between user1 and user2
        self.match = Match.objects.create(user1=self.user1, user2=self.user2)

        # Create messages between users
        Message.objects.create(sender=self.user1, receiver=self.user2, content="Hi User2!")
        Message.objects.create(sender=self.user2, receiver=self.user1, content="Hello User1!")

        # Login as user1 for tests
        self.client.login(username='user1', password='password123')
    def test_match_list(self):
        response = self.client.get(reverse('messaging:match_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging/match_list.html')
        self.assertIn(self.user2, response.context['matched_profiles'])


    def test_chat_view_get(self):
        response = self.client.get(reverse('messaging:chat', args=[self.user2.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'messaging/chat.html')
        self.assertEqual(response.context['other_user'], self.user2)
        self.assertEqual(len(response.context['chat_messages']), 2)

    def test_chat_view_post(self):
        response = self.client.post(reverse('messaging:chat', args=[self.user2.username]), {'content': 'New message'})
        self.assertEqual(response.status_code, 302)  # Redirect after POST
        self.assertEqual(Message.objects.count(), 3)  # New message created


    def test_get_new_messages(self):
        # Create a new message to test fetching new messages
        new_message = Message.objects.create(sender=self.user1, receiver=self.user2, content="Another message")

        response = self.client.get(reverse('messaging:get_new_messages', args=[self.user2.username]), {'last_message_id': new_message.id - 1})
        self.assertEqual(response.status_code, 200)
        response_data = response.json()
        self.assertEqual(len(response_data['chat_messages']), 1)
        self.assertEqual(response_data['chat_messages'][0]['content'], "Another message")

