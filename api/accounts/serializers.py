from .models import UserProfile
from rest_framework.serializers import ModelSerializer


class UserSerializer(ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'user_id', 'name']