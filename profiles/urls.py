from . import views
from django.urls import path



urlpatterns = [
    path('', views.UserProfileListView.as_view(), name='home'),
     path('profile/<str:username>/', views.post_detail, name='profile_detail'),
]
