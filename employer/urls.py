# encoding=utf-8

# from django.contrib.auth.decorators import login_required
# from django.conf.urls import include

from django.conf.urls import url
from . import views


list_only = {
    'get': 'list'
}

get_post = {
    'get': 'list',
    'post': 'create'
}

get_update = {
    'get': 'retrieve',
    'put': 'update'
}

update_delete = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}


urlpatterns = [
    url(
        r"^companies$",
        views.Companies.as_view()
    ),
    url(
        r"^signup$",
        views.Signup.as_view(),
        name="employer_signup"
    ),
    url(
        r"^employer",
        views.EmployerViewSet.as_view(get_update)
    ),
    url(
        r"^top10$",
        views.EmployerTopTenViewSet.as_view(list_only),
        name="employer_top_ten"
    ),
    url(
        r"^profile/my_postulants/$",
        views.PostulationsViewSet.as_view(list_only)
    ),
    url(
        r"^cvrequest/$",
        views.CVRequestViewSet.as_view(list_only)
    ),
    url(
        r"^cvrequest/(?P<pk>[0-9]+)$",
        views.CVRequestViewSet.as_view({'put': 'set_status'})
    ),
    url(
        r"^postulation/notes$",
        views.JobPostulationNoteViewSet.as_view({'post': 'create'})
    ),
    url(
        r"^postulation/notes/(?P<pk>[0-9]+)$",
        views.JobPostulationNoteViewSet.as_view(update_delete)
    ),
    url(
        r"^postulation/(?P<postulation_pk>[0-9]+)/notes$",
        views.JobPostulationNoteViewSet.as_view(list_only)
    ),
    url(
        r"^cvtags$",
        views.CVTagsViewSet.as_view(get_post)
    ),
    url(
        r"^cvtags/(?P<pk>[0-9]+)$",
        views.CVTagsViewSet.as_view({
            'get': 'retrieve',
            'put': 'update',
            'delete': 'delete_tags'
        })
    ),
    url(
        r"^cvtags/by_employer$",
        views.CVTagsViewSet.as_view({'get': 'list_tags_by_employer'})
    ),
    # templates
    url(
        r"^templates/home.html$",
        views.HomeView.as_view(),
        name="employer_home"
    ),
    # Forms
    url(
        r"^templates/signup.html$",
        views.SignupFormView.as_view(),
        name="employer_signup_form"
    ),
    url(
        r"^templates/employer.html$",
        views.EmployerFormView.as_view(),
    )
]
