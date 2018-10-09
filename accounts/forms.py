# -*- coding: utf8 -*-

from __future__ import unicode_literals

from django import forms
from django.utils import six

from django.contrib.auth.forms import (
    UserCreationForm as BaseUserCreationForm,
    UserChangeForm as BaseUserChangeForm,
    PasswordResetForm as BasePasswordResetForm,
)

from django.contrib.auth import password_validation

from django.utils.translation import ugettext_lazy as _

from djng.forms import (
    NgDeclarativeFieldsMetaclass,
    NgModelFormMixin,
    NgFormValidationMixin
)

from utils.adapter import NgErrorList

from accounts.models import User


class UserCreationForm(BaseUserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(UserCreationForm, self).__init__(*args, **kargs)
        # del self.fields['username']

    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(BaseUserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(UserChangeForm, self).__init__(*args, **kargs)
        # del self.fields['username']

    class Meta:
        model = User
        fields = ("email",)


class PasswordResetForm(BasePasswordResetForm):

    def save(self, *args, **kwargs):
        email = self.data['email']

        try:
            user = User.objects.get(email=email)
        except:
            return

        user.send_reset_password_email()


class NgChangePasswordForm(six.with_metaclass(
    NgDeclarativeFieldsMetaclass,
    NgFormValidationMixin,
    NgModelFormMixin,
    forms.Form
)):
    """Angular addapted change password form"""

    form_name = 'changePasswordForm'
    scope_prefix = 'changePasswordData'

    old_password = forms.CharField(
        label=_("Old password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password1 = forms.CharField(
        label=_("New password"),
        widget=forms.PasswordInput,
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )

    new_password2 = forms.CharField(
        label=_("New password confirmation"),
        strip=False,
        widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NgChangePasswordForm, self).__init__(*args, **kwargs)
