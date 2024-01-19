from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.views import generic
from .models import UserProfile
from .forms import CustomUserCreationForm
from .signup_forms import CustomSignupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage



@login_required
def my_profile(request):
    context = {'user': request.user}
    return render(request, 'profiles/my_profile.html', context)

class UserProfileListView(generic.ListView):
    template_name = 'profiles/index.html'
    paginate_by = 1


    def get_queryset(self):
        return UserProfile.objects.filter(is_superuser=False, is_active=True).prefetch_related('images')

def post_detail(request, username):
    profile = get_object_or_404(UserProfile, username=username)
    return render(request, 'profiles/profile_detail.html', {'profile': profile})

def home_view(request):
    if request.user.is_authenticated:
        user_profiles_list = UserProfile.objects.filter(is_superuser=False, is_active=True).prefetch_related('images')
        paginator = Paginator(user_profiles_list, 1)  # Show 1 profile per page

        page = request.GET.get('page', 1)
        try:
            user_profiles = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page
            user_profiles = paginator.page(1)
        except EmptyPage:
            # If page is out of range, redirect to the first page
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
