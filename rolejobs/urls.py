# -*- coding: utf-8 -*-

from django.conf import settings
from django.conf.urls import url, include
from django.views.generic import TemplateView, RedirectView
from django.contrib import admin

urlpatterns = [

    url(r"^accounts/reset_password$(?P<id>[\d]+)/(?P<hash>[0-9a-f]+)",
        RedirectView.as_view(url="/#/accounts/reset_password", permanent=True),
        name="password_reset_confirm"),

    url(r'^accounts/', include('allauth.urls')),

    # ADMIN
    url(r'^admin/', admin.site.urls),

    # API
    url(r"^api/v1/", include("rolejobs_api.urls")),

    # Terms and conditions
    url(
        r"^templates/terms_conditions.html",
        TemplateView.as_view(template_name="home/terms_conditions.html"),
    ),

    # Privacy
    url(
        r"^templates/privacy.html",
        TemplateView.as_view(template_name="home/privacy.html"),
    ),

    url(
        r"^media/(?P<path>.*)$",
        'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
            'show_indexes': False
        }
    ),

    # All
    url(r'^.*$', TemplateView.as_view(template_name="base.html"), name="home"),
]
