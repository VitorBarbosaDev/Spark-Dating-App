from django.db.models import Q
from django.shortcuts import render, redirect
from profiles.models import UserProfile,Match
from django.contrib.auth.decorators import login_required
from .models import Message
from django.http import JsonResponse

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

    chat_messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'messaging/chat.html', {'other_user': other_user, 'chat_messages': chat_messages})


@login_required
def get_new_messages(request, username):
    try:
        other_user = UserProfile.objects.get(username=username)
    except UserProfile.DoesNotExist:
        return JsonResponse({'error': 'User not found'}, status=404)

    last_message_id = request.GET.get('last_message_id')
    if last_message_id:
        new_messages = Message.objects.filter(
            Q(sender=request.user, receiver=other_user) | Q(sender=other_user, receiver=request.user),
            id__gt=last_message_id
        ).order_by('timestamp')
    else:
        new_messages = Message.objects.none()

    chat_messages_data = [{
        'id': message.id,
        'sender': message.sender.username,
        'content': message.content,
        'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
    } for message in new_messages]

    return JsonResponse({'chat_messages': chat_messages_data})



