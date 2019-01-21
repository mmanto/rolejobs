# encoding=utf-8

from django.utils.translation import gettext as _

from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from utils.serializers import ChoicesSerializer, SlugedItemSerializer
from accounts.models import User

from education.models import (
    UserEducation,
    Institution,
    UserLanguages,
    UserComputerknowledge,
    UserAdditionalknowledge,
    UserCertification
)

from jobs.models import Job, JobPostulation, FavoriteJob
from employer.serializers import EmployerPublicInformation
from employer.models import CVRequest

from models import (
    Postulant,
    Biographic,
    ProfessionalExperience,
    ProfessionalReference,
    PostulantAttachCV,
)


class PostulantSerializer(serializers.ModelSerializer):
    """Postulant, basic information"""

    email = serializers.EmailField(read_only=True)
    first_name = serializers.CharField(read_only=False)
    last_name = serializers.CharField(read_only=False)
    completed = serializers.ReadOnlyField()
    last_update = serializers.ReadOnlyField()

    class Meta:
        model = Postulant
        fields = [
            # profile
            'email',
            'first_name',
            'last_name',
            'gender',
            'phone_number',
            'mobile_number',
            'address',
            'city',
            'region',
            'country',
            # postulant
            'category',
            'marital_status',
            'dni',
            'date_of_birth',
            'country_of_birth',
            'postal_code',
            'driver_license',
            'own_vehicle',
            'has_disability',
            'completed',
            'last_update',
        ]

    def create(self, validated_data, *args, **kwargs):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")
        user = validated_data.get("user")

        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return super(PostulantSerializer, self).create(
                                            validated_data, *args, **kwargs)

    def update(self, instance, validated_data, *args, **kwargs):
        first_name = validated_data.pop("first_name")
        last_name = validated_data.pop("last_name")

        instance.user.first_name = first_name
        instance.user.last_name = last_name
        instance.user.save()

        return super(PostulantSerializer, self).update(
                                    instance, validated_data, *args, **kwargs)


class SignupSerializer(serializers.Serializer):

    first_name = serializers.CharField(required=True, allow_blank=False,
                                       max_length=250)
    last_name = serializers.CharField(required=True, allow_blank=False,
                                      max_length=250)
    email = serializers.EmailField(required=True, validators=[
                                        UniqueValidator(
                                            queryset=User.objects.all(),
                                            message="Email already registered"
                                        )
                                   ],
                                   allow_blank=False)
    password = serializers.CharField(required=True)

    def create(self, validated_data):
        """Create new User"""

        user = User.objects.create_user(
            email=validated_data.get('email'),
            password=validated_data.get("password")
        )

        try:
            user.first_name = validated_data.get("first_name")
            user.last_name = validated_data.get("last_name")
            user.type_profile = "postulant"

            user.save()
            user.send_validation_email()

        except Exception, e:
            user.delete()
            raise e

        return {
            "first_name": user.first_name,
            "last_name": user.last_name,
            "email": user.email,
            "password": None
        }

    def update(self, instance, validated_data):
        raise Exception("Not supported")


class BiographicSerializer(serializers.ModelSerializer):
    """Postulant, biographic"""

    user = serializers.CharField(read_only=True)

    class Meta:
        model = Biographic
        fields = [
            'user',
            'description'
        ]


class ProfessionalReferenceListSerializer(serializers.ListSerializer):
    """Professional references list serializer"""

    def create(self, validated_data):
        references = [ProfessionalReference(**item) for item in validated_data]
        return ProfessionalReference.objects.bulk_create(references)

    def update(self, instance, validated_data):
        mapping = {reference.id: reference for reference in instance}
        data = {item['id']: item for item in validated_data}

        ret = []

        for id, d in data.items():
            reference = mapping.get(id, None)

            if reference is None:
                ret.append(self.child.create(d))
            else:
                ret.append(self.child.update(reference, d))

        for id, reference in mapping.items():
            if id not in data:
                reference.delete()

        return ret


class ProfessionalReferenceSerializer(serializers.ModelSerializer):
    """Professional experience references"""

    id = serializers.IntegerField(
        read_only=False,
        required=False,
        allow_null=True)

    type_text = serializers.CharField(
        read_only=True)

    class Meta:
        model = ProfessionalReference
        list_serializer_class = ProfessionalReferenceListSerializer
        exclude = (
            'created_at', 'updated_at', 'created_by',
            'experience', 'confirmed')


