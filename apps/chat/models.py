from django.db import models
from django.contrib.auth import get_user_model
from apps.shapeteam.models import Connection


User = get_user_model()

class Message(models.Model):
    contact = models.ForeignKey(User, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.contact.username


class Chat(models.Model):
    participant = models.ForeignKey(Connection, related_name='chats', on_delete=models.CASCADE)
    messages = models.ManyToManyField(Message, blank=True)

    def __str__(self):
        return "{}".format(self.pk)