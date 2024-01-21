from django.db import models
from profiles.models import UserProfile

class Message(models.Model):
    sender = models.ForeignKey(
        UserProfile, 
        related_name='messaging_messages_sent', 
        on_delete=models.CASCADE
    )
    receiver = models.ForeignKey(
        UserProfile, 
        related_name='messaging_messages_received', 
        on_delete=models.CASCADE
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.sender.username} to {self.receiver.username}"

    class Meta:
        ordering = ['timestamp']