class ProfessionalExperienceSerializer(serializers.ModelSerializer):
    """ProfessionalExperience serializer"""

    position_value = serializers.CharField(
        source="position", read_only=True)

    title_value = serializers.CharField(
        source="title", read_only=True)

    hierarchy_value = serializers.CharField(
        source="hierarchy", read_only=True)

    area_value = serializers.CharField(
        source="area", read_only=True)

    subarea_value = serializers.CharField(
        source="subarea", read_only=True)

    branch_activity_value = serializers.CharField(
        source="branch_activity", read_only=True)

    references = ProfessionalReferenceSerializer(
        many=True,
        read_only=False)

    def validate(self, data):
        """ Check """

        if data['is_current'] and data['end_date'] is not None:
            raise serializers.ValidationError(_(u"Si el puesto es actual, " +
                                                u" no puede tener fecha de " +
                                                u"finalización"))

        elif not data['is_current'] and data['end_date'] is None:
            raise serializers.ValidationError(_(u"Debe definir una fecha, " +
                                                u"de finalización"))

        if data['end_date'] is not None:
            if data['start_date'] > data['end_date']:
                raise serializers.ValidationError(_(u"La fecha de inicio no " +
                                                    u"puede ser mayor a la " +
                                                    u"fecha de finalización"))

        return data

    def create_references(self, references, experience):

        for r in references:
            r.update({
                "experience": experience,
                "created_by": experience.user,
            })

        references = [
            ProfessionalReference(**reference) for reference in references]

        return ProfessionalReference.objects.bulk_create(references)

    def create(self, validated_data):
        references = validated_data.pop('references')
        pexperience = super(ProfessionalExperienceSerializer, self).create(
            validated_data)

        try:
            self.create_references(references, pexperience)
        except Exception, e:
            pexperience.delete()
            raise e

        return pexperience

    def update(self, instance, validated_data):
        references = validated_data.pop('references')
        experience = super(ProfessionalExperienceSerializer, self).update(
            instance,
            validated_data)

        new_references = [r for r in references
                          if r.get("id", None) is None]

        to_update = {r["id"]: r for r in references
                     if r.get("id", None) is not None}

        actuals = {r.id: r for r in instance.references.all()}

        self.create_references(new_references, experience)

        for id, reference in actuals.items():
            if id in to_update:
                data = to_update.get(id)
                reference.name = data.get("name", reference.name)
                reference.type = data.get("type", reference.type)
                reference.email = data.get("email", reference.email)
                reference.phone = data.get("phone", reference.phone)
                reference.save()
            else:
                reference.delete()

        return experience

    class Meta:
        model = ProfessionalExperience
        exclude = ('created_at', 'updated_at', 'user')


class PublicProfecionalExperienceSerializer(ProfessionalExperienceSerializer):

    salary = serializers.SerializerMethodField()
    currency = serializers.SerializerMethodField()

    def get_salary(self, obj):
        if (obj.show_salary):
            return obj.salary,
        else:
            return None

    def get_currency(self, obj):
        if (obj.show_salary):
            return obj.currency
        else:
            return None


class PostulantCertificationSerializer(serializers.ModelSerializer):
    """User Certification Serializer"""

    type_text = serializers.ReadOnlyField()

    class Meta:
        model = UserCertification
        exclude = (
            'created_at', 'updated_at', 'education')


