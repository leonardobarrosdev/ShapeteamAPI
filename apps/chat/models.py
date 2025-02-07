from django.db import models
from ..shapeteam.models import Connection
from ..user.models import CustomUser


class Chat(models.Model):
	connection = models.ForeignKey(Connection, related_name='messages', on_delete=models.CASCADE)
	user = models.ForeignKey(CustomUser, related_name='my_messages', on_delete=models.CASCADE)
	text = models.TextField()
	created = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.user.first_name + ': ' + self.text
