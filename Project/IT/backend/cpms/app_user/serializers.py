from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

__all__ = [
    'RegisterSerializer',
    'UserProfileSerializer'
]

User = get_user_model()


class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=32, validators=[UniqueValidator(queryset=User.objects.all())],
                                     required=False)
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())], required=False)

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'password',
            'email',
            'first_name',
            'last_name',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined'
        ]

        read_only_fields = [
            'id',
            'is_staff',
            'is_active',
            'is_superuser',
            'last_login',
            'date_joined'
        ]

        extra_kwargs = {
            'password': {'write_only': True}
        }

    @transaction.atomic
    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.save()

        return instance
