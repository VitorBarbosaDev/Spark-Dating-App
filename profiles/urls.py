from . import views
from django.urls import path
from .views import signup_view


urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/<str:username>/', views.post_detail, name='profile_detail'),
    path('like/<str:swiped_on_username>/', views.like_user, name='like_user'),
    path('dislike/<str:swiped_on_username>/', views.dislike_user, name='dislike_user'),
]

