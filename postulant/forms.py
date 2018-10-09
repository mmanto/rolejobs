# encoding=utf-8

from django import forms
from django.db.utils import OperationalError, ProgrammingError
# from django.utils.translation import ugettext_lazy as _

from djng.forms import (
    NgModelFormMixin,
    NgFormValidationMixin,
    NgModelForm
)

from utils.widgets import FoundationRating
from accounts.models import GENDER_CHOICES
from utils.adapter import NgErrorList
from education.models import (
    UserEducation,
    Language,
    UserLanguages,
    UserCertification
)

from models import (
    Postulant,
    ProfessionalExperience,
    ProfessionalReference,
    YES_NO_CHOICES
)


def get_lenguages():
    choices = []
    try:
        choices = [(l.id, l.name) for l in Language.objects.all()]
    except OperationalError:
        return []
    except ProgrammingError:
        return []
    except Exception, e:
        raise e
    else:
        return choices


class PostulantCvForm (
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Postulant data form"""

    form_name = 'postulantForm'
    scope_prefix = 'postulantData'

    first_name = forms.CharField(
        required=True,
        max_length=100)

    last_name = forms.CharField(
        required=True,
        max_length=100)

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        widget=forms.RadioSelect(),
        label="Sexo")

    own_vehicle = forms.ChoiceField(
        choices=YES_NO_CHOICES,
        widget=forms.RadioSelect(),
        label="¿Posée vehículo propio?")

    date_of_birth = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'datetimepicker': ""
            }
        ))

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(PostulantCvForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Postulant
        fields = [
            # profile
            'gender',
            'phone_number',
            'mobile_number',
            # postulant
            'category',
            'marital_status',
            'dni',
            'date_of_birth',
            'country_of_birth',
            'postal_code',
            'driver_license',
            'own_vehicle',
            'has_disability'
        ]


class NewProfieccionalExperienceForm(
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Form for add new professional experience"""

    form_name = 'peForm'
    scope_prefix = 'peData'

    subarea = forms.ChoiceField(
        choices=(),
        widget=forms.Select(
            attrs={
                'ng-options': 'sa as sa.name for sa in peOptions.subareas ' +
                              'track by sa.pk'
            }
        ))

    start_date = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'datetimepicker': ""                
            }
        ))

    end_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'datetimepicker': ""                
            }
        ))

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NewProfieccionalExperienceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProfessionalExperience
        exclude = ('created', 'updated_at', 'postulant')


class ExperienceReferenceForm(
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Add reference on PE form"""

    form_name = 'referenceForm'
    scope_prefix = 'referenceData'

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(ExperienceReferenceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = ProfessionalReference
        exclude = (
            'created_at', 'updated_at', 'created_by',
            'experience', 'confirmed')


class NewEducationForm(
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Form for add new education"""

    form_name = 'educationForm'
    scope_prefix = 'educationData'

    institution_id = forms.IntegerField(
        widget=forms.HiddenInput())

    institution = forms.CharField(
        widget=forms.TextInput(attrs={
            "autocomplete": "off",
            "typeahead": 'i.name for i in searchInstitution($viewValue)'
        }))

    start_date = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'datetimepicker': ""
            }
        ))

    end_date = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'datetimepicker': ""
            }
        ))

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NewEducationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserEducation
        exclude = ('created_at', 'updated_at', 'user')


class NewLanguageForm(
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Form for add new language"""

    form_name = 'languageForm'
    scope_prefix = 'languageData'

    language = forms.ChoiceField(
        choices=get_lenguages(),
        widget=forms.Select(
            attrs={
                'ng-readonly': "blockLang"
            }
        ))

    level = forms.IntegerField(
        min_value=0,
        max_value=10,
        widget=FoundationRating(
            attrs={
                "max": 10
            }
        ))

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NewLanguageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserLanguages
        exclude = ('user',)


class NewCertificationForm(
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Form for add new certification"""

    form_name = 'certificationForm'
    scope_prefix = 'certificationData'

    description = forms.CharField(
        widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NewCertificationForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserCertification
        exclude = ('education',)
