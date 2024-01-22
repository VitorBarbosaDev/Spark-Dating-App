from django.shortcuts import render, redirect, get_object_or_404,redirect
from django.http import HttpResponse ,JsonResponse
from django.views import generic
from .models import Swipe,UserProfile,Match,UserProfileImage
from .forms import CustomUserCreationForm,ProfileForm
from .signup_forms import CustomSignupForm
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .utils import gender_icon_mapper ,icon_mapper
from django.urls import reverse
from django.contrib.auth import logout


@login_required
def my_profile(request):
    context = {'user': request.user}
    return render(request, 'profiles/my_profile.html', context)


def post_detail(request, username):
    profile = get_object_or_404(UserProfile, username=username)
    return render(request, 'profiles/profile_detail.html', {'profile': profile})


def home_view(request):
    if request.user.is_authenticated:
        current_user = request.user

        # Basic query excluding the current user and users not wanting to be discovered
        query = UserProfile.objects.filter(
            is_superuser=False, is_active=True, show_me_in_discovery=True
        ).exclude(username=current_user.username)

        # Mapping for gender preferences
        gender_preference = {'Men': ['Male'], 'Women': ['Female'], 'Both': ['Male', 'Female'], 'None': []}
        interested_genders = gender_preference.get(current_user.interested_in, [])
        query = query.filter(gender__in=interested_genders)



        # Further filter to include only users who are interested in the current user's gender
        if current_user.gender in ['Male', 'Female']:
            gender_to_interested_in = {'Male': 'Women', 'Female': 'Men'}
            user_interested_in = gender_to_interested_in.get(current_user.gender, 'Both')
            mutual_interest_filter = Q(interested_in=user_interested_in)

            query = query.exclude(mutual_interest_filter)


        # Filter out users who have blocked the current user
        query = query.exclude(blocked_users=current_user)

        #filter out users who have been blocked by the current user
        query = query.exclude(id__in=current_user.blocked_users.all())

        # Filter out users who have already been swiped on by the current user
        swiped_user_ids = Swipe.objects.filter(swiper=current_user).values_list('swiped_on_id', flat=True)
        query = query.exclude(id__in=swiped_user_ids)

        # Calculate matching score based on shared interests
        shared_interests_count = Count('interests', filter=Q(interests__in=current_user.interests.all()))
        query = query.annotate(shared_interests_count=shared_interests_count).order_by('-shared_interests_count')

        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            paginator = Paginator(query.prefetch_related('images'), 1)
            page = request.GET.get('page', 1)

            try:
                user_profiles = paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                return JsonResponse({'message': 'No more profiles available.'})

            if user_profiles.has_next():
                next_profile = user_profiles.object_list[0]
                data = {
                    'id': next_profile.id,
                    'username': next_profile.username,
                    'first_name': next_profile.first_name,
                    'age': next_profile.age,
                    'gender': next_profile.gender,
                    'bio': next_profile.bio,
                    'interests': [interest.name for interest in next_profile.interests.all()],
                    'images': images,
                    'genderIcon': gender_icon_mapper(next_profile.gender),  # You will need to implement this function based on your logic
                    'profile_url': reverse('profile_detail', kwargs={'username': next_profile.username}),

                }
                return JsonResponse(data)
            else:
                return JsonResponse({'message': 'No more profiles available.'})
        else:
            paginator = Paginator(query.prefetch_related('images'), 1)
            page = request.GET.get('page', 1)
            try:
                user_profiles = paginator.page(page)
            except (PageNotAnInteger, EmptyPage):
                return redirect('home')

        context = {'user_profiles': user_profiles}
    else:
        example_user = get_object_or_404(UserProfile, id=2)
        context = {'example_user': example_user}

    return render(request, 'profiles/index.html', context)











def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request)
            login(request, user)

            # Send a welcome email
            send_mail(
                subject='Welcome to Spark Dating App!',
                message=f'Hi {user.username},\n\nWelcome to Spark Dating App! We are excited to have you on board.\n\nEnjoy finding your match with us!\n\nCheers,\nThe Spark Dating App Team',
                from_email='noreply@spark-datingapp-8a011a2b31a3.herokuapp.com',
                recipient_list=[user.email],
                fail_silently=False,
            )


            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'account/signup.html', {'form': form})


