from rest_framework import serializers
from apps.users.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'name', 'email', 'name', 'nickname', 'contact',
				  'is_active', 'is_staff', 'is_admin', 'is_superuser', 'last_login', 'created_at', 'updated_at']