# encoding=utf-8

from __future__ import unicode_literals
import re

from django.utils.translation import gettext as _
from django.core.exceptions import ObjectDoesNotExist

from rest_framework import serializers

from accounts.models import User
from accounts.serializers import PublicUserSerializer
from employer.serializers import EmployerPublicInformation

from postulant.serializers import PostulantFullProfileSerializer

from utils.serializers import (
    PkListField,
    SubModelSerializer,
    ModelWithSubModelsSerializer,
    ChoicesSerializer,
)

from geo.serializers import GeoDataSerializer

from models import (
    Job,
    Requirement,
    LanguageRequirement,
    EducationRequirement,
    KnowledgeRequirement,
    Area,
    SubArea,
    Technology,
    SubTechnology,
    Role,
    Question,
    QuestionOption,
    JobPostulation,
    QuestionAnswer,
    JOB_STATUS_HAB,
    JOB_STATUS_PENDING,
    InsufficientPostPointsException,
    POSTULATION_ACCEPTED,
    POSTULATION_REJECTED,
)


class RequirementSerializer(SubModelSerializer):
    """Job Requirement serializer"""

    class Meta:
        model = Requirement
        exclude = ('job', )


class LanguageRequirementSerializer(SubModelSerializer):
    """Language requirement serialier"""

    name = serializers.ReadOnlyField()

    class Meta:
        model = LanguageRequirement
        exclude = ('job', )


class EducationRequirementSerializer(SubModelSerializer):
    """Education requirement serializer"""

    level_text = serializers.ReadOnlyField()

    class Meta:
        model = EducationRequirement
        exclude = ('job', )


class KnowledgeRequirementSerializer(SubModelSerializer):
    """Knowleged requirement serializer"""

    technology_text = serializers.ReadOnlyField(source="technology.name")
    subtechnology_text = serializers.ReadOnlyField(source="subtechnology.name")
    hierarchy_text = serializers.ReadOnlyField(source="hierarchy.name")

    class Meta:
        model = KnowledgeRequirement
        exclude = ('job', )


class AreaSerializer(serializers.ModelSerializer):
    """Area model serializer"""

    class Meta:
        model = Area


class SubAreaSerializer(serializers.ModelSerializer):
    """SubArea serializer"""

    class Meta:
        model = SubArea
        fields = ['pk', 'name', 'description', 'slug']


class DetailedAreaSerializer(serializers.ModelSerializer):
    """Detailed Area serializer"""

    subareas = SubAreaSerializer(many=True, read_only=True)

    class Meta:
        model = Area


class JobsSimpleSerializer(serializers.ModelSerializer):
    """Jobs serializer for simple requests"""

    class Meta:
        model = Job
        fields = ('pk', 'title')


class JobListSerializer(serializers.ModelSerializer):
    """Job on list"""

    pk = serializers.ReadOnlyField()
    owner = serializers.SerializerMethodField()
    role_text = serializers.CharField(source="role", read_only=True)
    area_text = serializers.CharField(source="area", read_only=True)
    subarea_text = serializers.CharField(source="subarea", read_only=True)
    job_type_text = serializers.ReadOnlyField()
    roles = PkListField(read_only=False)
    geo = GeoDataSerializer(read_only=True, source="geodata")

    def get_owner(self, obj):
        if obj.confidential:
            return {}
        employer = EmployerPublicInformation(obj.owner, read_only=True)
        return employer.data

    class Meta:
        model = Job
        fields = ("pk", "title", "published", "owner", "featured", "role",
                  "role_text", "area", "subarea", "area_text", "subarea_text",
                  "job_type", "job_type_text", "roles", "geo",
                  "residence_range", "contract_date", "video")


