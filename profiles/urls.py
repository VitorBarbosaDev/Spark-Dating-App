from . import views
from django.urls import path
from .views import signup_view


urlpatterns = [
    path('', views.home_view, name='home'),
    path('profiles/', views.UserProfileListView.as_view(), name='profiles'),
    path('profile/<str:username>/', views.post_detail, name='profile_detail'),
]

