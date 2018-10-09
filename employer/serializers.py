
from django.utils.translation import gettext as _

from rest_framework import serializers
# from rest_framework.validators import UniqueValidator

from drf_braces.serializers.form_serializer import FormSerializer
from taggit_serializer.serializers import (
    TagListSerializerField, TaggitSerializer)

from accounts.models import User
from accounts.serializers import PublicUserSerializer
from jobs.models import Job, JobPostulation, JobPostulationNote

from models import (
    Employer, CVRequest, CVREQUEST_REJECTED, CVREQUEST_ACCEPTED, CVTags
)

from forms import SignupForm


class EmployerSerializer(serializers.ModelSerializer):
    """Employer, basic information"""

    email = serializers.EmailField(read_only=True)

    class Meta:
        model = Employer
        fields = [
            'first_name',
            'last_name',
            'email',
            'gender',
            'phone_number',
            'mobile_number',
            'name_company',
            'razon_social',
            'responsability_iva',
            'address',
            'city',
            'region',
            'country',
            'sector_empresarial',
            'workforce',
            'tipology',
            'description',
            'website',
            'cuit',
            'newsletter',
            'cv_spontany',
            'position'
        ]


class SignupSerializer(FormSerializer):
    """Employer signup serializer"""

    class Meta(object):
        form = SignupForm

    def create(self, validated_data):
        user = None
        employer = None

        try:

            user = User.objects.create_user(
                email=validated_data.get('email'),
                password=validated_data.get('password1'),
                first_name=validated_data.get('first_name'),
                last_name=validated_data.get('last_name'),
                type_profile="employer"
            )

            employer = Employer()

            employer.user = user

            employer.gender = validated_data.get('gender')
            employer.phone_number = validated_data.get('phone_number')
            employer.mobile_number = validated_data.get('mobile_number')

            employer.position = validated_data.get('position')
            employer.name_company = validated_data.get('name_company')
            employer.razon_social = validated_data.get('razon_social')
            employer.responsability_iva = validated_data.get(
                                                        'responsability_iva')
            employer.address = validated_data.get('address')
            employer.city_id = validated_data.get('city', None)
            employer.region_id = validated_data.get('region')
            employer.country_id = validated_data.get('country')
            employer.sector_empresarial = validated_data.get(
                                                        'sector_empresarial')
            employer.workforce = validated_data.get('workforce')
            employer.tipology = validated_data.get('tipology')
            employer.description = validated_data.get('description')
            employer.website = validated_data.get('website')
            employer.cuit = validated_data.get('cuit')
            # employer.logo = validated_data.get('logo')
            employer.reference = validated_data.get('reference')
            employer.newsletter = validated_data.get('newsletter')
            employer.cv_spontany = validated_data.get('cv_spontany')

            employer.save()

            user.send_validation_email()

        except Exception, e:

            if employer:
                try:
                    employer.delete()
                except:
                    pass

            if user:
                user.delete()

            raise e

        return validated_data


class EmployerPublicInformation(serializers.ModelSerializer):
    """Employer for public information"""

    avatars = serializers.JSONField()

    class Meta:
        model = Employer
        fields = (
            'name_company',
            'country',
            'avatars'
        )


# Rewriter here for a cross-dependencies issue
class JobsSimpleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Job
        fields = ('id', 'title')


class PostulationsListSerializer(serializers.ModelSerializer):
    """Postulation for employer"""

    user = PublicUserSerializer(read_only=True)
    job = JobsSimpleSerializer(read_only=True)
    status_text = serializers.ReadOnlyField()

    class Meta:
        model = JobPostulation
        fields = (
            'job',
            'user',
            'status',
            'status_text')


class CVRequestListSerializer(serializers.ModelSerializer):
    """CVRequest for employer"""

    user = PublicUserSerializer(read_only=True)
    status_text = serializers.ReadOnlyField()

    class Meta:
        model = CVRequest
        fields = (
            'id',
            'user',
            'status',
            'status_text')


class CVRequestStatusSerializer(serializers.Serializer):
    """CVRequest status serializer"""

    status = serializers.ChoiceField(
        required=True,
        allow_null=False,
        choices=(
            (CVREQUEST_ACCEPTED, _(u"Aceptada")),
            (CVREQUEST_REJECTED, _(u"Rechazada")),
        ))


class JobPostulationNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobPostulationNote
        fields = ('id', 'postulation', 'title', 'body')


class CVTagsSerializer(TaggitSerializer, serializers.ModelSerializer):
    """CVTags for employer"""

    user = PublicUserSerializer()
    tags = TagListSerializerField()

    class Meta:
        model = CVTags
        fields = (
            'id',
            'user',
            'tags',
        )
