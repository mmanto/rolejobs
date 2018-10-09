# encoding=utf-8

from django import forms

from djng.forms import (
    NgModelFormMixin,
    NgFormValidationMixin,
    NgForm
)

from utils.adapter import NgErrorList


class ContactForm (
    NgFormValidationMixin,
    NgModelFormMixin,
    NgForm
):
    """Contact form"""

    form_name = 'contactForm'
    scope_prefix = 'contactData'

    name = forms.CharField(
        required=True,
        max_length=100)

    phone = forms.CharField(
        required=True,
        max_length=100)

    email = forms.EmailField(
        required=True)

    subject = forms.CharField(
        required=True,
        max_length=100)

    message = forms.CharField(
        required=True,
        widget=forms.Textarea())

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(ContactForm, self).__init__(*args, **kwargs)
