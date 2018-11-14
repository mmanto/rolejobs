# -*- coding: utf-8 -*-

from django.conf.urls import url, include
from . import views


urlpatterns = [


    url(r"^$", views.LoginViewset.as_view({"get": "retrieve"})),
    url(r"^auth", include("rest_auth.urls")),
    url(r"^verifyresetpasswordemail/$", views.verify_reset_pass_email),
    url(r"^confirm$", views.validate_account, name="account_confirm"),
    url(r"^postulationauthcheck$", views.postulation_auth_check),
    # forms
    url(
        r"^templates/change_password.html$",
        views.ChangePasswordFormView.as_view()
    )
]
