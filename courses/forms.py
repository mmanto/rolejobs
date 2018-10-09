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

from models import Course
from constants import COURSES_TYPE_CHOICES, CURRENCY_TYPE_CHOICES


YES_NO_CHOICES = (
    (True, _(u"Si")),
    (False, _(u"No")),
)


class NewCourseForm (
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Add new course form"""

    form_name = 'courseForm'
    scope_prefix = 'courseData'

    course_type = forms.ChoiceField(
        widget=forms.Select(),
        label=_(u"Tipo de curso"),
        required=True,
        choices=COURSES_TYPE_CHOICES
    )

    description = forms.CharField(
        widget=TextAngular,
        required=True)

    currency_type = forms.ChoiceField(
        widget=forms.Select(),
        label=_(u"Moneda"),
        required=True,
        choices=CURRENCY_TYPE_CHOICES
    )

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NewCourseForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'price',
            'currency_type',
            'course_type',
            'company_data_from_owner',
            '_company',
            '_company_logo',
            'notify_by_email',
        ]
