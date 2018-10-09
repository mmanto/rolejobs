# encoding=utf-8

from django.conf.urls import url

from views import SearchInstitutionView, LanguageViewSet, EducationGradesView

urlpatterns = [
    url(
        r"^institution/search$",
        SearchInstitutionView.as_view({'get': 'list'})
    ),
    url(
        r"^languages/?$",
        LanguageViewSet.as_view({'get': 'list'})
    ),
    url(
        r"^grades/?$",
        EducationGradesView.as_view()
    )
]
