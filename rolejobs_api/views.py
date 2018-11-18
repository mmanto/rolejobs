# -*- encoding: utf-8 -*-

from django.views import generic
from jobs.models import Job, JobPostulation
from accounts.models import User
from django.http import JsonResponse

class StatsView(generic.View):
    
    def get(self, response):
        jobs = len(Job.objects.all())
        users = 0
        employers = 0
        for user in User.objects.all():
            if user.is_employer:
                employers += 1
            users += 1
        return JsonResponse({ "jobs": jobs, "users": users, "employers": employers })