# -*- encoding: utf-8 -*-

from django.views import generic


class HomeView(generic.TemplateView):
    template_name = 'test.html'
