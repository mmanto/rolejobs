# -*- coding: utf8 -*-

from __future__ import unicode_literals
from django.contrib.auth import authenticate
from django.utils.translation import ugettext as _
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import ValidationError

from rest_auth.serializers import PasswordResetSerializer

from accounts.models import User
from accounts.forms import PasswordResetForm


class LoginSerializer(serializers.Serializer):
    """Login serializer"""
    email = serializers.EmailField(required=True, allow_blank=True)
    password = serializers.CharField(style={'input_type': 'password'})

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(email=email, password=password)

        # Did we get back an active user?
        if user:
            if not user.is_active:
                msg = _('User account is disabled.')
                raise ValidationError(msg)
        else:
            msg = _('Unable to log in with provided credentials.')
            raise ValidationError(msg)

        # Did the email confirmed

        if not user.status == user.S_ENABLED:
            raise ValidationError(_('E-mail is not verified.'))

        attrs['user'] = user
        return attrs


class PublicUserSerializer(serializers.ModelSerializer):
    """User public information serializer"""

    avatar = serializers.SerializerMethodField()

    def get_avatar(self, obj):
        try:
            avatar = obj.avatars.get(label="default")
            url = avatar.url
        except ObjectDoesNotExist:
            url = '/api/v1/avatars/profile/default'

        return url

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'avatar')


class UserSerializer(serializers.Serializer):

    first_name = serializers.CharField(required=True, allow_blank=False,
                                       max_length=250)
    last_name = serializers.CharField(required=True, allow_blank=False,
                                      max_length=250)
    city = serializers.CharField(required=False, allow_blank=True,
                                 max_length=250)
    email = serializers.EmailField(required=True, validators=[
                                        UniqueValidator(
                                            queryset=User.objects.all(),
                                            message="Email already registered"
                                        )
                                   ],
                                   allow_blank=False)

    password = serializers.CharField(required=True, write_only=True)

    last_update = serializers.DateTimeField(
        source="last_profile_update",
        read_only=True)

    def create(self, validated_data):
        """Create new User"""

        user = User.objects.create_user(
            username=validated_data.get("email"),
            email=validated_data.get('email'),
            password=validated_data.get("password")
        )

        user.city = validated_data.get("city")
        user.save()

        return user

    def update(self, instance, validated_data):
        raise Exception("No updateable")


class PasswordResetSerializer(PasswordResetSerializer):
    """Serializer for password reset"""

    password_reset_form_class = PasswordResetForm
