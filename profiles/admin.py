from django.contrib import admin
from .models import UserProfile, Interest, UserProfileImage, Match, Swipe, Message, Report, Feedback
from .forms import CustomUserCreationForm, CustomUserChangeForm

# Inline model for UserProfileImage
class UserProfileImageInline(admin.StackedInline):
    model = UserProfileImage
    extra = 1  # Number of extra forms to display

# Inline model for Interest
class InterestInline(admin.TabularInline):
    model = UserProfile.interests.through
    extra = 1

# Customizing UserProfile Admin
class UserProfileAdmin(admin.ModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = UserProfile
    list_display = ('username', 'email', 'age', 'gender', 'account_status')
    list_filter = ('gender', 'account_status')
    search_fields = ('username', 'email')
    inlines = [UserProfileImageInline, InterestInline]

    # Overriding get_form to use different forms for add and change actions
    def get_form(self, request, obj=None, **kwargs):
        if obj:
            kwargs['form'] = self.form
        else:
            kwargs['form'] = self.add_form
        return super().get_form(request, obj, **kwargs)




# Customizing Interest Admin
class InterestAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# Customizing UserProfileImage Admin
class UserProfileImageAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')
    search_fields = ('user__username',)



# Customizing Match Admin
class MatchAdmin(admin.ModelAdmin):
    list_display = ('user1', 'user2', 'timestamp')
    search_fields = ('user1__username', 'user2__username')

# Customizing Swipe Admin
class SwipeAdmin(admin.ModelAdmin):
    list_display = ('swiper', 'swiped_on', 'liked', 'timestamp')
    list_filter = ('liked',)
    search_fields = ('swiper__username', 'swiped_on__username')

# Customizing Message Admin
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'read')
    list_filter = ('read',)
    search_fields = ('sender__username', 'receiver__username')

# Customizing Report Admin
class ReportAdmin(admin.ModelAdmin):
    list_display = ('reported_user', 'reporting_user', 'timestamp')
    search_fields = ('reported_user__username', 'reporting_user__username')

# Customizing Feedback Admin
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'email', 'timestamp', 'read')
    list_filter = ('read',)
    search_fields = ('user__username', 'email')

# Registering models with their custom admin classes
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Interest, InterestAdmin)
admin.site.register(Match, MatchAdmin)
admin.site.register(Swipe, SwipeAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Feedback, FeedbackAdmin)
