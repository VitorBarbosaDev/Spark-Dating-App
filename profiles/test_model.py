from django.test import TestCase
from .forms import CustomUserCreationForm, ProfileForm, CustomUserChangeForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Interest





class UserProfileModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        UserProfile.objects.create(username='testuser', first_name='Test')

    def test_first_name_label(self):
        user = UserProfile.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEquals(field_label, 'first name')

    def test_user_str_method(self):
        user = UserProfile.objects.get(id=1)
        expected_object_name = f'{user.username}'
        self.assertEquals(expected_object_name, str(user))






class UserProfileTest(TestCase):

    def setUp(self):
        Interest.objects.create(name='Gaming')
        self.user = UserProfile.objects.create_user(
            username='testuser', email='test@example.com',
            password='testpassword', first_name='Test',
            age=25, gender='Male', bio='Test Bio',
            interested_in='Women', location='Test Location'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, 'test@example.com')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.age, 25)
        self.assertEqual(self.user.gender, 'Male')
        self.assertEqual(self.user.bio, 'Test Bio')
        self.assertEqual(self.user.interested_in, 'Women')
        self.assertEqual(self.user.location, 'Test Location')
        self.assertEqual(self.user.search_distance, 10)
        self.assertEqual(self.user.search_age_range_min, 18)
        self.assertEqual(self.user.search_age_range_max, 100)
        self.assertEqual(self.user.account_status, 'active')
        self.assertTrue(self.user.profile_visibility)


    def test_user_str(self):
        self.assertEqual(str(self.user), 'testuser')

    def test_interest_assignment(self):
        gaming = Interest.objects.get(name='Gaming')
        self.user.interests.add(gaming)
        self.assertIn(gaming, self.user.interests.all())