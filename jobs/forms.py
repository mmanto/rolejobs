# encoding=utf-8

from __future__ import unicode_literals

from django import forms
from django.utils.translation import gettext as _

from djng.forms import (
    NgModelFormMixin,
    NgFormValidationMixin,
    NgModelForm,
    field_mixins,
)

from utils.adapter import NgErrorList
from utils.widgets import TextAngular
from education.choices import EDUCATION_GRADES

from jobs.models import (
    Job,
    JOB_STATUS_HAB,
    KnowledgeRequirement,
    JobPostulation,
    Question,
    QUESTION_TYPE_TEXT,
    QUESTION_TYPE_NUMBER,
    QUESTION_TYPE_CHOICES,
    QUESTIONS_TYPE_BOOLEAN,
    JOB_MODERATOR_STATUS_CHOICES,
)

YES_NO_CHOICES = (
    (True, _(u"Si")),
    (False, _(u"No")),
)


class NewJobForm (
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Add new job form"""

    form_name = 'jobForm'
    scope_prefix = 'jobData'

    description = forms.CharField(
        widget=TextAngular,
        required=True)

    subarea = forms.ChoiceField(
        choices=(),
        widget=forms.Select(
            attrs={
                'ng-options': 'sa as sa.name for sa in areaOptions.subareas ' +
                              'track by sa.pk'
            }
        ))

    education_requirement_grade = forms.ChoiceField(
        widget=forms.Select(),
        label=_(u"Grado de educación requerida"),
        required=False,
        choices=((-1, _(u"Seleccionar")),) + EDUCATION_GRADES)

    education_requirement_finished = forms.BooleanField(
        required=False,
        label=_("Terminado"))

    education_requirement_exclusive = forms.BooleanField(
        required=False,
        label=_(u"Es excluyente"))

    publish_now = forms.BooleanField(
        required=False,
        label=_(u"Publicar inmediatamente si es posible"))

    publish_date = forms.CharField(
        label=_(u"Fecha de publicación"),
        widget=forms.TextInput(
            attrs={
                'datetimepicker': ""
            }
        ))

    contract_date = forms.CharField(
        label=_(u"Fecha de publicación"),
        widget=forms.TextInput(
            attrs={
                'datetimepicker': ""
            }
        ))  

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NewJobForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Job
        fields = [
            'title',
            'reference_number',
            'description',
            'handicapped_postulant',
            'show_address',
            'get_cvs_ctrl_panel',
            'send_cvs_by_mail',
            'send_gratitude_by_mail',
            'area',
            'subarea',
            'role',
            'position',
            'hierarchy',
            'branch_activity',
            'job_type',
            'contract_date',
            'vacancies',
            'video',
            'publish_date',
            'confidential',
            'residence_range',
            'residence_range_exclusive',
            'requirement_gender',
            'requirement_age_min',
            'requirement_age_max',
            'requirement_driver_license',
            'similar'
        ]


class KnowledgeRequirementForm (
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Add new Knowledge requirement form"""

    form_name = 'requirementForm'
    scope_prefix = 'requirementData'

    subtechnology = forms.ChoiceField(
        choices=(),
        required=True,
        widget=forms.Select(
            attrs={
                'ng-options': 's as s.name for s in tech.subtechnologies ' +
                              'track by s.id'
            }
        ))

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(KnowledgeRequirementForm, self).__init__(*args, **kwargs)

    class Meta:
        model = KnowledgeRequirement
        exclude = ('job', )


class QuestionForm (
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Add new question form"""

    form_name = 'questionForm'
    scope_prefix = 'questionData'

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(QuestionForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Question
        exclude = ('job', 'created_at', 'updated_at')


class ModerationForm(forms.Form):

    status = forms.ChoiceField(
        choices=JOB_MODERATOR_STATUS_CHOICES)

    reason = forms.CharField(
        required=False,
        widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('job')
        return super(ModerationForm, self).__init__(*args, **kwargs)

    def clean_status(self):
        status = int(self.cleaned_data['status'])

        if status == JOB_STATUS_HAB:
            return status

        if self.instance.status == status:
            raise forms.ValidationError(
                 _(u"No se puede definir el mismo estado"))

        return status

    def clean_reason(self):
        reason = self.cleaned_data['reason']

        if not reason:
            return None
        else:
            return reason

    def save(self, user):
        self.instance.moderate(
            user,
            self.cleaned_data['status'],
            self.cleaned_data['reason']
        )


class JobQuestionsForm(
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Dynamic form"""

    form_name = 'postulateForm'
    scope_prefix = 'postulateData'

    def __init__(self, job, *args, **kwargs):
        self.job = job
        kwargs.update(error_class=NgErrorList)

        questions = job.questions.all()

        super(JobQuestionsForm, self).__init__(*args, **kwargs)

        self.fields['message'].widget = forms.Textarea()

        for question in questions:
            self.add_question(question)

        for field in self.fields.values():
            FieldMixinName = field.__class__.__name__ + 'Mixin'
            FieldMixin = getattr(field_mixins, FieldMixinName)

            field.__class__ = type(field.__class__.__name__,
                                   (field.__class__, FieldMixin), {})

    def add_question(self, question):
        field = None
        type = question.question_type

        if type == QUESTION_TYPE_TEXT:
            field = forms.CharField(
                label=question.question,
                required=question.is_required)

        elif type == QUESTION_TYPE_NUMBER:
            field = forms.IntegerField(
                label=question.question,
                required=question.is_required)

        elif type == QUESTIONS_TYPE_BOOLEAN:
            field = forms.ChoiceField(
                label=question.question,
                choices=YES_NO_CHOICES)

        elif type == QUESTION_TYPE_CHOICES:
            choices = [(o.id, o.text) for o in question.options.all()]

            field = forms.ChoiceField(
                label=question.question,
                required=question.is_required,
                widget=forms.RadioSelect,
                choices=choices)

        else:
            raise Exception("Question type unknow")

        field_name = 'question_%i' % question.id

        ng_model = self.add_prefix(field_name)
        field.widget.attrs.setdefault('ng-model', ng_model)

        self.fields[field_name] = field

    class Meta:
        model = JobPostulation
        fields = ('request_salary', 'message')
