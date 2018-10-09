# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views


urlpatterns = [
    url(r"^$", views.LoginViewset.as_view({"get": "retrieve"})),
    url(r"^auth", include("rest_auth.urls")),
    url(r"^confirm$", views.validate_account, name="account_confirm"),
    # forms
    url(
        r"^templates/change_password.html$",
        views.ChangePasswordFormView.as_view()
    )
]
