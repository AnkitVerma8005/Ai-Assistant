from django.db import models

from django.contrib.auth.models import User

class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chat_messages')
    role = models.CharField(max_length=10, choices=[('user', 'User'), ('ai', 'AI')])
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role.capitalize()} message by {self.user.username} at {self.created_at}"
