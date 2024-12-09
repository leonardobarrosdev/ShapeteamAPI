from rest_framework import serializers
from .models import Chat


class ChatSerializer(serializers.ModelSerializer):
	# is_me = serializers.SerializerMethodField()

	class Meta:
		model = Chat
		fields = [
			'id',
			# 'is_me',
            'user',
			'text',
			'created'
		]

	def get_is_me(self, obj):
		return self.context['user'] == obj.user

