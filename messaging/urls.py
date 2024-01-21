from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('matches/', views.match_list, name='match_list'),  # List of matches
    path('chat/<str:username>/', views.chat_view, name='chat'),  # Individual chat view
]