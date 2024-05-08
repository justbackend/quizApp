from rest_framework.serializers import ModelSerializer, Serializer
from django.contrib.auth import get_user_model
User = get_user_model()


class UserRegisterSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['is_staff', 'is_active', 'date_joined', 'groups', 'user_permissions', 'is_superuser', 'last_login']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user