class JobSerializer(serializers.ModelSerializer):
    """Jobs serializer"""

    pk = serializers.ReadOnlyField()

    owner = serializers.SerializerMethodField()

    role_text = serializers.CharField(
        source="role",
        read_only=True)

    position_text = serializers.CharField(
        source="position",
        read_only=True)

    hierarchy_text = serializers.CharField(
        source="hierarchy",
        read_only=True)

    branch_activity_text = serializers.CharField(
        source="branch_activity",
        read_only=True)

    requirements = RequirementSerializer(
        read_only=True,
        many=True)

    area = AreaSerializer(
        read_only=True,
        many=False)

    subarea = SubAreaSerializer(
        read_only=True,
        many=False)

    language_requirements = LanguageRequirementSerializer(
        read_only=True,
        many=True)

    education_requirement = EducationRequirementSerializer(
        read_only=True, many=False)

    knowledge_requirements = KnowledgeRequirementSerializer(
        read_only=True, many=True)

    job_type_text = serializers.ReadOnlyField()

    postulation_status = serializers.SerializerMethodField(
        read_only=True)

    geo = GeoDataSerializer(
        read_only=True,
        source="geodata")

    requirement_gender_text = serializers.CharField(
        source="requirenment_gender",
        read_only=True)

    def get_owner(self, obj):
        if obj.confidential:
            return {}
        employer = EmployerPublicInformation(obj.owner, read_only=True)
        return employer.data

    def get_postulation_status(self, obj):
        request = self.context.get('request', None)
        postulation = None

        if request:
            user = request.user
            if user:
                try:
                    postulation = obj.get_user_postulation(user)
                except JobPostulation.DoesNotExist, e:
                    return None
                except Exception, e:
                    raise e
                else:
                    return postulation.status
            else:
                return None
        else:
            return None

    class Meta:
        model = Job
        fields = ("pk", "title", "published", "owner", "featured", "role",
                  "role_text", "area", "subarea", "job_type", "job_type_text",
                  "roles", "geo", "position", "position_text", "hierarchy",
                  "hierarchy_text", "requirements", "language_requirements",
                  "education_requirement", "knowledge_requirements",
                  "postulation_status", "branch_activity",
                  "branch_activity_text", "residence_range", "contract_date",
                  "video", "requirement_gender_text", "requirement_age_min",
                  "requirement_age_max", "requirement_driver_license")


class OwnQuestionOptionSerializer(SubModelSerializer):
    """Option serializer"""

    class Meta:
        model = QuestionOption
        exclude = ('question', )


class OwnQuestionSerializer(SubModelSerializer):
    """Question serializer"""

    type_text = serializers.ReadOnlyField()
    options = OwnQuestionOptionSerializer(
        read_only=False,
        required=False,
        many=True,
        pass_id=True)

    class Meta:
        model = Question
        exclude = ('job', 'created_at', 'updated_at')


