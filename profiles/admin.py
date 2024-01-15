from django.contrib import admin
from .models import UserProfile, Interest, UserProfileImage, Match, Swipe, Message, Report, Feedback
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django_summernote.admin import SummernoteModelAdmin

# Inline model for UserProfileImage
class UserProfileImageInline(admin.StackedInline):
    model = UserProfileImage
    extra = 1  # Number of extra forms to display

# Inline model for Interest
class InterestInline(admin.TabularInline):
    model = UserProfile.interests.through
    extra = 1

# Customizing UserProfile Admin
@admin.register(UserProfile)
class UserProfileAdmin(SummernoteModelAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    list_display = ('username', 'email', 'age', 'gender', 'account_status')
    list_filter = ('gender', 'account_status')
    search_fields = ('username', 'email')
    inlines = [UserProfileImageInline, InterestInline]


    summernote_fields = ('bio',)

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
@admin.register(Swipe)
class SwipeAdmin(admin.ModelAdmin):
    list_display = ('swiper', 'swiped_on', 'liked', 'timestamp')
    list_filter = ('liked',)
    search_fields = ('swiper__username', 'swiped_on__username')

@admin.register(Message)
class MessageAdmin(SummernoteModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'read')
    list_filter = ('read',)
    search_fields = ('sender__username', 'receiver__username')
    summernote_fields = ('content',)


@admin.register(Report)
class ReportAdmin(SummernoteModelAdmin):
    list_display = ('reported_user', 'reporting_user', 'timestamp')
    search_fields = ('reported_user__username', 'reporting_user__username')
    summernote_fields = ('reason',)


@admin.register(Feedback)
class FeedbackAdmin(SummernoteModelAdmin):
    list_display = ('user', 'email', 'timestamp', 'read')
    list_filter = ('read',)
    search_fields = ('user__username', 'email')
    summernote_fields = ('message',)


# Registering models with their custom admin classes
admin.site.register(Interest, InterestAdmin)
admin.site.register(Match, MatchAdmin)

