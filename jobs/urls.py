# encoding=utf-8

from django.conf.urls import url
from views import (
    PublicJobsViewSet,
    OwnJobsViewSet,
    AreaViewSet,
    DetailedAreaViewSet,
    TechnologyViewSet,
    HierarchyViewSet,
    RoleViewSet,
    JobPostulationViewSet,
    OwnJobPostulationsViewSet,
    JobQuestionsFormView,
    NewJobFormView,
    KnowledgeRequirementFormView,
    QuestionFormView,
    OwnJobsInfoView,
    AdvanceSearchFiltersChoices,
    RelatedJobsViewSet,
    UserPostulationsJobs,
    EnterpriceJobs
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

get_update = {
    'get': 'retrieve',
    'put': 'update'
}

update_delete = {
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
}

post_only = {
    'post': 'create'
}

urlpatterns = [

    url(
        r"^enterpricejobs$",
        EnterpriceJobs.as_view()
    ),
    url(
        r"^userpostulationjobs$",
        UserPostulationsJobs.as_view()
    ),
    url(
        r"^jobs/(?P<pk>[0-9]+)$",
        RelatedJobsViewSet.as_view({'get': 'mretrieve'})
    ),
    url(
        r"^jobs/?$",
        PublicJobsViewSet.as_view(list_only),
        name="public_jobs"
    ),
    url(
        r"^jobs/by_area/(?P<area_pk>[0-9]+)/?$",
        PublicJobsViewSet.as_view({
            "get": "by_area"
        })
    ),
    url(
        r"^jobs/with_roles/?$",
        PublicJobsViewSet.as_view({
            "get": "with_roles"
        })
    ),
    url(
        r"^jobs/(?P<job_pk>[0-9]+)/related?$",
        RelatedJobsViewSet.as_view(list_only),
        name="job_detail"
    ),
    url(
        r"^jobs/(?P<job_pk>[0-9]+)/postulate/?$",
        JobPostulationViewSet.as_view(post_only),
    ),
    url(
        r"^own_info$",
        OwnJobsInfoView.as_view()
    ),
    url(
        r"^own/?$",
        OwnJobsViewSet.as_view(get_post),
        name="own_jobs"
    ),
    url(
        r"^own/(?P<pk>[0-9]+)/?$",
        OwnJobsViewSet.as_view(update_delete),
        name="own_job_detail"
    ),
    url(
        r"^own/(?P<job_pk>[0-9]+)/postulations/?$",
        OwnJobPostulationsViewSet.as_view(list_only)
    ),
    url(
        r"^own/(?P<job_pk>[0-9]+)/postulations/(?P<pk>[0-9]+)/?$",
        OwnJobPostulationsViewSet.as_view({
            "get": "retrieve",
            "put": "set_status"
        })
    ),
    url(
        r"^own/(?P<job_pk>[0-9]+)/postulations/(?P<pk>[0-9]+)/favorite$",
        OwnJobPostulationsViewSet.as_view({
            "put": "set_favorite"
        })
    ),
    url(
        r"^own/lasts$",
        OwnJobsViewSet.as_view({"get": "get_lasts"}),
    ),
    url(
        r"^areas/?$",
        AreaViewSet.as_view(list_only)
    ),
    url(
        r"^areas/(?P<pk>[0-9]+)$",
        DetailedAreaViewSet.as_view(retrieve_only)
    ),
    url(
        r"^areas/(?P<slug>[a-z0-9_-]+)$",
        DetailedAreaViewSet.as_view({"get": "by_slug"})
    ),
    url(
        r"^technologies/?$",
        TechnologyViewSet.as_view(list_only)
    ),
    url(
        r"^technologies/(?P<pk>[0-9]+)/?$",
        TechnologyViewSet.as_view(retrieve_only)
    ),
    url(
        r"hierarchies/?$",
        HierarchyViewSet.as_view(list_only)
    ),
    url(
        r"^roles/?$",
        RoleViewSet.as_view(list_only)
    ),
    url(
        r"^as_choices/?$",
        AdvanceSearchFiltersChoices.as_view()
    ),
    # Forms
    url(
        r"^jobs/(?P<job_pk>[0-9]+)/postulate_form.html$",
        JobQuestionsFormView.as_view(),
    ),
    url(
        r"^templates/new_job.html$",
        NewJobFormView.as_view()
    ),
    url(
        r"^templates/new_knowledge_requirement.html$",
        KnowledgeRequirementFormView.as_view()
    ),
    url(
        r"^templates/new_question.html",
        QuestionFormView.as_view()
    )
]