@login_required
def like_user(request, swiped_on_username):
    swiped_on = get_object_or_404(UserProfile, username=swiped_on_username)
    swipe, created = Swipe.objects.get_or_create(
        swiper=request.user,
        swiped_on=swiped_on,
        defaults={'liked': True}
    )

    response_data = {'match': False}

    if created:
        # Check for mutual like
        if Swipe.objects.filter(swiper=swiped_on, swiped_on=request.user, liked=True).exists():
            Match.objects.create(user1=request.user, user2=swiped_on)
            response_data['match'] = True
            response_data['message'] = f"You matched with {swiped_on.username}!"

    next_profile = get_next_profile(request.user)
    if next_profile:
        response_data['next_profile'] = profile_to_dict(next_profile)

    return JsonResponse(response_data)

@login_required
def dislike_user(request, swiped_on_username):
    swiped_on = get_object_or_404(UserProfile, username=swiped_on_username)
    Swipe.objects.get_or_create(
        swiper=request.user,
        swiped_on=swiped_on,
        defaults={'liked': False}
    )

    next_profile = get_next_profile(request.user)
    if next_profile:
        response_data = {'success': True, 'next_profile': profile_to_dict(next_profile)}
    else:
        response_data = {'success': True, 'message': 'No more profiles available.'}

    return JsonResponse(response_data)

def get_next_profile(user):
    query = UserProfile.objects.filter(
        is_superuser=False, is_active=True, show_me_in_discovery=True
    ).exclude(username=user.username)

    # Replicate the gender preference filter
    gender_preference = {'Men': ['Male'], 'Women': ['Female'], 'Both': ['Male', 'Female'], 'None': []}
    interested_genders = gender_preference.get(user.interested_in, [])
    query = query.filter(gender__in=interested_genders)

    # Include mutual interest filter
    if user.gender in ['Male', 'Female']:
        gender_to_interested_in = {'Male': 'Women', 'Female': 'Men'}
        user_interested_in = gender_to_interested_in.get(user.gender, 'Both')
        mutual_interest_filter = Q(interested_in=user_interested_in)
        query = query.exclude(mutual_interest_filter)

    # Exclude users who have blocked the current user or are blocked by the current user
    query = query.exclude(blocked_users=user)
    query = query.exclude(id__in=user.blocked_users.all())

    # Exclude users already swiped on
    swiped_user_ids = Swipe.objects.filter(swiper=user).values_list('swiped_on_id', flat=True)
    query = query.exclude(id__in=swiped_user_ids)

    # Attempt to get the first profile from the filtered query
    next_profile = query.first()
    return next_profile


def profile_to_dict(profile):

    data = {
        'id': profile.id,
        'username': profile.username,
        'first_name': profile.first_name,
        'age': profile.age,
        'gender': profile.gender,
        'bio': profile.bio,
        'interests': [{'name': interest.name, 'icon': icon_mapper(interest)} for interest in profile.interests.all()],
        'images': [image.image.url for image in profile.images.all()],
        'genderIcon': gender_icon_mapper(profile.gender),
        'profile_url': reverse('profile_detail', kwargs={'username': profile.username}),
    }
    return data



@login_required
def profile_edit(request, username):
    user = get_object_or_404(UserProfile, username=username)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()

            # Handling additional image uploads
            for file in request.FILES.getlist('additional_images'):
                # Upload to Cloudinary and create UserProfileImage instance
                # Make sure to handle exceptions and errors
                UserProfileImage.objects.create(user=user, image=file)

            return redirect('my_profile')
    else:
        form = ProfileForm(instance=user)

    context = {'form': form, 'user': user}
    return render(request, 'profiles/profile_edit.html', context)


@login_required
def delete_image(request, image_id):
    image = get_object_or_404(UserProfileImage, id=image_id, user=request.user)
    image.delete()
    return redirect('profile_edit', username=request.user.username)


@login_required
def profile_delete(request, username):
    profile = get_object_or_404(UserProfile, username=username)
    if request.user.id == profile.id:
        profile.delete()
        return redirect('home')
    else:
        return redirect('profile_detail', username=username)
