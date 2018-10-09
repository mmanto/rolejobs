# encoding=utf-8

from rest_framework import serializers
# from rest_framework.validators import UniqueValidator
# from cities_light.models import City, Country, Region

from models import Institution, Language


class InstitutionSerializer(serializers.ModelSerializer):
    """Institutions serializer"""

    levels = serializers.ReadOnlyField(source="list_levels")

    class Meta:
        model = Institution
        exclude = (
            'created_at', 'updated_at', 'created_by', 'education_levels')


class LanguageSerializer(serializers.ModelSerializer):
    """Languages serializer"""

    class Meta:
        model = Language
