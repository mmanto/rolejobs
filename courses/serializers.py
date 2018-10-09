# encoding: utf-8

from rest_framework import serializers

from geo.serializers import GeoDataSerializer
from accounts.serializers import PublicUserSerializer

from models import (Course, CoursePostulation)


class CourseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'price',
            'currency_type_text',
            'course_type_text',
            'company',
            'company_logo',
        ]


class CourseEmployerSerializer(serializers.ModelSerializer):
    geo = GeoDataSerializer(read_only=True, source="geodata")

    class Meta:
        model = Course
        fields = [
            'id',
            'title',
            'description',
            'price',
            'currency_type',
            'currency_type_text',
            'course_type',
            'course_type_text',
            'company_data_from_owner',
            'company',
            'company_logo',
            'notify_by_email',
            'geo',
        ]
        read_only_fields = ['currency_type_text', 'course_type_text']


class CoursePostulationEmployerSerializer(serializers.ModelSerializer):
    course = CourseEmployerSerializer()
    user = PublicUserSerializer()

    class Meta:
        model = CoursePostulation
        fields = ['id', 'course', 'user']
