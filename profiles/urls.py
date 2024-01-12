from . import views
from django.urls import path



urlpatterns = [
    path('', views.UserProfileListView.as_view(), name='home'),
]
