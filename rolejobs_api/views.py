# -*- encoding: utf-8 -*-

from django.views import generic
from jobs.models import Job, JobPostulation
from accounts.models import User
from django.http import JsonResponse

class StatsView(generic.View):
    
    def get(self, response):
        jobs = len(Job.objects.all())
        postulations = len(JobPostulation.objects.all())
        enterprices = 0
        for user in User.objects.all():
            if user.is_employer:
                enterprices += 1
        return JsonResponse({ "jobs": jobs, "postulations": postulations, "enterprices": enterprices })