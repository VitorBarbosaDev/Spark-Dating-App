from django.db.models import Q
from django.shortcuts import render, redirect
from profiles.models import UserProfile,Match
from django.contrib.auth.decorators import login_required
from .models import Message

@login_required
def match_list(request):
    # Get the current user's profile
    user_profile = UserProfile.objects.get(username=request.user.username)

    # Find matches where the current user is either user1 or user2
    matches = Match.objects.filter(Q(user1=user_profile) | Q(user2=user_profile))

    # Extract the user profiles from these matches
    matched_profiles = []
    for match in matches:
        if match.user1 != user_profile:
            matched_profiles.append(match.user1)
        else:
            matched_profiles.append(match.user2)

    return render(request, 'messaging/match_list.html', {'matched_profiles': matched_profiles})


@login_required
def chat_view(request, username):
    try:
        other_user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return redirect('messaging:match_list')

    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            # Use request.user directly since it's already an instance of UserProfile
            Message.objects.create(sender=request.user, receiver=other_user, content=content)
            return redirect('messaging:chat', username=username)

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'messaging/chat.html', {'other_user': other_user, 'messages': messages})



