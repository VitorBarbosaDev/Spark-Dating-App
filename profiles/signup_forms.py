from django import forms
from allauth.account.forms import SignupForm
from .models import UserProfile, Interest, UserProfileImage
from PIL import Image

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    age = forms.IntegerField(initial=18, required=False)  # Set default age to 18
    gender = forms.ChoiceField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other'), ('Prefer not to say', 'Prefer not to say')], required=False)
    interested_in = forms.ChoiceField(choices=[('Men', 'Men'), ('Women', 'Women'), ('Both', 'Both'), ('None', 'None')])
    bio = forms.CharField(widget=forms.Textarea, required=False)
    image1 = forms.ImageField(required=False)
    image2 = forms.ImageField(required=False)
    image3 = forms.ImageField(required=False)
    image4 = forms.ImageField(required=False)
    image5 = forms.ImageField(required=False)
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.age = self.cleaned_data.get('age', None)
        user.gender = self.cleaned_data.get('gender', '')
        user.interested_in = self.cleaned_data.get('interested_in', '')
        user.bio = self.cleaned_data.get('bio', '')
        user.save()

        # Handling images
        for field_name in ['image1', 'image2', 'image3', 'image4', 'image5']:
            image = self.cleaned_data.get(field_name)
            if image:
                UserProfileImage.objects.create(user=user, image=image)

        # Handling interests
        interests = self.cleaned_data.get('interests')
        for interest in interests:
            user.interests.add(interest)