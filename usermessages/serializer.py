# encoding=utf-8

from rest_framework import serializers

from accounts.models import User

from models import UserMessage


class UserMessageSerializer(serializers.ModelSerializer):
    """UserMessage serializer"""
    employer = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type_profile='employer'), required=False,
        allow_null=True)
    postulant = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(type_profile='postulant'), required=False,
        allow_null=True)

    class Meta:
        model = UserMessage
        fields = ('__all__')
