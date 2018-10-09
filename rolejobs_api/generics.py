# -*- coding: utf-8 -*-

from django.conf import settings

from rest_framework.pagination import PageNumberPagination


class StandarPagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = settings.STANDAR_PAGE_SIZE
    max_page_size = settings.STANDAR_MAX_PAGE_SIZE
