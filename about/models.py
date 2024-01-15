from django.db import models
from cloudinary.models import CloudinaryField

class About(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class TeamMember(models.Model):
    about = models.ForeignKey(About, related_name='team_members', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()
    image = CloudinaryField('image', blank=True, null=True)

    def __str__(self):
        return self.name
