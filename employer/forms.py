# encoding=utf-8

from django.utils import six
from django import forms
from django.utils.translation import ugettext_lazy as _

from djng.forms import (
    NgDeclarativeFieldsMetaclass,
    NgModelFormMixin,
    NgFormValidationMixin,
    NgModelForm
)

from utils.adapter import NgErrorList
from accounts.models import GENDER_CHOICES, User

from models import (
    Employer,
    TYPE_REFERENCE,
    TYPE_COMPANY
)


class SignupForm(forms.Form):
    """Employer signup form"""

    first_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Nombre')}))

    last_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Apellido')}))

    email = forms.EmailField(
        required=True,
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Correo electrónico')}))

    password1 = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.PasswordInput(
                                   attrs={
                                       'placeholder': _(u'Contraseña')
                                    }))

    password2 = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.PasswordInput(
                            attrs={
                                'placeholder': _(u'Repetir contraseña')
                            }))

    name_company = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Nombre de la Empresa')}))

    razon_social = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Razon Social')}))

    responsability_iva = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Responsabilidad ante el IVA')}))

    country = forms.IntegerField(
         required=True)

    region = forms.IntegerField(
         required=True)

    city = forms.IntegerField(
        required=False)

    address = forms.CharField(
        required=True,
        max_length=100)

    sector_empresarial = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Sector empresarial')}))

    workforce = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': _('Numero de trabajadores')}))

    tipology = forms.ChoiceField(
        choices=TYPE_COMPANY, widget=forms.RadioSelect())

    description = forms.CharField(widget=forms.Textarea({'rows': 3}))

    website = forms.CharField(max_length=1024, required=True)

# @TODO Implementar logo
#    logo = forms.ImageField(required=False)

    cuit = forms.CharField(required=False, max_length=255)

    reference = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'selector'}), choices=TYPE_REFERENCE)

    newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'placeholder': _(u'Newsletter')}))

    terms_conditions = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                'placeholder': _(u'Terminos y Condiciones')}))

    cv_spontany = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'placeholder': _(u'CV espontaneo')}))

    position = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Cargo')}))

    gender = forms.ChoiceField(
        choices=GENDER_CHOICES, widget=forms.RadioSelect())

    phone_number = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Telefono')}))

    mobile_number = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Celular')}))

    def clean_terms_conditions(self):
        if not self.cleaned_data['terms_conditions']:
            raise forms.ValidationError("Debe aceptar los terminos y " +
                                        "condiciones")

    def clean_email(self):
        """Comprueba que no exista un email igual en la db"""
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError(u'Cuenta de correo ya registrada')
        return email

    def clean_password2(self):
        """Comprueba que password y password2 sean iguales."""
        password = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        if password != password2:
            raise forms.ValidationError(u'Las contraseñas no coinciden.')
        else:
            if len(password2) > 6:
                return password2
            else:
                raise forms.ValidationError(
                    'La contraseña debe tener mas de 6 caracteres')


class NgSignupForm(six.with_metaclass(
    NgDeclarativeFieldsMetaclass,
    NgFormValidationMixin,
    NgModelFormMixin,
    forms.Form
)):
    """Angular addapted verion of SignupForm"""

    form_name = 'employerSignupForm'
    scope_prefix = 'employerSignupData'

    first_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Nombre')}))

    last_name = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Apellido')}))

    email = forms.EmailField(
        required=True,
        max_length=250,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Correo electrónico')}))

    password1 = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.PasswordInput(
                                   attrs={
                                       'placeholder': _(u'Contraseña'),
                                       'ng-minlength': 6
                                    }))

    password2 = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.PasswordInput(
                            attrs={
                                'placeholder': _(u'Repetir contraseña'),
                                'ng-minlength': 6
                            }))

    name_company = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Nombre de la Empresa')}))

    razon_social = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Razon Social')}))

    responsability_iva = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Responsabilidad ante el IVA')}))

    sector_empresarial = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _('Sector empresarial')}))

    workforce = forms.IntegerField(
        required=True,
        widget=forms.NumberInput(
            attrs={
                'placeholder': _('Numero de trabajadores')}))

    tipology = forms.ChoiceField(required=True, widget=forms.Select(
        attrs={'class': 'selector'}), choices=TYPE_COMPANY)

    description = forms.CharField(widget=forms.Textarea({'rows': 3}))

    website = forms.CharField(max_length=1024, required=True)

# @TODO Implementar logo
#    logo = forms.ImageField(required=False)

    cuit = forms.CharField(required=False, max_length=255)

    reference = forms.ChoiceField(required=False, widget=forms.Select(
        attrs={'class': 'selector'}), choices=TYPE_REFERENCE)

    newsletter = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'placeholder': _(u'Newsletter')}))

    terms_conditions = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(
            attrs={
                'placeholder': _(u'Terminos y Condiciones')}))

    cv_spontany = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'placeholder': _(u'CV espontaneo')}))

    position = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Cargo')}))

    gender = forms.ChoiceField(required=True, widget=forms.Select(
        attrs={'class': 'selector'}), choices=GENDER_CHOICES)

    phone_number = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Telefono')}))

    mobile_number = forms.CharField(
        required=True,
        max_length=100,
        widget=forms.TextInput(
            attrs={
                'placeholder': _(u'Celular')}))

#    def __init__(self, *args, **kwargs):
#        super(NgSignupForm, self).__init__(*args, **kwargs)
    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(NgSignupForm, self).__init__(*args, **kwargs)


class EmployerDataForm (
    NgFormValidationMixin,
    NgModelFormMixin,
    NgModelForm
):
    """Employer data form"""

    form_name = 'employerForm'
    scope_prefix = 'employerData'

    first_name = forms.CharField(
        required=True,
        max_length=100)

    last_name = forms.CharField(
        required=True,
        max_length=100)

    def __init__(self, *args, **kwargs):
        kwargs.update(error_class=NgErrorList)
        super(EmployerDataForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Employer
        fields = [
            'gender',
            'phone_number',
            'mobile_number',
            'name_company',
            'razon_social',
            'responsability_iva',
            'address',
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
