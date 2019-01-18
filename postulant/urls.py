# encoding=utf-8

# from django.contrib.auth.decorators import login_required
# from django.conf.urls import include

from django.conf.urls import url
from postulant.views import (
    Signup,
    PostulantViewSet,
    PostulantBiographicViewSet,
    ProfessionalExperienceViewSet,
    PostulantLanguagesViewSet,
    PostulantComputerknowledgesViewSet,
    PostulantCvFormView,
    NewProfieccionalExperienceFormView,
    NewEducationFormView,
    PostulantEducationViewSet,
    PostulantRolesViewSet,
    JobPostulationsViewSet,
    NewReferenceFormView,
    NewLanguageFormView,
    NewComputerknowledgeFormView,
    NewCertificationFormView,
    CompletedProfileViewSet,
    CVRequestPostulantViewSet,
    PostulantAttachCVView,
    FavoritesViewSet
)

list_only = {
    'get': 'list'
}

retrieve_only = {
    'get': 'retrieve'
}

get_post = {
    'get': 'list',
    'post': 'create'
}

get_post_bulkdelete = {
    'get': 'list',
    'post': 'create',
    'delete': 'delete_bulk'
}

get_update = {
    'get': 'retrieve',
    'put': 'update'
}

get_update_post = {
    'get': 'retrieve',
    'post': 'create',
    'put': 'update'
}

update_delete = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}

get_post_delete = {
    'get': 'retrieve',
    'post': 'create',
    'delete': 'destroy'
}

urlpatterns = [
    url(
        r"^signup$",
        Signup.as_view(),
        name="postulant_signup"
    ),
    url(
        r"^profile$",
        PostulantViewSet.as_view(get_update_post)
    ),
    url(
        r"^profile/biographic$",
        PostulantBiographicViewSet.as_view(get_update_post)
    ),
    url(
        r"^profile/experience$",
        ProfessionalExperienceViewSet.as_view(get_post_bulkdelete)
    ),
    url(
        r"^profile/experience/(?P<pk>[0-9]+)$",
        ProfessionalExperienceViewSet.as_view(update_delete)
    ),
    url(
        r"^profile/education$",
        PostulantEducationViewSet.as_view(get_post_bulkdelete)
    ),
    url(
        r"^profile/education/(?P<pk>[0-9]+)$",
        PostulantEducationViewSet.as_view(update_delete)
    ),
    url(
        r"^profile/languages$",
        PostulantLanguagesViewSet.as_view(get_post_bulkdelete)
    ),
    url(
        r"^profile/languages/(?P<language>[0-9]+)$",
        PostulantLanguagesViewSet.as_view(update_delete)
    ),
    url(
        r"^profile/computerknowledges$",
        PostulantComputerknowledgesViewSet.as_view(get_post_bulkdelete)
    ),
    url(
        r"^profile/computerknowledges/(?P<computerknowledge>[0-9]+)$",
        PostulantComputerknowledgesViewSet.as_view(update_delete)
    ),
    url(
        r"^profile/roles/?$",
        PostulantRolesViewSet.as_view({
            'get': 'list',
            'post': 'set_roles'
        })
    ),
    url(
        r"^profile/completed/?$",
        CompletedProfileViewSet.as_view(retrieve_only)
    ),
    url(
        r"^profile/attachs_cv/$",
        PostulantAttachCVView.as_view(list_only)
    ),
    url(
        r"^profile/attachs_cv/(?P<filename>[^/]+)$",
        PostulantAttachCVView.as_view(get_post_delete)
    ),
    url(
        r"^panel/postulations/?$",
        JobPostulationsViewSet.as_view(list_only)
    ),
    url(
        r"^panel/favorites/?$",
        FavoritesViewSet.as_view(list_only)
    ),
    url(
        r"^panel/postulations/(?P<pk>[0-9]+)/?$",
        JobPostulationsViewSet.as_view(retrieve_only),
        name='postulant_postulation'
    ),
    url(
        r"^cvrequest$",
        CVRequestPostulantViewSet.as_view({'post': 'create'})
    ),

    # Templates
    url(
        r"^templates/cv_edit.html$",
        PostulantCvFormView.as_view()
    ),
    url(
        r"^templates/add_pe.html$",
        NewProfieccionalExperienceFormView.as_view()
    ),
    url(
        r"^templates/add_education.html$",
        NewEducationFormView.as_view()
    ),
    url(
        r"^templates/add_reference.html$",
        NewReferenceFormView.as_view()
    ),
    url(
        r"^templates/add_language.html$",
        NewLanguageFormView.as_view()
    ),
    url(
        r"^templates/add_computerknowledge.html$",
        NewComputerknowledgeFormView.as_view()
    ),
    url(
        r"^templates/add_certification.html",
        NewCertificationFormView.as_view()
    )
]
