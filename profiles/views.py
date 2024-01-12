from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import UserProfile
# Create your views here.



class UserProfileListView(generic.ListView):
    template_name = 'profiles/profiles.html'

    def get_queryset(self):
        # Excludes any user where is_superuser is True
        return UserProfile.objects.filter(is_superuser=False)

