from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import generic
from .models import UserProfile
# Create your views here.


class UserProfileListView(generic.ListView):
    template_name = 'profiles/index.html'
    paginate_by = 1

    def get_queryset(self):
        return UserProfile.objects.filter(is_superuser=False, is_active=True).prefetch_related('images')

def post_detail(request, username):
    profile = get_object_or_404(UserProfile, username=username)
    return render(request, 'profiles/profile_detail.html', {'profile': profile})


