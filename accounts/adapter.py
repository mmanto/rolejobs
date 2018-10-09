# -*- coding: utf8 -*-
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.account.adapter import DefaultAccountAdapter
from allauth.account.utils import user_email, user_field, user_username
from allauth.utils import valid_email_or_none


class AccountAdapter(DefaultAccountAdapter):

    def send_confirmation_mail(self, request, emailconfirmation, signup):
        emailconfirmation.email_address.user.send_validation_email()


class SocialAccountAdapter(DefaultSocialAccountAdapter):

    def populate_user(self, request, sociallogin, data):
        sociallogin.user.type_profile = 'postulant'

        # original code from lib
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        name = data.get('name')
        user = sociallogin.user
        user_username(user, username or '')
        user_email(user, valid_email_or_none(email) or '')
        name_parts = (name or '').partition(' ')
        user_field(user, 'first_name', first_name or name_parts[0])
        user_field(user, 'last_name', last_name or name_parts[2])
        return user
