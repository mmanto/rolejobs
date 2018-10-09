# -*- coding: utf8 -*-

from __future__ import unicode_literals

# from django.conf.urls import patterns
from django.conf.urls import url
from django.contrib import admin
# from django.http import HttpResponse
from django.shortcuts import render

from jobs.models import (
    Job,
    JobForModeration,
    Area,
    SubArea,
    Role,
    Hierarchy,
    TitleRole,
    Position,
    BranchActivity,
    Technology,
    SubTechnology,
    JOB_STATUS_HAB,
    JOB_STATUS_REJECTED,
    JOB_STATUS_PENDING,
)

from jobs.forms import ModerationForm


def publish_jobs(modeladmin, request, queryset):
    user = request.user

    if user.has_perm("jobs.can_moderate"):
        for job in queryset.all():
            job.moderate(user, JOB_STATUS_HAB, u"Bulk published")

publish_jobs.short_description = u"Habilitar publicaciones"


def reject_jobs(modeladmin, request, queryset):
    user = request.user

    if user.has_perm("jobs.can_moderate"):
        for job in queryset.all():
            job.moderate(user, JOB_STATUS_REJECTED, u"Bulk rejected")

reject_jobs.short_description = u"Rechazar publicaciones"


class JobModerate(admin.ModelAdmin):

    list_display = ("title", "status_text", "moderate")
    list_display_links = None
    list_filter = ("created", "status", )
    ordering = ('-created',)
    actions = (publish_jobs, reject_jobs)

    def get_queryset(self, request):
        user = request.user
        qs = super(JobModerate, self).get_queryset(request)

        if user.is_superuser:
            return qs
        if user.has_perm("jobs.can_moderate"):
            return qs.filter(
                status__in=(
                    JOB_STATUS_HAB,
                    JOB_STATUS_PENDING)
            ).filter(
                moderated=False
            )
        else:
            return None

    def get_urls(self):

        urls = super(JobModerate, self).get_urls()

        own_urls = [
            url(
                r'^moderate/(?P<pk>\d+)/?$',
                self.admin_site.admin_view(self.moderate_view),
                name="moderate_job"
            ),
        ]

        return own_urls + urls

    def moderate_view(self, request, pk=None, *args, **kwargs):
        opts = self.opts
        job = JobForModeration.objects.get(pk=pk)
        form = ModerationForm(job=job)
        user = request.user

        if request.method == "POST":
            form = ModerationForm(job=job, data=request.POST)
            if form.is_valid():
                form.save(user)

        return render(request, "moderate_job.html", {
            "pk": pk,
            "opts": opts,
            "job": job,
            "moderation_form": form
        })

    def has_change_permission(self, request, obj=None):
        return True

    def has_module_permission(self, request):
        return True

    def moderate(self, form):
        return "<a href='moderate/%s'>Moderate</a>" % (form.id)

    moderate.allow_tags = True


admin.site.register([
    Job,
    Area,
    SubArea,
    Role,
    Hierarchy,
    TitleRole,
    Position,
    BranchActivity,
    Technology,
    SubTechnology,
])


admin.site.register(JobForModeration, JobModerate)
