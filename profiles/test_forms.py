from django.test import TestCase
from .forms import CustomUserCreationForm, ProfileForm, CustomUserChangeForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserProfile, Interest




class CustomUserCreationFormTest(TestCase):

    def test_custom_user_creation_form_validity(self):
        form_data = {
            'username': 'testuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'first_name': 'Test',
            'age': 25,
            'gender': 'Male',
            'bio': 'Test Bio',
            'interested_in': 'Women',
            'location': 'Test Location',
            'latitude': 12.345678,
            'longitude': 98.7654321,
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_custom_user_creation_form_invalid_data(self):
            form_data = {
                'username': '',  # Empty username to test for required field
                'password1': 'pass123',
                'password2': 'pass1234',  # Mismatched passwords
                'age': -1,  # Invalid age
                'gender': 'Unknown',  # Invalid gender
                'interested_in': 'Aliens',  # Invalid choice
                'location': '',  # Required field
                'latitude': 200,  # Out of valid range
                'longitude': 200,  # Out of valid range
            }
            form = CustomUserCreationForm(data=form_data)
            self.assertFalse(form.is_valid())
            self.assertIn('username', form.errors)
            self.assertIn('password2', form.errors)
            self.assertIn('age', form.errors)
            self.assertIn('gender', form.errors)
            self.assertIn('interested_in', form.errors)



class CustomUserChangeFormTest(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create_user('testuser', 'test@example.com', 'password123')
        self.interest = Interest.objects.create(name='Sample Interest')

    def test_change_form_validity(self):
        form_data = {
            'username': 'newtestuser',
            'email': 'newemail@example.com',
            'first_name': 'NewTest',
            'age': 26,
            'gender': 'Female',
            'interests': [self.interest.id],
            'location': 'NewTest Location',
            'latitude': 12.345678,
            'longitude': 98.7654321,
            'date_joined': self.user.date_joined,
            'feedback_count': self.user.feedback_count,
            'unread_messages_count': self.user.unread_messages_count,
            'swipes_count': self.user.swipes_count,
            'account_status': self.user.account_status,
            'search_distance': self.user.search_distance,
            'search_age_range_min': self.user.search_age_range_min,
            'search_age_range_max': self.user.search_age_range_max,
            'reports_made': self.user.reports_made
        }

        form = CustomUserChangeForm(data=form_data, instance=self.user)

        if not form.is_valid():
            print(form.errors)
        self.assertTrue(form.is_valid())


class ProfileFormTest(TestCase):

    def setUp(self):
        self.user = UserProfile.objects.create(
            username='testuser', email='test@example.com',
            first_name='Test', age=25, gender='Male',
            bio='Test Bio', interested_in='Women',
            location='Test Location', latitude=12.345678, longitude=98.7654321
        )
        self.interest = Interest.objects.create(name='Gaming')

    def test_profile_form_validity_with_valid_data(self):
        form_data = {
            'username': 'newtestuser',
            'email': 'newemail@example.com',
            'first_name': 'NewTest',
            'age': 26,
            'gender': 'Female',
            'interests': [self.interest.id],
            'bio': 'New Test Bio',
            'interested_in': 'Men',
            'location': 'New Test Location',
            'latitude': 23.456789,
            'longitude': 87.654321
        }
        form = ProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())

    def test_profile_form_invalidity_with_invalid_data(self):
            form_data = {
                'username': '',
                'email': 'invalidemail',
                'first_name': 'T' * 101,
                'age': -5,
                'gender': 'InvalidGender',
                'interests': ['invalid'],
                'interested_in': 'InvalidChoice',
                'location': 'L' * 101,
                'latitude': 200,
                'longitude': 200
            }
            form = ProfileForm(data=form_data, instance=self.user)
            self.assertFalse(form.is_valid())
            self.assertIn('username', form.errors)
            self.assertIn('email', form.errors)
            self.assertIn('first_name', form.errors)
            self.assertIn('age', form.errors)
            self.assertIn('gender', form.errors)
            self.assertIn('interests', form.errors)
            self.assertIn('interested_in', form.errors)


