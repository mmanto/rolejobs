# encoding=utf-8

from django.conf.urls import url
from views import ContactView, ContactFormView

urlpatterns = [
    url(
        r"^form.html$",
        ContactFormView.as_view()
    ),
    url(
        r"^$",
        ContactView.as_view()
    ),
]
