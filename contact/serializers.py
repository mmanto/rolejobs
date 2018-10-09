# encoding=utf-8

from rest_framework import serializers


class ContactSerializer(serializers.Serializer):
    """Contact info serializer"""

    name = serializers.CharField(
        max_length=250)

    phone = serializers.CharField(
        max_length=250)

    email = serializers.EmailField()

    subject = serializers.CharField(
        max_length=250)

    message = serializers.CharField(
        max_length=4096)