class OwnJobSerializer(ModelWithSubModelsSerializer):
    """Own job serializer"""

    pk = serializers.ReadOnlyField()
    url = serializers.CharField(source='get_url', read_only=True)
    area_text = serializers.CharField(source="area", read_only=True)
    subarea_text = serializers.CharField(source="subarea", read_only=True)
    status_text = serializers.ReadOnlyField()

    position_text = serializers.CharField(
        source="position",
        read_only=True)

    hierarchy_text = serializers.CharField(
        source="hierarchy",
        read_only=True)

    branch_activity_text = serializers.CharField(
        source="branch_activity",
        read_only=True)

    job_type_text = serializers.ReadOnlyField()

    publish_now = serializers.BooleanField(
        write_only=True,
        default=False)

    requirements = RequirementSerializer(
        many=True,
        read_only=False,
        pass_id=True)

    language_requirements = LanguageRequirementSerializer(
        read_only=False,
        many=True,
        pass_id=True)

    education_requirement = EducationRequirementSerializer(
        read_only=False,
        many=False,
        required=False)

    knowledge_requirements = KnowledgeRequirementSerializer(
        read_only=False,
        many=True,
        pass_id=True)

    roles = PkListField(
        read_only=False)

    questions = OwnQuestionSerializer(
        read_only=False,
        many=True,
        pass_id=True)

    postulants_number = serializers.IntegerField(
        read_only=True)

    geo = GeoDataSerializer(
        read_only=True,
        source="geodata_original")

    def update_sub_element(self, instance, data, model):
        data.update({
            "job": instance
        })
        return data

    def create_language_requirements(self, instance, languages):
        return self.create_parts(instance, LanguageRequirement, languages)

    def create_knowledge_requirements(self, instance, knowledges):
        return self.create_parts(instance, KnowledgeRequirement, knowledges)

    def create_requirements(self, instance, requirements):
        return self.create_parts(instance, Requirement, requirements)

    def create_options(self, question, options):
        options_models = [QuestionOption(question=question, **op_data)
                          for op_data in options]
        return QuestionOption.objects.bulk_create(options_models)

    def create_questions(self, instance, questions):

        for data in questions:
            options_list = data.pop("options", None)
            q = Question.objects.create(job=instance, **data)
            q.save()

            try:
                self.create_options(q, options_list)
            except Exception, e:
                q.delete()
                raise e

    def save_education_requirement(self, instance, education_requirement):
        try:
            er = instance.education_requirement
        except ObjectDoesNotExist:

            if education_requirement is None:
                return

            er = EducationRequirement.objects.create(
                job=instance, **education_requirement)

            return er.save()

        except Exception, e:
            raise e
        else:

            if education_requirement is None:
                return er.delete()

            er.exclusive = education_requirement.get('exclusive', False)
            er.level = education_requirement.get('level')
            er.finished = education_requirement.get('finished')
            return er.save()

    def update_requirements(self, instance, requirements):
        self.save_parts(instance, "requirements", Requirement, requirements)

    def update_language_requirements(self, instance, requirements):
        return self.save_parts(
            instance,
            "language_requirements",
            LanguageRequirement,
            requirements)

    def update_knowledge_requirements(self, instance, requirements):
        return self.save_parts(
            instance,
            "knowledge_requirements",
            KnowledgeRequirement,
            requirements)

    def update_question(self, question, data):
        options = data.pop('options')

        # Save question
        question.is_required = data.get(
            "is_required", question.is_required)
        question.question_type = data.get(
            "question_type", question.question_type)
        question.question = data.get(
            "question", question.question)
        question.save()

        new_items = [i for i in options
                     if i.get("id", None) is None]

        to_update = {str(i["id"]): i for i in options
                     if i.get("id", None) is not None}

        actuals = {str(i.id): i for i in question.options.all()}

        # Save options
        self.create_options(question, new_items)

        for id, actual in actuals.items():
            if str(id) in to_update:
                data = to_update.get(str(id))
                actual.text = data.get("text", actual.text)
                actual.is_correct = data.get("is_correct", actual.is_correct)
                actual.save()
            else:
                actual.delete()

    def update_questions(self, instance, questions):
        new_questions = (q for q in questions
                         if q.get("id", None) is None)

        to_update = {str(q["id"]): q for q in questions
                     if q.get("id", None) is not None}

        actuals = {str(q.id): q for q in instance.questions.all()}

        self.create_questions(instance, new_questions)

        for id, actual in actuals.items():
            if str(id) in to_update:
                self.update_question(actual, to_update.get(str(id)))
            else:
                actual.delete()

    def set_roles(self, instance, roles_pks):
        roles = [Role.objects.get(id=int(id)) for id in roles_pks]
        instance.roles.set(roles)
        return roles

    def send_moderator_emails(self, instance):

        moderators = User.objects.moderators.all()

        for mod in moderators:
            mod.send_moderation_email(instance)

    def create(self, validated_data):
        requirements = validated_data.pop('requirements')
        language_requirements = validated_data.pop('language_requirements')
        education_requirement = validated_data.pop('education_requirement',
                                                   None)
        knowledge_requirements = validated_data.pop('knowledge_requirements')
        roles_pks = validated_data.pop('roles')
        questions = validated_data.pop('questions')
        publish_now = validated_data.pop("publish_now", False)

        instance = super(OwnJobSerializer, self).create(validated_data)

        try:
            self.create_requirements(instance, requirements)
            self.create_language_requirements(instance, language_requirements)
            self.save_education_requirement(instance, education_requirement)
            self.create_knowledge_requirements(instance,
                                               knowledge_requirements)
            self.set_roles(instance, roles_pks)
            self.create_questions(instance, questions)
        except Exception, e:
            instance.delete()
            raise e

        if publish_now:
            try:
                instance.publish()
            except InsufficientPostPointsException:
                pass
            except Exception, e:
                raise e

        if instance.status in (JOB_STATUS_HAB, JOB_STATUS_PENDING):
            self.send_moderator_emails(instance)

        return instance

    def update(self, instance, validated_data):
        requirements = validated_data.pop('requirements')
        language_requirements = validated_data.pop('language_requirements')
        education_requirement = validated_data.pop('education_requirement',
                                                   None)
        knowledge_requirements = validated_data.pop('knowledge_requirements')
        roles_pks = validated_data.pop('roles')
        questions = validated_data.pop('questions')
        publish_now = validated_data.pop("publish_now", False)

        validated_data.update({
            "moderated": False
        })

        instance = super(OwnJobSerializer, self).update(
            instance, validated_data)

        if publish_now:
            instance.moderation_object.moderate(
                None,
                JOB_STATUS_PENDING,
                u"Petición de aprobación")

        self.update_requirements(instance, requirements)
        self.update_language_requirements(instance, language_requirements)
        self.save_education_requirement(instance, education_requirement)
        self.update_knowledge_requirements(instance, knowledge_requirements)
        self.set_roles(instance, roles_pks)
        self.update_questions(instance, questions)

        if instance.status in (JOB_STATUS_HAB, JOB_STATUS_PENDING):
            self.send_moderator_emails(instance)

        return instance

    class Meta:
        model = Job
        exclude = ('id', 'owner', 'created', 'updated')
        read_only_fields = ('created', 'updated', 'featured', 'status')


class SubTechnologySerializer(serializers.ModelSerializer):
    """Technology model serializer"""

    class Meta:
        model = SubTechnology
        exclude = ('technology', )


