# encoding=utf-8

from django.conf.urls import url

from views import UserMessageView, NewUserMessageFormView

urlpatterns = [
    url(
        r"^$",
        UserMessageView.as_view({
            'get': 'list',
        })
    ),
    url(
        r"^\?$",
        UserMessageView.as_view({
            'get': 'list',
        })
    ),
    url(
        r"^by_postulation/(?P<postulation_pk>[0-9]+)$",
        UserMessageView.as_view({
            'get': 'list_by_postulation',
            'post': 'create_by_postulation'
        })
    ),
    url(
        r"^by_cvrequest/(?P<cvrequest_pk>[0-9]+)$",
        UserMessageView.as_view({
            'get': 'list_by_cvrequest',
            'post': 'create_by_cvrequest'
        })
    ),
    url(
        r"^(?P<message_pk>[0-9]+)/$",
        UserMessageView.as_view({
            'get': 'retrieve',
            'post': 'create',
        }),
        name='usermessage-retrieve'
    ),
    url(
        r"^(?P<message_pk>[0-9]+)/read$",
        UserMessageView.as_view({
            'post': 'read',
        })
    ),
    url(
        r"^templates/new_message.html$",
        NewUserMessageFormView.as_view()
    ),
]
