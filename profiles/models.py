from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils.translation import gettext_lazy as _

class Interest(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
            return self.name

    class Meta:
                verbose_name = "Interest"
                verbose_name_plural = "Interests"


class UserProfile(AbstractUser):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
        ('Prefer not to say', 'Prefer not to say'),
    ]
    INTERESTED_IN_CHOICES = [
        ('Men', 'Men'),
        ('Women', 'Women'),
        ('Both', 'Both'),
        ('None', 'None'),
    ]
    ACCOUNT_STATUS_CHOICES = [
            ('active', 'Active'),
            ('inactive', 'Inactive'),
            ('suspended', 'Suspended'),
    ]



    # Personal Information
    first_name = models.CharField(max_length=50, blank=True)
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=50, choices=GENDER_CHOICES, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    bio = models.TextField(blank=True)
    interested_in = models.CharField(max_length=50, choices=INTERESTED_IN_CHOICES, blank=True)


    feedback_count = models.PositiveIntegerField(default=0)
    unread_messages_count = models.PositiveIntegerField(default=0)
    swipes_count = models.PositiveIntegerField(default=0)
    account_status = models.CharField(
            max_length=50,
            choices=ACCOUNT_STATUS_CHOICES,
            default='active'
    )
    last_swipe = models.DateTimeField(null=True, blank=True)

    # location Information
    location = models.CharField(max_length=100, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)



    # Privacy and Communication
    blocked_users = models.ManyToManyField('self', symmetrical=False, blank=True)
    feedback_submitted = models.TextField(blank=True)
    show_age = models.BooleanField(default=True)
    show_location = models.BooleanField(default=False)
    show_distance = models.BooleanField(default=True)
    profile_visibility = models.BooleanField(default=True)

    # User Preferences and Settings
    show_me_in_discovery = models.BooleanField(default=True)
    search_distance = models.PositiveIntegerField(default=10)
    search_age_range_min = models.PositiveIntegerField(default=18)
    search_age_range_max = models.PositiveIntegerField(default=100)

    # Communication Preferences
    message_notifications = models.BooleanField(default=True)

    # Reporting and Blocking
    reports_made = models.IntegerField(default=0)


    groups = models.ManyToManyField(
            Group,
            verbose_name=_('groups'),
            blank=True,
            help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
            related_name="userprofile_set",
            related_query_name="userprofile",
        )

    user_permissions = models.ManyToManyField(
                Permission,
                verbose_name=_('user permissions'),
                blank=True,
                help_text=_('Specific permissions for this user.'),
                related_name="userprofile_set",
                related_query_name="userprofile",
            )

    class Meta:
            verbose_name = "User Profile"
            verbose_name_plural = "User Profiles"




class UserProfileImage(models.Model):
    user = models.ForeignKey(UserProfile, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image')

    def __str__(self):
        return f"{self.user.username}'s image"

    class Meta:
            verbose_name = "User Profile Image"
            verbose_name_plural = "User Profile Images"



class Match(models.Model):
    user1 = models.ForeignKey(UserProfile, related_name='matches_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(UserProfile, related_name='matches_user2', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Match between {self.user1.username} and {self.user2.username}"

    class Meta:
            verbose_name = "Match"
            verbose_name_plural = "Matches"


class Swipe(models.Model):
    swiper = models.ForeignKey(UserProfile, related_name='swipes_made', on_delete=models.CASCADE)
    swiped_on = models.ForeignKey(UserProfile, related_name='swipes_received', on_delete=models.CASCADE)
    liked = models.BooleanField(default=False)  # True for like (swipe right), False for pass (swipe left)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.swiper.username} swiped {'right' if self.liked else 'left'} on {self.swiped_on.username}"


class Message(models.Model):
    sender = models.ForeignKey(UserProfile, related_name='messages_sent', on_delete=models.CASCADE)
    receiver = models.ForeignKey(UserProfile, related_name='messages_received', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    class Meta:
            verbose_name = "Swipe"
            verbose_name_plural = "Swipes"


@receiver(post_save, sender=Message)
def update_unread_messages(sender, instance, created, **kwargs):
    if created:
        receiver = instance.receiver
        receiver.unread_messages_count += 1
        receiver.save()


class Report(models.Model):
    reported_user = models.ForeignKey(UserProfile, related_name='reports_received', on_delete=models.CASCADE)
    reporting_user = models.ForeignKey(UserProfile, related_name='user_reports_made', on_delete=models.CASCADE)
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Report by {self.reporting_user.username} on {self.reported_user.username}"

    class Meta:
            verbose_name = "Report"
            verbose_name_plural = "Reports"

class Feedback(models.Model):
    user = models.ForeignKey(UserProfile, related_name='feedbacks', on_delete=models.CASCADE)
    email = models.EmailField()
    message = models.TextField()
    read = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.user.username}"

    class Meta:
            verbose_name = "Feedback"
            verbose_name_plural = "Feedbacks"