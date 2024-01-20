from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.views import generic
from .models import Swipe,UserProfile
from .forms import CustomUserCreationForm
from .signup_forms import CustomSignupForm
from django.db.models import Count, Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



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

        # Debugging: Print the count and usernames after applying gender filter
        print("After gender filter:", query.count())
        print("Usernames:", list(query.values_list('username', flat=True)))

        # Further filter to include only users who are interested in the current user's gender
        if current_user.gender in ['Male', 'Female']:
            gender_to_interested_in = {'Male': 'Women', 'Female': 'Men'}
            user_interested_in = gender_to_interested_in.get(current_user.gender, 'Both')
            mutual_interest_filter = Q(interested_in=user_interested_in)

            query = query.exclude(mutual_interest_filter)

            # Debugging: Print the count and usernames after applying mutual interest filter
            print("After mutual interest filter:", query.count())
            print("Usernames:", list(query.values_list('username', flat=True)))


        print("After mutual If interest filter:", query.count())
        print("Usernames:", list(query.values_list('username', flat=True)))

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

        paginator = Paginator(query.prefetch_related('images'), 1)
        page = request.GET.get('page', 1)
        try:
            user_profiles = paginator.page(page)
        except PageNotAnInteger:
            user_profiles = paginator.page(1)
        except EmptyPage:
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
    Swipe.objects.get_or_create(swiper=request.user, swiped_on=swiped_on, liked=True)
    return redirect('next_profile')  # Redirect to the next profile

@login_required
def dislike_user(request, swiped_on_username):
    swiped_on = get_object_or_404(UserProfile, username=swiped_on_username)
    Swipe.objects.get_or_create(swiper=request.user, swiped_on=swiped_on, liked=False)
    return redirect('next_profile')  # Redirect to the next profile