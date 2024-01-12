from django.shortcuts import render
from django.http import HttpResponse
from django.views import generic
from .models import UserProfile
# Create your views here.


class UserProfileListView(generic.ListView):
    template_name = 'profiles/index.html'
    paginate_by = 1
    def get_queryset(self):
        return UserProfile.objects.filter(is_superuser=False, is_active=True)


