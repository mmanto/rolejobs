# encoding=utf-8

from __future__ import unicode_literals

from django.db.models import Q

import rest_framework_filters as filters

from accounts.models import User
from employer.models import Employer

from models import Job


class OwnJobsFilters(filters.FilterSet):
    """Filters for own jobs lists"""

    title = filters.CharFilter(
        lookup_expr="contains")

    class Meta:
        model = Job
        fields = ("status", "title")


class BasicPublicJobsFilters(filters.FilterSet):
    """Basic filters for public jobs"""

    filter_subareas = filters.CharFilter(
        name="subarea",
        method="multi_id_filter")

    filter_roles = filters.CharFilter(
        name="roles",
        method="multi_id_filter")

    def multi_id_filter(self, qs, name, value):
        values = (int(x) for x in value.split(","))
        filter_name = "%s__in" % name

        return qs.filter(**{
            filter_name: values})

    class Meta:
        model = Job
        fields = ("filter_subareas", "filter_roles")


class EmployerFilter(filters.FilterSet):
    """Filter employer"""

    name = filters.CharFilter(
        name="name_company",
        lookup_expr="contains")

    class Meta:
        model = Employer
        fields = ('id', 'name')


class AdvancePublicJobsFilters(BasicPublicJobsFilters):
    """Filters for advance search"""

    filter_search = filters.InSetCharFilter(
        name="title",
        method="search_all")

    filter_company = filters.RelatedFilter(
        EmployerFilter,
        name="owner",
        queryset=Employer.objects.filter(
            user__is_active=True,
            user__status=User.S_ENABLED))

    filter_title_role = filters.NumberFilter(
        name="role")

    filter_position = filters.NumberFilter(
        name="position")

    filter_hierarchy = filters.NumberFilter(
        name="hierarchy")

    filter_branch_activity = filters.NumberFilter(
        name="branch_activity")

    filter_handicapped = filters.BooleanFilter(
        name="handicapped_postulant")

    filter_job_type = filters.NumberFilter(
        name="job_type")

    filter_is_new = filters.BooleanFilter(
        method="is_new")

    def search_all(self, qs, name, value):
        """Search on title and description"""

        mq = Q()
        if len(value) > 0:
            values = value[0].split(' ')
            for i in range(len(values)):
                if values[i] != '':
                    mq |= Q(title__icontains=values[i]) | Q(description__icontains=values[i])
        res = qs.filter(mq)
        return res

    def is_new(self, qs, name, value):
        """Check if is new"""
        # @TODO
        return qs

    class Meta:
        model = Job
        fields = (
            "filter_subareas",
            "filter_roles",
            "filter_search",
            "filter_title_role",
            "filter_position",
            "filter_hierarchy",
            "filter_branch_activity",
            "filter_handicapped",
            "filter_job_type",
            "filter_is_new",
        )
