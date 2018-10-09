# encoding=utf-8

from django.conf.urls import url
from views import (
    ProfileAvatarView
)

urlpatterns = [
    url(
        r"^profile/?$",
        ProfileAvatarView.as_view()
    ),
    url(
        r"^profile/(?P<label>[a-zA-Z]+)/?$",
        ProfileAvatarView.as_view()
    ),
]
