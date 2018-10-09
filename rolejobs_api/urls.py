# -*- coding: utf-8 -*-

from django.conf.urls import url, include

urlpatterns = [
    url(r"^docs/", include('rest_framework_swagger.urls')),
    url(r"^accounts/", include("accounts.urls")),
    url(r"^postulant/", include("postulant.urls")),
    url(r"^employer/", include("employer.urls")),
    url(r"^localidades/", include("localidades.urls")),
    url(r"^jobs/", include("jobs.urls")),
    url(r"^education/", include("education.urls")),
    url(r"^contact/", include("contact.urls")),
    url(r"^avatars/", include("avatars.urls")),
    url(r"^messages/", include("usermessages.urls")),
    url(r"^courses/", include("courses.urls")),
    url(r"^geo/", include("geo.urls")),
]