class PostulantEducationSerializer(serializers.ModelSerializer):
    """Postulant education serialiser"""

    institution = serializers.CharField(
        required=False,
        source="institution.name")

    institution_id = serializers.IntegerField(
        required=False,
        source="institution.id")

    level_text = serializers.CharField(
        read_only=True)

    certifications = PostulantCertificationSerializer(
        many=True,
        read_only=False)

    def fill_institucion(self, data):
        institution_taked = data.get("institution")
        institution_id = institution_taked.get("id", None)
        institution_name = institution_taked.get("name", None)
        level = data.get('level', 0)

        if institution_id:
            institution = Institution.objects.get(
                id=institution_id)

        elif institution_name:
            institution = Institution.objects.get_or_create(
                name=institution_name,
                defaults={
                    "education_levels": data.get("level", 0),
                    "created_by": data.get("user")
                })[0]

        if level and not institution.is_level(level):
            institution.add_level(level)

        data.update({
            "institution": institution
        })

        return data

    def validate(self, data):
        is_current = data.get('is_current', False)
        finished = data.get('finished', False)
        start_date = data.get('start_date', None)
        end_date = data.get('end_date', None)

        if "institution" not in data:
            raise serializers.ValidationError(_(u"Debe definir una institu" +
                                                "ción"))

        if is_current and end_date is not None:
            raise serializers.ValidationError(_(u"Si está actualmente " +
                                                u"cursando, no puede tener " +
                                                u"fecha de finalización"))

        elif not is_current and end_date is None:
            raise serializers.ValidationError(_(u"Debe definir una fecha, " +
                                                u"de finalización"))
        if is_current and finished:
            raise serializers.ValidationError(_(u"No se puede marcar como" +
                                                u" terminado si está en " +
                                                u"curso"))

        if end_date is not None:
            if start_date > end_date:
                raise serializers.ValidationError(_(u"La fecha de inicio no " +
                                                    u"puede ser mayor a la " +
                                                    u"fecha de finalización"))

        # Search education
        data = self.fill_institucion(data)

        return data

    def create_certifications(self, education, certifications):
        for cert in certifications:
            cert.update({
                "education": education,
            })

        certifications = [
            UserCertification(**cert) for cert in certifications]

        return UserCertification.objects.bulk_create(certifications)

    def create(self, validated_data):
        certifications = validated_data.pop("certifications")
        education = super(PostulantEducationSerializer, self).create(
            validated_data)

        try:
            self.create_certifications(education, certifications)
        except Exception, e:
            education.delete()
            raise e

        return education

    def update(self, instance, validated_data):
        certifications = validated_data.pop('certifications')

        education = super(PostulantEducationSerializer, self).update(
            instance,
            validated_data)

        new_certifications = [r for r in certifications
                              if r.get("id", None) is None]

        to_update = {r["id"]: r for r in certifications
                     if r.get("id", None) is not None}

        actuals = {r.id: r for r in instance.certifications.all()}

        self.create_certifications(education, new_certifications)

        for id, certification in actuals.items():
            if id in to_update:
                data = to_update.get(id)
                certification.name = data.get(
                    "name", certification.name)
                certification.description = data.get(
                    "description", certification.description)
                certification.type = data.get(
                    "type", certification.type)
                certification.number_certification = data.get(
                    "number_certification", certification.number_certification)
                certifications.number_examen = data.get(
                    "number_examen", certification.number_examen)
                certification.save()
            else:
                certification.delete()

        return education

    class Meta:
        model = UserEducation
        exclude = ('user', 'created_at', 'updated_at')


class PostulantLanguagesSerializer(serializers.ModelSerializer):
    """Postulant languages serialiser"""

    language_text = serializers.ReadOnlyField(
        source="language.name")

    class Meta:
        model = UserLanguages
        fields = ('language', 'language_text', 'level')

class PostulantComputerknowledgesSerializer(serializers.ModelSerializer):
    """Postulant computerknowledge serializer"""

    computerknowledge_text = serializers.ReadOnlyField(
        source="computerknowledge.name")

    class Meta:
        model = UserComputerknowledge
        fields = ('computerknowledge', 'computerknowledge_text', 'level')

class PostulantAdditionalknowledgesSerializer(serializers.ModelSerializer):
    """Postulant additionalknowledge serializer"""

    additionalknowledge_text = serializers.ReadOnlyField(
        source="additionalknowledge.name")

    class Meta:
        model = UserAdditionalknowledge
        fields = ('additionalknowledge', 'additionalknowledge_text', 'description')


class PostulantLanguagesDetailSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(),

    language_text = serializers.ReadOnlyField(
        source="language.name")

    class Meta:
        model = UserLanguages
        fields = ('language_text', 'level', 'id')

class PostulantComputerknowledgesDetailSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(),

    computerknowledge_text = serializers.ReadOnlyField(
        source="computerknowledge.name")

    class Meta:
        model = UserComputerknowledge
        fields = ('computerknowledge_text', 'level', 'id')


class PostulantAdditionalknowledgesDetailSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField(),

    additionalknowledge_text = serializers.ReadOnlyField(
        source="additionalknowledge.name")

    class Meta:
        model = UserAdditionalknowledge
        fields = ('additionalknowledge_text', 'description', 'id')


