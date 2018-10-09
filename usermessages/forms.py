# encoding=utf-8

from __future__ import unicode_literals

from django import forms

from djng.forms import (
    NgModelFormMixin,
    NgFormValidationMixin,
    NgModelForm,
)

from utils.adapter import NgErrorList
from utils.widgets import TextAngular

from models import UserMessage


class NewUserMessageForm (
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Add new message form"""

    form_name = 'messageForm'
    scope_prefix = 'messageData'

    message = forms.CharField(
        widget=TextAngular,
        required=True)

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NewUserMessageForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserMessage
        fields = [
            'message',
        ]
