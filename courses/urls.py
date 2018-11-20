# encoding: utf-8

from django.conf.urls import url

from views import (
    CourseEmployerView, CoursePostulationEmployerView,
    CoursePostulationPostulantView, CourseView, NewCourseFormView
)

urlpatterns = [
    url(
        r"^$",
        CourseView.as_view({
            'get': 'list',
        })
    ),
    url(
        r"^courses/?$",
        CourseView.as_view({
            'get': 'list',
        })
    ),
    url(
        r"^courses/(?P<pk>[0-9]+)$",
        CourseView.as_view({
            'get': 'retrieve',
        })
    ),
    url(
        r"^(?P<pk>[0-9]+)/join$",
        CoursePostulationPostulantView.as_view({
            'post': 'create',
        })
    ),
    url(
        r"^own$",
        CourseEmployerView.as_view({
            'get': 'list',
            'post': 'create',
        })
    ),
    url(
        r"^own/(?P<pk>[0-9]+)$",
        CourseEmployerView.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'destroy',
        })
    ),
    url(
        r"^own/postulants$",
        CoursePostulationEmployerView.as_view({
            'get': 'list',
        })
    ),
    url(
        r"^own/postulants/(?P<pk>[0-9]+)$",
        CoursePostulationEmployerView.as_view({
            'get': 'retrieve',
        }),
        name='courses_by_postulant'
    ),
    url(
        r"^templates/new_course.html$",
        NewCourseFormView.as_view()
    ),
]