# Rewriter here for a cross-dependencies issue
class JobsSimpleSerializer(serializers.ModelSerializer):

    owner = EmployerPublicInformation(read_only=True)
    area_text = serializers.CharField(source="area", read_only=True)

    class Meta:
        model = Job
        fields = ('id', 'title', 'owner', 'area_text', 'job_type_text')


class PostulationsListSerializer(serializers.ModelSerializer):
    """Postulation for postulant"""

    job = JobsSimpleSerializer(read_only=True)
    status_text = serializers.ReadOnlyField()

    class Meta:
        model = JobPostulation
        fields = (
            'id',
            'job',
            'status',
            'status_text')


class PostulantFullProfileSerializer(serializers.ModelSerializer):
    """Full CV profile serializer"""

    user = serializers.IntegerField(
        source="user.id",
        read_only=True)

    avatar = serializers.SerializerMethodField()

    biographic = serializers.CharField(
        read_only=True)

    experience = PublicProfecionalExperienceSerializer(
        many=True)

    roles = serializers.StringRelatedField(
        many=True,
        source="roles.roles")

    education = PostulantEducationSerializer(
        many=True)

    languages = PostulantLanguagesDetailSerializer(
        many=True)

    max_education = serializers.IntegerField()

    education_level = serializers.IntegerField()
    education_finish_level = serializers.IntegerField()

    gender_text = serializers.CharField(read_only=True)

    def get_avatar(self, obj):
        avatar = None
        try:
            avatar = obj.user.avatars.get(label="default")
        except obj.DoesNotExist:
            return None
        else:
            return avatar.url

    class Meta:
        model = Postulant
        fields = ('user', 'first_name', 'last_name', 'gender', 'phone_number',
                  'mobile_number', 'marital_status', 'country_of_birth',
                  'date_of_birth', 'driver_license', 'own_vehicle',
                  'has_disability', 'avatar', 'biographic', 'experience',
                  'roles', 'education', 'languages', 'max_education',
                  'education_level', 'education_finish_level', 'gender_text')


class CompletedItemsSerializer(ChoicesSerializer):
    """Completable items"""

    is_completed = serializers.BooleanField()


class CompletedProfileSerializer(serializers.Serializer):
    """Complete info serializer Info"""

    percent = serializers.IntegerField(
        read_only=True)

    items = CompletedItemsSerializer(
        read_only=True,
        many=True)


class CompleteProfileSerializer(PostulantSerializer):

    biographic = BiographicSerializer(
        read_only=True)

    experience = ProfessionalExperienceSerializer(
        read_only=True,
        many=True)

    education = PostulantEducationSerializer(
        read_only=True,
        many=True)

    languages = PostulantLanguagesSerializer(
        read_only=True,
        many=True)

    completed_info = CompletedProfileSerializer(
        read_only=True)

    roles = SlugedItemSerializer(
        source="roles.roles",
        read_only=True,
        many=True)

    class Meta:
        model = Postulant
        fields = [
            # profile
            'email',
            'first_name',
            'last_name',
            'gender',
            'phone_number',
            'mobile_number',
            'address',
            'city',
            'region',
            'country',
            # postulant
            'category',
            'marital_status',
            'dni',
            'date_of_birth',
            'country_of_birth',
            'postal_code',
            'driver_license',
            'own_vehicle',
            'has_disability',
            'completed',
            'last_update',
            # linked
            'biographic',
            'experience',
            'education',
            'languages',
            'roles',
            # generated
            'completed_info'
        ]


class CVRequestPostulantSerializer(serializers.ModelSerializer):
    """CVRequest for postulant"""
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault())

    def validate(self, data):
        """Check if employer want to receive cv request"""
        _employer = data.get('employer')
        if not _employer.cv_spontany:
            raise serializers.ValidationError('Employer not allow cv spontany')
        return data

    class Meta:
        model = CVRequest
        fields = ('employer', 'user')


class PostulantAttachCVListSerializer(serializers.ModelSerializer):

    user = serializers.PrimaryKeyRelatedField(read_only=True)
    name = serializers.CharField(read_only=True)
    attach = serializers.FileField(read_only=True)

    class Meta:
        model = PostulantAttachCV
        fields = ('user', 'name', 'attach')


class FavoriteSerializer(serializers.ModelSerializer):
    """Postulation for postulant"""

    job = JobsSimpleSerializer(read_only=True)

    class Meta:
        model = FavoriteJob
        fields = (
            'id',
            'job')