class TechnologySerializer(serializers.ModelSerializer):
    """Technology model serializer"""

    subtechnologies = SubTechnologySerializer(
        read_only=True,
        many=True)

    class Meta:
        model = Technology


class AnswerSerializer(serializers.ModelSerializer):
    """Answer serializer"""

    question_id = serializers.ReadOnlyField(
        source="question.id")

    question = serializers.CharField(source="question.question")
    type = serializers.IntegerField(source="question.question_type")
    response = serializers.SerializerMethodField()

    def get_response(self, obj):
        response = obj.response
        if isinstance(response, QuestionOption):
            response = response.text
        return response

    class Meta:
        model = QuestionAnswer
        fields = ("id", "question", "type", "response", "question_id")


class JobPostulationSerializer(serializers.ModelSerializer):
    """Job postulation request serializer"""

    id = serializers.ReadOnlyField()

    questionsanswers = AnswerSerializer(
        many=True,
        read_only=True)

    answers = serializers.JSONField(
        write_only=True)

    status_text = serializers.ReadOnlyField()

    def save_answers(self, instance, answers):
        actuals = instance.job.questions.all()
        requireds = actuals.filter(is_required=True)

        for key in answers.keys():
            if not re.match("^question_[0-9]+$", key):
                raise Exception("Invalid key")

        send_ids = [int(p.split("_")[1]) for p in answers.keys()]
        actuals_ids = [r.id for r in actuals]
        required_ids = [r.id for r in requireds]

        # Check if all answers are for valid questions
        for id in send_ids:
            if id not in actuals_ids:
                raise Exception("Unknow question")

        # Check if required questions are answered
        for id in required_ids:
            if id not in send_ids:
                raise Exception("Required question not present")
            if answers.get('question_%s' % id) is None:
                raise Exception("Invalid content for required question")

        questions = {q.id: q for q in actuals}

        # Create models
        models = [QuestionAnswer(
            postulation=instance,
            question=questions.get(id)) for id in send_ids]

        # Set responses
        for answer in models:
            answer.set_response(
                answers.get("question_%s" % answer.question.id))

        return QuestionAnswer.objects.bulk_create(models)

    def create(self, validated_data):
        answers = validated_data.pop("answers")
        instance = super(JobPostulationSerializer, self).create(validated_data)

        try:
            self.save_answers(instance, answers)
        except Exception, e:
            instance.delete()
            raise e

        # # Dont exist this field or method in job model
        # if instance.job.send_postulation_gratitude_notification:
        #     request = self.context.get('request', None)
        #     request.user.send_postulation_gratitude_notification(instance)

        return instance

    def update(self, instance, validated_data):
        raise Exception("Invalid action")

    class Meta:
        model = JobPostulation
        fields = (
            'id',
            'request_salary',
            'status',
            'status_text',
            'message',
            'questionsanswers',
            'answers')


class OwnJobPostulationListSerializer(serializers.ModelSerializer):

    user = PublicUserSerializer(
        read_only=True)

    class Meta:
        model = JobPostulation
        fields = (
            'id',
            'user',
            'request_salary',
            'status',
            'status_text',
            'message',
            'favorite'
        )


class OwnJobPostulationDetailledSerializer(serializers.ModelSerializer):

    id = serializers.ReadOnlyField()

    user = PostulantFullProfileSerializer(
        read_only=True,
        source="user.profile")

    questionsanswers = AnswerSerializer(
        many=True,
        read_only=True)

    answers = serializers.JSONField(
        write_only=True)

    class Meta:
        model = JobPostulation
        fields = (
            'id',
            'user',
            'request_salary',
            'status',
            'status_text',
            'message',
            'questionsanswers',
            'answers')


class PostulantPostulationDetailSerializer(JobPostulationSerializer):

    job = JobsSimpleSerializer(read_only=True)

    class Meta:
        model = JobPostulation
        fields = (
            'job',
            'request_salary',
            'status',
            'status_text',
            'message',
            'questionsanswers',
            'answers')


class PostulationStatusSerializer(serializers.Serializer):
    """Postulation status serializer"""

    status = serializers.ChoiceField(
        required=True,
        allow_null=False,
        choices=(
            (POSTULATION_ACCEPTED, _(u"Aceptada")),
            (POSTULATION_REJECTED, _(u"Rechazada")),
        ))


class PostulationFavoriteSerializer(serializers.Serializer):
    """Postulation favorite serializer"""

    favorite = serializers.BooleanField(required=True)


class OwnJobsInfoSerializer(serializers.Serializer):

    total_postulants = serializers.IntegerField()

    aviable_status = ChoicesSerializer(
        read_only=True,
        many=True)
