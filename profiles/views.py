from django.shortcuts import render, get_object_or_404,redirect
from django.http import HttpResponse
from django.views import generic
from .models import UserProfile
from .forms import CustomUserCreationForm
from .signup_forms import CustomSignupForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required



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



def signup_view(request):
    if request.method == 'POST':
        form = CustomSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(request)
            login(request, user)

            # Send a welcome email
            send_mail(
                subject='Welcome to Spark Dating App!',
                message='Hi {username},\n\nWelcome to Spark Dating App! We are excited to have you on board.\n\nEnjoy finding your match with us!\n\nCheers,\nThe Spark Dating App Team'.format(username=user.username),
                from_email='sparkdating69@gmail.com',
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')
    else:
        form = CustomSignupForm()
    return render(request, 'account/signup.html', {'form': form})
