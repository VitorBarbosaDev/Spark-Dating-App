from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('matches/', views.match_list, name='match_list'),  # List of matches
    path('chat/<str:username>/', views.chat_view, name='chat'),  # Individual chat view
    path('chat/<str:username>/get_new_messages/', views.get_new_messages, name='get_new_messages'),

]