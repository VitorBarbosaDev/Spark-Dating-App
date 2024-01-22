from django.test import TestCase
from .forms import CustomUserCreationForm, ProfileForm, CustomUserChangeForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Interest, Swipe, Match


class ViewTestCase(TestCase):

    def setUp(self):
            # Create a test user and profile
            self.user = UserProfile.objects.create_user(
                username='testuser', email='test@example.com', password='12345',
                first_name='Test', age=25, gender='Male', bio='Test Bio',
                interested_in='Women', location='Test Location'
            )
            self.other_user = UserProfile.objects.create_user(
                username='otheruser', email='other@example.com', password='67890',
                first_name='Test', age=25, gender='Female', bio='Test Bio',
                interested_in='Men', location='Test Location'
            )
            self.interest = Interest.objects.create(name='Gaming')
            self.other_interest = Interest.objects.create(name='Gaming')
            # Log in the user for tests that require authentication
            self.client.login(username='testuser', password='12345')


    def test_my_profile_view(self):
        response = self.client.get(reverse('my_profile'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/my_profile.html')
        self.assertEqual(response.context['user'], self.user)

    def test_post_detail_view(self):
        response = self.client.get(reverse('profile_detail', args=[self.user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/profile_detail.html')
        self.assertEqual(response.context['profile'], self.user)

    def test_home_view_authenticated(self):
            response = self.client.get(reverse('home'))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'profiles/index.html')
            # Check if 'user_profiles' is in context for authenticated user
            self.assertIn('user_profiles', response.context)

    def test_home_view_unauthenticated(self):
        self.client.logout()
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'profiles/index.html')
                # Check if 'example_user' is in context for unauthenticated user
        self.assertIn('example_user', response.context)

    def test_like_user(self):
            # Create a swipe to simulate the other user liking the test user first (to test match creation)
        Swipe.objects.create(swiper=self.other_user, swiped_on=self.user, liked=True)

            # Now, test user likes the other user
        response = self.client.post(reverse('like_user', args=[self.other_user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Swipe.objects.filter(swiper=self.user, swiped_on=self.other_user, liked=True).exists())

            # Check for the creation of Match if mutual like
        self.assertTrue(Match.objects.filter(user1=self.user, user2=self.other_user).exists() or
            Match.objects.filter(user1=self.other_user, user2=self.user).exists())

    def test_dislike_user(self):
        response = self.client.post(reverse('dislike_user', args=[self.other_user.username]))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Swipe.objects.filter(swiper=self.user, swiped_on=self.other_user, liked=False).exists())
