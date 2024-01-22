from . import views
from django.urls import path
from .views import signup_view


urlpatterns = [
    path('', views.home_view, name='home'),
    path('profile/<str:username>/', views.post_detail, name='profile_detail'),
    path('like/<str:swiped_on_username>/', views.like_user, name='like_user'),
    path('dislike/<str:swiped_on_username>/', views.dislike_user, name='dislike_user'),
    path('profile/<str:username>/edit/', views.profile_edit, name='profile_edit'),
    path('profile/<str:username>/delete/', views.profile_delete, name='profile_delete'),
    path('delete_image/<int:image_id>/', views.delete_image, name='delete_image'),
    path('profile/<str:username>/delete/', views.profile_delete, name='profile_delete'),
]

